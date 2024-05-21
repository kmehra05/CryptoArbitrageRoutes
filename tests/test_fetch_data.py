import unittest
from unittest.mock import patch
from src import fetch_data


class TestExchangeDataFetcher(unittest.TestCase):
    @patch('fetch_data.ccxt.kraken')
    @patch('fetch_data.ccxt.gemini')
    @patch('fetch_data.config')
    def setUp(self, mock_config, mock_kraken, mock_gemini):
        mock_config.kraken_api_key = 'test_kraken_key'
        mock_config.kraken_private_key = 'test_kraken_secret'
        mock_config.gemini_api_key = 'test_gemini_key'
        mock_config.gemini_private_key = 'test_gemini_secret'
        self.fetcher = fetch_data.ExchangeDataFetcher()

    def test_get_exchange_names(self):
        self.assertEqual(self.fetcher.get_exchange_names(), ['kraken', 'gemini'])

    @patch.object(fetch_data.ExchangeDataFetcher, 'fetch_tickers')
    def test_fetch_tickers(self, mock_fetch_tickers):
        mock_fetch_tickers.return_value = {
            'BTC/USD': {'kraken': {'bid': 50000, 'ask': 50010}, 'gemini': {'bid': 50020, 'ask': 50030}}}
        result = self.fetcher.fetch_tickers('BTC')
        self.assertIn('BTC/USD', result)
        self.assertDictEqual(result['BTC/USD'],
                             {'kraken': {'bid': 50000, 'ask': 50010}, 'gemini': {'bid': 50020, 'ask': 50030}})


if __name__ == '__main__':
    unittest.main()
