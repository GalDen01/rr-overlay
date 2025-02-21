function updateMMR() {
    let player = document.getElementById("player").value.trim();
    let leaderboard = document.getElementById("leaderboard").value;

    if (!player) {
        alert("Please enter a player name.");
        return;
    }

    let messageElement = document.getElementById("message");
    if (messageElement) {
        messageElement.style.display = "none";
    }

    fetchMMR(player, leaderboard);
}

async function fetchMMR(player, leaderboard) {
    let loadingSpinner = document.getElementById("loading");
    let mmrContainer = document.getElementById("mmr-container");
    let rankImg = document.getElementById("rank-img");

    loadingSpinner.style.display = "block";
    mmrContainer.style.display = "none";

    try {
        let response = await fetch(`/mmr?player=${encodeURIComponent(player)}&leaderboard=${leaderboard}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });
        let data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById("mmr").textContent = `MMR : ${data.rating}`;

        if (data.rank) {
            let rankLower = data.rank.toLowerCase();
            rankImg.src = `https://raw.githubusercontent.com/GalDen01/rr-overlay/refs/heads/main/media/ranks/${rankLower}.png`;
            rankImg.alt = data.rank;
            rankImg.onclick = () => window.location.href = `/mmr?player=${encodeURIComponent(player)}&leaderboard=${leaderboard}`;
        } else {
            rankImg.src = "";
            rankImg.style.display = "none";
        }

        mmrContainer.style.display = "block";

    } catch (error) {
        console.error("Error fetching MMR:", error);
    } finally {
        loadingSpinner.style.display = "none";
    }
}