import os
from dotenv import load_dotenv
load_dotenv()

kraken_api_key = os.getenv('KRAKEN_API_KEY')
kraken_private_key = os.getenv('KRAKEN_PRIVATE_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')
gemini_private_key = os.getenv('GEMINI_PRIVATE_KEY')