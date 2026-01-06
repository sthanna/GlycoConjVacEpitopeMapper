# --------------------------------------------------------------------------------
# Author: Sandeep Thanna
# Copyright: 2025, Sandeep Thanna
# Maintainer: Sandeep Thanna
# --------------------------------------------------------------------------------
from typing import List, Dict, Any, Optional
from pathlib import Path
from google import genai
from .constants import GEMINI_API_KEY, DEFAULT_MODEL

# Initialize Gemini Client (new unified SDK)
try:
    _genai_client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Warning: Failed to initialize Gemini Client: {e}")
    _genai_client = None

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
        
        # Initialize Gemini Chat using new unified SDK
        self.chat = None
        if _genai_client:
            try:
                self.chat = _genai_client.chats.create(model=self.model_name)
            except Exception as e:
                print(f"Warning: Failed to create chat for {self.name}: {e}")
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
        
        Note: The new google.genai SDK doesn't expose chat.history for direct manipulation.
        We rely on _processed_history_len to track what's been sent to the model.
        """
        # If external history is shorter than what we've processed, something reset (unlikely)
        if len(conversation_history) < self._processed_history_len:
            self.reset_history()
            
        # Process new messages (excluding the current prompt at the end)
        # In the new SDK, we can't directly manipulate history, so we'll
        # send catch-up context in the next actual message if needed
        new_messages = conversation_history[self._processed_history_len : -1]
        
        if new_messages:
            # Build a context summary of missed messages
            context_parts = []
            for entry in new_messages:
                role = entry.get('role', 'user')
                name = entry.get('name', 'Unknown')
                content = entry.get('content') or entry.get('message') or ""
                context_parts.append(f"[{role}] {name}: {content}")
            
            # Store context to prepend to next message
            if not hasattr(self, '_pending_context'):
                self._pending_context = ""
            self._pending_context += "\n".join(context_parts) + "\n"
        
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
        
        # Include any pending context from history synchronization
        if hasattr(self, '_pending_context') and self._pending_context:
            input_text = f"Previous conversation:\n{self._pending_context}\n\n" + input_text
            self._pending_context = ""
        
        # If this is the first message, prepend system instruction
        if not hasattr(self, '_first_message_sent') or not self._first_message_sent:
            input_text = f"System Instruction: {self.system_prompt}\n\n" + input_text
            self._first_message_sent = True

        try:
            if not self.chat:
                return f"[{self.role}] Error: Chat not initialized"
            response = self.chat.send_message(message=input_text)
            response_text = response.text.strip()
            # Update processed len (since we just added the prompt and our response)
            self._processed_history_len = len(conversation_history) 
            return response_text
        except Exception as e:
            return f"[{self.role}] Error generating response: {e}"

    def reset_history(self):
        if _genai_client:
            try:
                self.chat = _genai_client.chats.create(model=self.model_name)
            except Exception as e:
                print(f"Warning: Failed to reset chat for {self.name}: {e}")
        self._processed_history_len = 0
        self._first_message_sent = False
        self._pending_context = ""
