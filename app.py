from flask import Flask, jsonify, request
from scraper import get_rating_and_rank  # ✅ Import corrigé
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["http://127.0.0.1:5500", "https://galden01.github.io"])
@app.route('/mmr', methods=['GET'])
def fetch_mmr():
    player = request.args.get('player')
    if not player:
        return jsonify({"error": "Aucun joueur spécifié"}), 400

    rating, rank = get_rating_and_rank(player)
    return jsonify({"player": player, "rating": rating, "rank": rank})  # ✅ On renvoie aussi le rang

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
