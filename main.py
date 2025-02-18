from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os

app = Flask(__name__, static_folder='static')

# تكوين المنفذ للعمل مع Railway
port = int(os.environ.get('PORT', 5000))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        # استلام البيانات من الطلب
        calculation_type = data.get('calculation_type')
        currency = data.get('currency')
        
        if calculation_type == "chicken_profits":
            eggs = float(data.get('eggs', 0))
            days = float(data.get('days', 0))
            
            # حساب الأرباح
            egg_price = 0.1155  # سعر البيض الافتراضي
            feed_price = 0.0189  # سعر العلف الافتراضي
            
            total_egg_price = eggs * egg_price
            total_feed_cost = (days * 2) * feed_price
            total_rent = 6 if eggs >= 260 else 0
            
            net_profit_before_rent = total_egg_price - total_feed_cost
            net_profit = net_profit_before_rent - total_rent
            
            if currency == "IQD":
                conversion_rate = 1480
                total_egg_price *= conversion_rate
                total_feed_cost *= conversion_rate
                net_profit_before_rent *= conversion_rate
                total_rent *= conversion_rate
                net_profit *= conversion_rate
            
            return jsonify({
                'total_egg_price': total_egg_price,
                'total_feed_cost': total_feed_cost,
                'net_profit_before_rent': net_profit_before_rent,
                'total_rent': total_rent,
                'net_profit': net_profit
            })
            
        elif calculation_type == "daily_rewards":
            rewards = float(data.get('rewards', 0))
            food = float(data.get('food', 0))
            
            egg_price = 0.1155
            feed_price = 0.0189
            
            daily_profit = rewards * egg_price - food * feed_price
            
            if currency == "IQD":
                daily_profit *= 1480
                
            return jsonify({
                'daily_profit': daily_profit
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True) 