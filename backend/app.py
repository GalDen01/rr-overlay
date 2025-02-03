from flask import Flask, jsonify, request
from scraper import get_rating
import os
import signal

app = Flask(__name__)

@app.route('/mmr', methods=['GET'])
def fetch_mmr():
    player = request.args.get('player')
    if not player:
        return jsonify({"error": "Aucun joueur spécifié"}), 400

    rating = get_rating(player)
    return jsonify({"player": player, "rating": rating})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)  # Envoie un signal d'arrêt au processus actuel
    return 'Arrêt du serveur...'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
