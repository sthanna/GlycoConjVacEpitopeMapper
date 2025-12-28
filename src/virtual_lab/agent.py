# --------------------------------------------------------------------------------
# Author: Sandeep Thanna
# Copyright: 2025, Sandeep Thanna
# Maintainer: Sandeep Thanna
# --------------------------------------------------------------------------------
from typing import List, Dict, Any, Optional
from pathlib import Path
import google.generativeai as genai
from .constants import GEMINI_API_KEY, DEFAULT_MODEL

# Configure Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Warning: Failed to configure Gemini API: {e}")

class Agent:
    def __init__(
        self, 
        name: str = "", 
        role: str = "", 
        system_prompt: str = "", 
        model: str = DEFAULT_MODEL, 
        tools: Optional[List[Any]] = None,
        # Legacy/Compatibility args
        title: Optional[str] = None,
        prompt: Optional[str] = None,
        instructions: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize a Virtual Lab Agent with Gemini.
        """
        # Resolve Name/Title
        self.name = name or title or "Unknown Agent"
        
        # Resolve Role
        self.role = role or self.name
        
        # Resolve System Prompt
        self.system_prompt = system_prompt or prompt or instructions or ""
        
        self.model_name = model
        self.tools = tools if tools else []
        self.history: List[Dict[str, str]] = [{"role": "user", "parts": [self.system_prompt]}]
        
        # Initialize Gemini Model
        self.generative_model = genai.GenerativeModel(self.model_name)
        self.chat = self.generative_model.start_chat(history=[])
        self._processed_history_len = 0
        
        self.extras = kwargs
        
        # RAG Support
        self.kb_path = kwargs.get("kb_path")
        self.vector_store = None
        if self.kb_path and Path(self.kb_path).exists():
            try:
                from langchain_community.vectorstores import FAISS
                from langchain_huggingface import HuggingFaceEmbeddings
                embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                self.vector_store = FAISS.load_local(self.kb_path, embeddings, allow_dangerous_deserialization=True)
                print(f"[{self.name}] Knowledge base loaded from {self.kb_path}")
            except Exception as e:
                print(f"[{self.name}] Failed to load knowledge base: {e}")

    @property
    def title(self):
        return self.name

    @property
    def prompt(self):
        return self.system_prompt

    def query_kb(self, query: str, k: int = 3) -> str:
        """
        Query the agent's knowledge base for relevant context.
        """
        if not self.vector_store:
            return ""
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            context = "\n---\n".join([r.page_content for r in results])
            return f"\n\nContext from Knowledge Base:\n{context}\n\n"
        except Exception as e:
            print(f"[{self.name}] Error querying KB: {e}")
            return ""

    def _sync_history(self, conversation_history: List[Dict[str, str]]):
        """
        Synchronize the internal chat session with the external conversation history.
        We skip the last message as it's the prompt we're about to respond to.
        """
        # If external history is shorter than what we've processed, something reset (unlikely)
        if len(conversation_history) < self._processed_history_len:
            self.reset_history()
            
        # Process new messages (excluding the current prompt at the end)
        new_messages = conversation_history[self._processed_history_len : -1]
        
        for entry in new_messages:
            role = entry.get('role', 'user')
            name = entry.get('name', 'Unknown')
            content = entry.get('content') or entry.get('message') or ""
            
            # Formulate as a context message
            # If it's our own message, we should ideally inform the chat session it was "us"
            # But in multi-agent, the ChatSession thinks "user" is everyone else.
            
            msg_text = f"[{role}] {name}: {content}"
            
            # Prepend system instruction on the very first message
            if not self.chat.history:
                msg_text = f"System Instruction: {self.system_prompt}\n\n" + msg_text
            
            # Send message without generating a response (catchup)
            # Actually, standard ChatSession doesn't have a simple "append" without calling.
            # We can use chat.history.append({'role': 'user', 'parts': [msg_text]})
            # and when it's our own turn, append as 'model'.
            
            if name == self.name:
                self.chat.history.append({'role': 'model', 'parts': [content]})
            else:
                self.chat.history.append({'role': 'user', 'parts': [msg_text]})
        
        self._processed_history_len = len(conversation_history) - 1

    def respond(self, conversation_history: List[Dict[str, str]]) -> str:
        """
        Generate a response using Gemini's native multi-turn chat capability.
        """
        if not conversation_history:
            return f"[{self.role}] Ready."

        # 1. Sync history
        self._sync_history(conversation_history)
            
        # 2. Extract final prompt
        last_entry = conversation_history[-1]
        last_msg = last_entry.get('content') or last_entry.get('message') or ""
        sender = last_entry.get('name', 'Unknown')
        role = last_entry.get('role', 'user')
        
        # 3. Retrieve context if RAG is enabled
        kb_context = ""
        if self.vector_store:
            kb_context = self.query_kb(last_msg)

        input_text = f"[{role}] {sender}: {last_msg}\n\n{kb_context}[{self.role}] (You):"
        
        # If history is still empty (this is the first message), prepend system instruction
        if not self.chat.history:
             input_text = f"System Instruction: {self.system_prompt}\n\n" + input_text

        try:
            response = self.chat.send_message(input_text)
            response_text = response.text.strip()
            # Update processed len (since we just added the prompt and our response)
            self._processed_history_len = len(conversation_history) 
            return response_text
        except Exception as e:
            return f"[{self.role}] Error generating response: {e}"

    def reset_history(self):
        self.chat = self.generative_model.start_chat(history=[])
        self._processed_history_len = 0
