from flask import Flask, render_template, jsonify, request, session
import csv
import json
from datetime import datetime, timedelta
import random
import threading
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Global stock data
stock_data = {}

def load_stock_data():
    with open('stock_data.csv', 'r') as file:
        reader = csv.DictReader(file)
        return {row['symbol']: float(row['price']) for row in reader}

def update_stock_prices():
    global stock_data
    while True:
        for symbol in stock_data:
            # Update price with random walk
            change = random.gauss(0.001, 0.01)  # Mean of 0.1% daily return, std dev of 1%
            stock_data[symbol] *= (1 + change)
            stock_data[symbol] = round(stock_data[symbol], 2)
        time.sleep(3)  # Update every 3 seconds

def generate_price_history(price, days=30):
    history = []
    current_price = price
    for _ in range(days):
        change = random.gauss(0.001, 0.01)
        current_price *= (1 + change)
        history.append(round(current_price, 2))
    return history

# Initialize user portfolio in session if not exists
def init_portfolio():
    if 'portfolio' not in session:
        session['portfolio'] = {
            'cash': 10000.0,  # Starting with $10,000
            'stocks': {}  # Dictionary to store owned stocks
        }

@app.route('/')
def index():
    init_portfolio()
    return render_template('index.html')

@app.route('/get_stock_data/<symbol>')
def get_stock_data(symbol):
    try:
        if symbol not in stock_data:
            return jsonify({'success': False, 'error': 'Stock not found'})
        
        current_price = stock_data[symbol]
        price_history = generate_price_history(current_price)
        dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(29, -1, -1)]
        
        return jsonify({
            'success': True,
            'current_price': current_price,
            'dates': dates,
            'prices': price_history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    data = request.get_json()
    symbol = data.get('symbol')
    shares = int(data.get('shares'))
    
    try:
        if symbol not in stock_data:
            return jsonify({'success': False, 'error': 'Stock not found'})
        
        current_price = stock_data[symbol]
        total_cost = current_price * shares
        
        if total_cost > session['portfolio']['cash']:
            return jsonify({'success': False, 'error': 'Insufficient funds'})
        
        # Update portfolio
        session['portfolio']['cash'] -= total_cost
        if symbol in session['portfolio']['stocks']:
            session['portfolio']['stocks'][symbol] += shares
        else:
            session['portfolio']['stocks'][symbol] = shares
        
        session.modified = True
        return jsonify({
            'success': True,
            'new_cash': session['portfolio']['cash'],
            'new_shares': session['portfolio']['stocks'].get(symbol, 0)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/sell_stock', methods=['POST'])
def sell_stock():
    data = request.get_json()
    symbol = data.get('symbol')
    shares = int(data.get('shares'))
    
    try:
        if symbol not in session['portfolio']['stocks'] or session['portfolio']['stocks'][symbol] < shares:
            return jsonify({'success': False, 'error': 'Insufficient shares'})
        
        if symbol not in stock_data:
            return jsonify({'success': False, 'error': 'Stock not found'})
        
        current_price = stock_data[symbol]
        total_proceeds = current_price * shares
        
        # Update portfolio
        session['portfolio']['cash'] += total_proceeds
        session['portfolio']['stocks'][symbol] -= shares
        
        if session['portfolio']['stocks'][symbol] == 0:
            del session['portfolio']['stocks'][symbol]
        
        session.modified = True
        return jsonify({
            'success': True,
            'new_cash': session['portfolio']['cash'],
            'new_shares': session['portfolio']['stocks'].get(symbol, 0)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_portfolio')
def get_portfolio():
    return jsonify(session['portfolio'])

if __name__ == '__main__':
    # Initialize stock data
    stock_data = load_stock_data()
    
    # Start price update thread
    update_thread = threading.Thread(target=update_stock_prices, daemon=True)
    update_thread.start()
    
    app.run(debug=True) 