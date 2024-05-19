import ccxt
import config


class ExchangeDataFetcher:
    def __init__(self):
        self.exchanges = {
            'kraken': ccxt.kraken({
                'apiKey': config.kraken_api_key,
                'secret': config.kraken_private_key
            }),
            'gemini': ccxt.gemini({
                'apiKey': config.gemini_api_key,
                'secret': config.gemini_private_key
            })
        }

    def fetch_tickers(self, *symbols):
        all_prices = {}
        for symbol in symbols:
            prices = {}
            for exchange_name, exchange in self.exchanges.items():
                try:
                    ticker = exchange.fetch_ticker(symbol)
                    prices[exchange_name] = {
                        'bid': ticker['bid'],
                        'ask': ticker['ask']
                    }
                except Exception as e:
                    print(f"Error fetching data from {exchange_name}: {str(e)}")
            all_prices[symbol] = prices
        return all_prices
