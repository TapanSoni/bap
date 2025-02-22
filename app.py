from flask import Flask, render_template, jsonify, request
from Crypto.Util import number
from concurrent.futures import ThreadPoolExecutor
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
executor = ThreadPoolExecutor(max_workers=4)  # Allow parallel processing

def generate_large_prime(bits):
    return number.getPrime(bits)  # Optimized prime generation

@app.route('/')
def home():
    """Serve the main HTML page."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        bits = int(data.get("bits", 2048))  # Default to 2048 bits
        if bits not in [2048, 4096, 8192]:
            return jsonify({"error": "Invalid bit size. Choose 2048, 4096, or 8192."}), 400
        
        future = executor.submit(generate_large_prime, bits)
        prime = future.result()
        
        return jsonify({"prime": str(prime)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template, request, jsonify
# import random
# from sympy import randprime

# app = Flask(__name__)

# def generate_large_prime(bits):
#     """Generate a large prime number with the specified number of bits."""
#     lower_bound = 2**(bits - 1)
#     upper_bound = 2**bits - 1
#     return randprime(lower_bound, upper_bound)

# @app.route('/')
# def home():
#     """Serve the main HTML page."""
#     return render_template('index.html')

# @app.route('/generate_prime', methods=['GET'])
# def generate_prime():
#     """Generate a cryptographically secure prime number."""
#     size = request.args.get('size', default=2048, type=int)
#     if size not in [2048, 4096, 8192]:
#         return jsonify({"error": "Invalid key size"}), 400

#     prime = generate_large_prime(size)
#     return jsonify({"prime": str(prime)})

# if __name__ == '__main__':
#     app.run(debug=True)
