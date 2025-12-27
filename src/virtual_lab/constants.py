"""Holds constants."""

DEFAULT_MODEL = "gemini-3-flash-preview"
GEMINI_API_KEY = "AIzaSyAarvWr0hFZWw6fOSxnGpkMMmXPudtYHdU"

# Prices Placeholders (Gemini pricing varies, leaving empty or generic for now)
MODEL_TO_INPUT_PRICE_PER_TOKEN = {}
MODEL_TO_OUTPUT_PRICE_PER_TOKEN = {}

FINETUNING_MODEL_TO_INPUT_PRICE_PER_TOKEN = {}
FINETUNING_MODEL_TO_OUTPUT_PRICE_PER_TOKEN = {}
FINETUNING_MODEL_TO_TRAINING_PRICE_PER_TOKEN = {}

DEFAULT_FINETUNING_EPOCHS = 4

CONSISTENT_TEMPERATURE = 0.2
CREATIVE_TEMPERATURE = 0.8

PUBMED_TOOL_NAME = "pubmed_search"
PUBMED_TOOL_DESCRIPTION = {
    "function_declarations": [{
        "name": PUBMED_TOOL_NAME,
        "description": "Get abstracts or the full text of biomedical and life sciences articles from PubMed Central.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to use to search PubMed Central for scientific articles.",
                },
                "num_articles": {
                    "type": "integer",
                    "description": "The number of articles to return from the search query.",
                },
                "abstract_only": {
                    "type": "boolean",
                    "description": "Whether to return only the abstract of the articles.",
                },
            },
            "required": ["query", "num_articles"],
        },
    }]
}
