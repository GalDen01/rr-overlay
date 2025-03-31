let isAutoRefreshing = false;

function startAutoRefresh(player, leaderboard) {
    if (!isAutoRefreshing) {
        isAutoRefreshing = true;
        setInterval(() => {
            console.log(`Refreshing MMR for ${player}`);
            fetchMMR(player, leaderboard);
        }, 60000); 
    }
}


function updateMMR() {
    let player = document.getElementById("player").value.trim();
    let leaderboard = document.getElementById("leaderboard").value;

    if (player) {
        fetchMMR(player, leaderboard);
    } else {
        alert("Please enter a player name.");
    }
}

async function fetchMMR(player, leaderboard) {
    let loadingSpinner = document.getElementById("loading");
    let mmrContainer = document.getElementById("mmr-container");
    let rankImg = document.getElementById("rank-img");
    let rankText = document.getElementById("rank");

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
            rankText.style.display = "block";
            rankImg.onclick = () => window.location.href = `/mmr?player=${encodeURIComponent(player)}&leaderboard=${encodeURIComponent(leaderboard)}`;
        } else {
            rankImg.src = "";
            rankImg.style.display = "none";
            rankText.style.display = "none";
        }

        mmrContainer.style.display = "block";

        startAutoRefresh(player, leaderboard);

    } catch (error) {
        console.error("Error fetching MMR:", error);
    } finally {
        loadingSpinner.style.display = "none";
    }
}