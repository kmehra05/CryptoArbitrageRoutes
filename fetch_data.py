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

    def get_exchange_names(self):
        return ['kraken', 'gemini']

    def fetch_tickers(self, *symbols):
        all_prices = {}
        # Generate pairs for each symbol against USD and every combination with other symbols
        pairs = [f"{sym}/USD" for sym in symbols]
        pairs += [f"{sym1}/{sym2}" for sym1 in symbols for sym2 in symbols if sym1 != sym2]

        for pair in pairs:
            prices = {}
            valid_data_found = False  # Flag to track if any valid data was found for the pair
            for exchange_name, exchange in self.exchanges.items():
                try:
                    ticker = exchange.fetch_ticker(pair)
                    prices[exchange_name] = {
                        'bid': ticker['bid'],
                        'ask': ticker['ask']
                    }
                    valid_data_found = True  # Set flag true if at least one exchange returns data
                except Exception as e:
                    print(f"Error fetching data from {exchange_name} for {pair}: {str(e)}")

            # Only add pair to all_prices if at least one exchange has valid data
            if valid_data_found:
                all_prices[pair] = prices

        return all_prices