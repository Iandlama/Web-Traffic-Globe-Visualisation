from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
packages = []


""" @app.route('/')
def index():
    return render_template('visual.html')
 """


@app.route('/package', methods=['GET'])
def receive_package():
    import json
    data_str = request.args.get('data')
    if not data_str:
        return jsonify({"error": "Missing 'data' parameter"}), 400

    data = json.loads(data_str)

    data['suspicious'] = int(float(data['suspicious']))

    packages.append(data)
    print(f"📦 Received: {data['ip']} (total: {len(packages)})")
    return jsonify({"status": "ok"}), 200


@app.route('/packages', methods=['GET'])
def get_packages():
    return jsonify(packages)


if __name__ == '__main__':
    print("🚀 Flask server starting on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
