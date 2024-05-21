# Cryptocurrency Arbitrage Routes

## Project Overview
Cryptocurrency Arbitrage Routes is a system that leverages a custom implementation of Dijkstra's algorithm to identify the most profitable arbitrage opportunities across various cryptocurrency exchanges. By exploiting the price differences of the same asset on different markets (bid/ask spread), the tool helps visualize the most lucrative path considering potential gains.

<img src="https://github.com/kmehra05/CryptoArbitrageRoutes/assets/17500616/a61a0e5a-e91e-439e-8487-20168d8302d6" width="50%">

## Features
- **Data Integration:** Real-time and historical pricing data from multiple exchanges are integrated using ccxt.
- **Graph Construction:** Constructs a dynamic graph with networkx where nodes represent exchange/ticker pairs, and edges denote potential arbitrage opportunities, factoring in the inverse of the profitability multiplier as the edge weight to easily be used for Djikstra’s algorithm with the purpose of maximum path length rather than minimum path length.
- **Path Optimization:** Utilizes a custom implementation of Dijkstra's algorithm tailored for maximizing profitability by considering the compounded effect of consecutive arbitrage opportunities by multiplying edge weights to determine path length instead of summing.
- **Interactive GUI:** Users can select cryptocurrencies to analyze and visualize the optimal arbitrage path starting from a chosen ticker and exchange, with profit metrics shown.

## Tools and Technologies
- **Python:** Primary programming language.
- **ccxt:** Library used for fetching data from various exchanges.
- **networkx:** Facilitates the construction and manipulation of complex network graphs.
- **Tkinter:** For creating the GUI
- **matplotlib:** For visualizing the results and optimal paths graphically in the GUI

## Installation
Refer to `INSTALL.md` for detailed installation and setup instructions.

## Limitations
- **Theoretical Application:** The current implementation does not account for transaction costs, which affects profitability metrics that are outputted.
- **Performance:** Due to computational complexity, the scalability is currently limited, affecting performance with large sets of tickers.
- **Exchange Coverage:** Initially configured for two exchanges, but expandable via modifications in `fetch_data.py`.

## Usage
To run the project:
```bash
python main.py
```
