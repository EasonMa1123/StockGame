# Stock Market Game

A web-based stock market game where users can buy and sell stocks using real market data. The game features an interactive chart showing stock price history and a portfolio management system.

## Features

- Real-time stock data using Yahoo Finance API
- Interactive stock price charts
- Buy and sell stocks
- Portfolio tracking
- Starting balance of $10,000
- Modern and responsive UI

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your web browser and navigate to:
```
http://localhost:5000
```

## How to Play

1. Enter a stock symbol (e.g., AAPL for Apple, GOOGL for Google) in the search box
2. Press Enter or click the Buy/Sell buttons to view the stock's current price and chart
3. Enter the number of shares you want to buy or sell
4. Click the Buy or Sell button to execute the trade
5. Monitor your portfolio value and available cash

## Note

This is a game for educational purposes only. It uses real market data but is not connected to any real trading platform. All trades are simulated within the game. 