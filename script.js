// Fonction pour récupérer les paramètres de l'URL
function getQueryParam(param) {
    let params = new URLSearchParams(window.location.search);
    return params.get(param);
}

// Récupérer le pseudo depuis l'URL
let player = getQueryParam("player");

// Si aucun pseudo n'est fourni, afficher un message d'instruction
if (!player) {
    document.getElementById("message").style.display = "block";  // Afficher le message
    document.querySelector(".overlay").style.display = "none";  // Cacher l'overlay
} else {
    document.getElementById("message").style.display = "none";  // Cacher le message
    fetchMMR(player);  // Charger les données du joueur
}

async function fetchMMR(player) {
    try {
        let response = await fetch(`http://localhost:5001/mmr?player=${player}`);
        let data = await response.json();

        document.getElementById("mmr").textContent = `MMR : ${data.rating}`;

        // Mise à jour de l'image de rang
        let rankImg = document.getElementById("rank-img");
        if (data.rank) {
            rankImg.src = `github.com/GalDen01/rr-overlay/blob/main/media/ranks/${data.rank}.png`;
            rankImg.alt = data.rank;
        } else {
            rankImg.src = "";  // Mettre une image par défaut si nécessaire
        }

    } catch (error) {
        console.error("Erreur de récupération du MMR :", error);
    }
}

// Rafraîchir toutes les 60 secondes
setInterval(() => {
    if (player) fetchMMR(player);
}, 60000);
