import tkinter as tk
from tkinter import ttk
import fetch_data

class MainWindow(tk.Tk):
    def __init__(self, exchange_list):
        super().__init__()
        self.title("Cryptocurrency Arbitrage Pathfinder")
        self.exchange_list = exchange_list
        self.init_ui()

    def init_ui(self):

        # Entry for the crypto ticker
        label_tickers = tk.Label(self, text="Enter Crypto Tickers (comma separated)")
        label_tickers.pack(pady=10)

        self.ticker_list = ttk.Entry(self, foreground="grey")
        self.ticker_list.pack(pady=10)
        self.ticker_list.insert(0, "BTC, ETH, DOGE")
        self.ticker_list.bind("<FocusIn>", self.on_focus_in_list)
        self.ticker_list.bind("<FocusOut>", self.on_focus_out_list)

        label_ticker = tk.Label(self, text="Enter Starting Ticker (BTC):")
        label_ticker.pack(pady=10)

        self.ticker_entry = ttk.Entry(self, foreground="grey")
        self.ticker_entry.pack(pady=10)
        self.ticker_entry.insert(0, "BTC")
        self.ticker_entry.bind("<FocusIn>", self.on_focus_in_entry)
        self.ticker_entry.bind("<FocusOut>", self.on_focus_out_entry)

        # Dropdown Menu to choose the exchange
        label_exchange = tk.Label(self, text="Select Starting Exchange:")
        label_exchange.pack(pady=10)

        self.exchange_var = tk.StringVar(self)
        dropdown_exchange = ttk.Combobox(self, textvariable=self.exchange_var)
        dropdown_exchange['values'] = self.exchange_list
        dropdown_exchange.pack(pady=10)

        # Button to find and display the best path
        self.plot_button = ttk.Button(self, text="Start")
        self.plot_button.pack(pady=20)

    def on_focus_in_list(self, event):
        if self.ticker_list.get() == 'BTC, ETH, DOGE':
            self.ticker_list.delete(0, tk.END)
            self.ticker_list.config(foreground="black")

    def on_focus_out_list(self, event):
        if not self.ticker_list.get():
            self.ticker_list.insert(0, 'BTC, ETH, DOGE')
            self.ticker_list.config(foreground="grey")

    def on_focus_in_entry(self, event):
        if self.ticker_entry.get() == 'BTC':
            self.ticker_entry.delete(0, tk.END)
            self.ticker_entry.config(foreground="black")

    def on_focus_out_entry(self, event):
        if not self.ticker_entry.get():
            self.ticker_entry.insert(0, 'BTC')
            self.ticker_entry.config(foreground="grey")

def main():
    data_fetcher = fetch_data.ExchangeDataFetcher()
    app = MainWindow(data_fetcher.get_exchange_names())
    app.mainloop()

if __name__ == "__main__":
    main()
