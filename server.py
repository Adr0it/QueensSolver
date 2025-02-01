from flask import Flask, request, jsonify, send_from_directory
from queens import solveMatrix
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'queens.html')

# Serve static files like style.css and queens.js from the 'static' folder
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'static'), filename)

@app.route('/solve', methods=['POST'])
def solve():
    try:
        # Get JSON data from request
        matrix = request.json  # This is your 2D array
        print("Received Data:", matrix)

        # Solve the matrix
        result = solveMatrix(matrix, len(matrix[0]))

        # Return JSON response
        return jsonify({"solved": result})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
