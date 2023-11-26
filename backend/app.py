import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import evadb_stock_forecasting
import app_secrets


app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    ticker = data.get('ticker')
    model = data.get('model', None) 
    if model == None:
        return jsonify({"error": "Model must be specified"}), 400
    if ticker == None:
        return jsonify({"error": "Ticker must be specified"}), 400
    if model:
        print(model)
        try:
            res = evadb_stock_forecasting.getForecast(ticker, model)
            return jsonify({
                "forecast": str(res[0]),
                "low": str(res[1]),
                "high": str(res[2])
                })
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500
    
@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))