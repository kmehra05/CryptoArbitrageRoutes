# Installation Guide for CryptoArbitrage

This document provides the instructions for setting up and running the CryptoArbitrage project on your local machine.

## Prerequisites

Before you begin, ensure you have Python installed on your system. Python 3.6 or higher is recommended. You can download Python from [python.org](https://www.python.org/downloads/).

## Environment Setup

1. **Clone the Repository:**
   Clone the CryptoArbitrage project to your local machine.
2. **Navigate to the Project Directory:**
cd CryptoArbitrage
3. **Install Python Dependencies:**
Install all the required Python packages using either:
   - `pip install -r requirements.txt`
   - `pip3 install -r requirements.txt`

## Configuration

1. **Environment Variables:**
Create a `.env` file in the root directory of the project and populate it with necessary environment variables:
   - `KRAKEN_PRIVATE_KEY = your_kraken_private_key`
   - `KRAKEN_API_KEY = your_kraken_api_key`
   - `GEMINI_PRIVATE_KEY = your_gemini_private_key`
   - `GEMINI_API_KEY = your_gemini_api_key`
   - **Replace `your_api_key_here` and `your_private_key_here` with your actual API keys.**

