import os
from flask import Flask, jsonify, render_template, request
from scraper import get_rating_and_rank
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mmr', methods=['GET'])
def fetch_mmr():
    player = request.args.get('player')
    leaderboard = request.args.get('leaderboard', 'D7D6u-')

    if not player:
        return jsonify({"error": "Aucun joueur spécifié"}), 400

    rating, rank = get_rating_and_rank(player, leaderboard)
    return jsonify({"player": player, "rating": rating, "rank": rank})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
