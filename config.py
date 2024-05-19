import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access an environment variable
binance_api_key = os.getenv('BINANCE_API_KEY')
