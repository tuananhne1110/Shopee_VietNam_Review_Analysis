from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from bs4 import BeautifulSoup
from Shopee import Shopee_extract
app = Flask("Take_Request")
CORS(app)

@app.route('/save_html', methods=['OPTIONS', 'POST'])
def save_html():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    if request.method == 'POST':
        data = request.json
        html_content = data.get('html_content', '')
        if not html_content:
            return _corsify_actual_response(jsonify({"error": "No HTML content provided"}), 400)
        for i in range(2):
            shopee = Shopee_extract(html_content)
            shopee.to_csv()
            # if os.path.exists(file_path):
            #     continue
            
            
            # with open(file_path, 'w', encoding='utf-8') as file:
            #     file.write(html_content)
            break
        
        return _corsify_actual_response(jsonify({"message": "HTML content saved successfully"}))

def _build_cors_preflight_response():
    response = jsonify()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True)
