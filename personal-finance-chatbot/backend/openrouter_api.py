import os
import requests
import logging
from transformers import pipeline
from dotenv import load_dotenv

# =========================
# 🔹 Load Environment Variables
# =========================
load_dotenv()  # Ensure .env variables are loaded

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_TIMEOUT = int(os.getenv("OPENROUTER_TIMEOUT", "30"))  # Default 30 seconds timeout

# =========================
# 🔹 Logging Setup
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if OPENROUTER_API_KEY:
    logger.info(f"✅ OPENROUTER_API_KEY loaded successfully: {OPENROUTER_API_KEY[:8]}...")
else:
    logger.error("❌ OPENROUTER_API_KEY is NOT set. Check your .env file.")

# =========================
# 🔹 Lazy Pipeline Initialization
# =========================
_sentiment_analyzer = None
_ner_tagger = None


def analyze_nlu(text: str):
    """
    Perform sentiment analysis and named entity recognition (NER) on the given text.
    Returns sentiment, entities, and keywords.
    """
    global _sentiment_analyzer, _ner_tagger

    try:
        # Initialize sentiment analyzer if not already loaded
        if _sentiment_analyzer is None:
            logger.info("Loading sentiment analysis model...")
            _sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )

        # Initialize NER tagger if not already loaded
        if _ner_tagger is None:
            logger.info("Loading NER model...")
            _ner_tagger = pipeline(
                "ner",
                model="dslim/bert-base-NER",
                aggregation_strategy="simple"
            )

        sentiment_result = _sentiment_analyzer(text)[0]
        sentiment = sentiment_result['label'].lower()

        ner_results = _ner_tagger(text)
        entities = [ent['word'] for ent in ner_results]

        keywords = list(set(entities))[:5]

        return {
            "sentiment": sentiment,
            "entities": entities,
            "keywords": keywords
        }

    except Exception as e:
        logger.error(f"❌ NLU analysis failed: {e}")
        return {
            "sentiment": "neutral",
            "entities": [],
            "keywords": []
        }


def generate_response(messages):
    """
    Send messages to OpenRouter API and return the model's response.
    """
    if not OPENROUTER_API_KEY:
        error_msg = "❌ OPENROUTER_API_KEY is not set in environment variables"
        logger.error(error_msg)
        raise ValueError(error_msg)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7,
        "top_p": 0.95,
        "n": 1,
        "stream": False
    }

    try:
        logger.info(f"📡 Sending request to OpenRouter model: {OPENROUTER_MODEL}")
        response = requests.post(
            OPENROUTER_API_URL, json=payload, headers=headers, timeout=OPENROUTER_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        reply = data['choices'][0]['message']['content']
        logger.info("✅ Response received from OpenRouter")
        return reply

    except requests.exceptions.Timeout:
        logger.error("⏳ Request to OpenRouter API timed out.")
        raise
    except requests.exceptions.ConnectionError as e:
        logger.error(f"🌐 Connection error: {e}")
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(f"❌ HTTP error: {e} - Response: {response.text}")
        raise
    except Exception as e:
        logger.error(f"⚠️ Unexpected error: {e}")
        raise
