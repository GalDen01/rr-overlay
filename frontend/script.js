// Fonction pour récupérer les paramètres de l'URL
function getQueryParam(param) {
    let params = new URLSearchParams(window.location.search);
    return params.get(param);
}

// Récupérer le pseudo depuis l'URL
let player = getQueryParam("player") || "steph";  // Valeur par défaut : "steph"

async function fetchMMR(player) {
    try {
        let response = await fetch(`http://localhost:5000/mmr?player=${player}`);
        let data = await response.json();

        document.getElementById("player-name").textContent = `Joueur : ${data.player}`;
        document.getElementById("mmr").textContent = `MMR : ${data.rating}`;

        // Mise à jour de l'image de rang
        let rankImg = document.getElementById("rank-img");
        if (data.rank) {
            rankImg.src = `media/ranks/${data.rank}.png`;  // ✅ Assure-toi que le nom du fichier est identique
            rankImg.alt = data.rank;
        } else {
            rankImg.src = "";  // Mettre une image par défaut si nécessaire
        }

    } catch (error) {
        console.error("Erreur de récupération du MMR :", error);
    }
}

// Charger le MMR dès le chargement de la page
fetchMMR(player);

// Rafraîchir toutes les 10 secondes
setInterval(() => fetchMMR(player), 10000);
