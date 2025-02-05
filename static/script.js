function getQueryParam(param) {
    let params = new URLSearchParams(window.location.search);
    return params.get(param);
}

let player = getQueryParam("player");

if (!player) {
    document.getElementById("message").style.display = "block";
    document.querySelector(".overlay").style.display = "none";
} else {
    document.getElementById("message").style.display = "none";
    fetchMMR(player);
}

async function fetchMMR(player) {
    try {
        let response = await fetch(`/mmr?player=${player}`);
        let data = await response.json();

        document.getElementById("mmr").textContent = `MMR : ${data.rating}`;

        let rankImg = document.getElementById("rank-img");
        if (data.rank) {
            let rankLower = data.rank.toLowerCase();
            rankImg.src = `https://raw.githubusercontent.com/GalDen01/rr-overlay/refs/heads/main/media/ranks/${rankLower}.png`;
            rankImg.alt = data.rank;
        } else {
            rankImg.src = "";
        }

    } catch (error) {
        console.error("Erreur de récupération du MMR :", error);
    }
}

setInterval(() => {
    if (player) fetchMMR(player);
}, 60000);
