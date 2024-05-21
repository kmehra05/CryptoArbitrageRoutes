import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.pathfinding import *

class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Cryptocurrency Arbitrage Pathfinder")
        self.init_ui()

    def init_ui(self):
        # Entry for the crypto ticker
        label_tickers = tk.Label(self, text="Enter Crypto Tickers (comma separated):")
        label_tickers.pack(pady=10)

        self.ticker_list = ttk.Entry(self, foreground="grey")
        self.ticker_list.pack(pady=10)
        self.ticker_list.insert(0, "BTC, ETH, DOGE")
        self.ticker_list.bind("<FocusIn>", self.on_focus_in_list)
        self.ticker_list.bind("<FocusOut>", self.on_focus_out_list)

        label_ticker = tk.Label(self, text="Enter Starting Ticker:")
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
        self.dropdown_exchange = ttk.Combobox(self, textvariable=self.exchange_var)
        self.dropdown_exchange.pack(pady=10)

        # Button to find and display the best path
        self.plot_button = ttk.Button(self, text="Start", command=self.on_plot_button_clicked)
        self.plot_button.pack(pady=20)

        self.path_summary = tk.Label(self, text="")
        self.path_summary.pack(pady=20)

        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

    def on_focus_in_list(self, event):
        if self.ticker_list.get() == 'BTC, ETH, DOGE':
            self.ticker_list.delete(0, tk.END)
            self.ticker_list.config(foreground="white")

    def on_focus_out_list(self, event):
        if not self.ticker_list.get():
            self.ticker_list.insert(0, 'BTC, ETH, DOGE')
            self.ticker_list.config(foreground="grey")

    def on_focus_in_entry(self, event):
        if self.ticker_entry.get() == 'BTC':
            self.ticker_entry.delete(0, tk.END)
            self.ticker_entry.config(foreground="white")

    def on_focus_out_entry(self, event):
        if not self.ticker_entry.get():
            self.ticker_entry.insert(0, 'BTC')
            self.ticker_entry.config(foreground="grey")

    def on_plot_button_clicked(self):
        self.summary_to_loading()  # Show loading indicator
        self.controller.plot_graph()

    def update_exchange_list(self, exchange_list):
        self.dropdown_exchange['values'] = exchange_list

    def get_user_inputs(self):
        return {
            'tickers': self.ticker_list.get().replace(' ', '').split(','),
            'start_ticker': self.ticker_entry.get(),
            'start_exchange': self.exchange_var.get()
        }

    def summary_to_loading(self):
        self.path_summary.config(text="Loading...", fg="red")

    def loading_to_summary(self, summary):
        self.path_summary.config(text=summary, fg="white")

    def loading_to_error(self, error):
        self.path_summary.config(text=f"Error: {error}", fg="red")

    def display_graph(self, graph, total_multiplier):
        self.path_summary.config(text=generate_best_path_summary(graph, total_multiplier, 100))
        plt.figure(figsize=(10, 5))
        pos = nx.planar_layout(graph)

        # Draw nodes
        nx.draw_networkx_nodes(graph, pos, node_color='skyblue', node_size=1500)

        # Draw labels for nodes
        nx.draw_networkx_labels(graph, pos, font_size=8, font_color='black')

        # Draw edges with arrows
        nx.draw_networkx_edges(graph, pos, edge_color='k', arrowstyle='-|>', arrowsize=50)

        # Format and draw edge labels with custom formatting
        edge_labels = nx.get_edge_attributes(graph, 'weight')  # Assuming the weights are stored under 'weight'
        formatted_edge_labels = {k: f"x{v:.5f}" for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=formatted_edge_labels, font_color='red')

        plt.draw()

        # Clear previous canvas if it exists
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()

        # Create new canvas and embed matplotlib plot
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        plt.close()  # Close the plot to free up memory
