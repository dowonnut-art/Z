
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Super Mario Game",
    page_icon="🍄",
    layout="wide"
)

# HTML + CSS + JavaScript game
game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        font-family: Arial, sans-serif;
        background: #70c5ff;
        overflow: hidden;
    }

    .game-container {
        width: 100%;
        text-align: center;
    }

    h1 {
        color: white;
        text-shadow: 3px 3px #333;
        margin: 10px;
    }

    #scoreboard {
        font-size: 22px;
        font-weight: bold;
        color: white;
        padding: 10px;
    }

    canvas {
        display: block;
        margin: auto;
        background: linear-gradient(#70c5ff 70%, #65c94b 70%);
        border: 5px solid white;
        border-radius: 10px;
        max-width: 100%;
    }

    button {
        background: #e63946;
        color: white;
        padding: 12px 25px;
        border: none;
        border-radius: 8px;
        font-size: 18px;
        cursor: pointer;
        margin: 10px;
    }

    button:hover {
        background: #b91c2c;
    }

    .instructions {
        color: white;
        font-size: 16px;
        margin: 10px;
    }
</style>
</head>

<body>
<div class="game-container">

    <h1>🍄 SUPER MARIO GAME 🍄</h1>

    <div id="scoreboard">
        Score: <span id="score">0</span>
        |
        Lives: <span id="lives">3</span>
    </div>

    <canvas id="gameCanvas" width="850" height="450"></canvas>

    <button onclick="restartGame()">Restart Game</button>

    <div class="instructions">
        ← → Move | SPACE Jump
        <br>
        Collect coins and avoid enemies!
    </div>

</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let score = 0;
let lives = 3;
let gameRunning = true;

const keys = {};

const player = {
    x: 50,
    y: 300,
    width: 30,
    height: 40,
    speed: 5,
    velocityY: 0,
    jumpPower: -13,
    grounded: false
};

const gravity = 0.6;

const platforms = [
    {x: 0, y: 410, width: 850, height: 40},
    {x: 180, y: 330, width: 120, height: 15},
    {x: 370, y: 270, width: 120, height: 15},
    {x: 570, y: 210, width: 130, height: 15}
];

let coins = [
    {x: 220, y: 290, collected: false},
    {x: 410, y: 230, collected: false},
    {x: 620, y: 170, collected: false},
    {x: 750, y: 370, collected: false}
];

let enemies = [
    {x: 350, y: 380, width: 30, height: 30, speed: 2},
    {x: 650, y: 380, width: 30, height: 30, speed: -2}
];

document.addEventListener("keydown", e => {
    keys[e.code] = true;

    if (["ArrowLeft", "ArrowRight", "Space"].includes(e.code)) {
        e.preventDefault();
    }
});

document.addEventListener("keyup", e => {
    keys[e.code] = false;
});

function drawPlayer() {
    // Mario-inspired character
    ctx.fillStyle = "#e63946";
    ctx.fillRect(player.x, player.y, 30, 12);

    ctx.fillStyle = "#f5c28b";
    ctx.fillRect(player.x + 5, player.y + 12, 20, 13);

    ctx.fillStyle = "#2563eb";
    ctx.fillRect(player.x + 4, player.y + 25, 22, 15);

    ctx.fillStyle = "#111";
    ctx.fillRect(player.x + 19, player.y + 16, 3, 3);
}

function drawPlatforms() {
    platforms.forEach(p => {
        ctx.fillStyle = "#8b4513";
        ctx.fillRect(p.x, p.y, p.width, p.height);

        ctx.fillStyle = "#38a169";
        ctx.fillRect(p.x, p.y, p.width, 5);
    });
}

function drawCoins() {
    coins.forEach(c => {
        if (!c.collected) {
            ctx.beginPath();
            ctx.fillStyle = "gold";
            ctx.arc(c.x, c.y, 10, 0, Math.PI * 2);
            ctx.fill();

            ctx.strokeStyle = "#d69e00";
            ctx.stroke();
        }
    });
}

function drawEnemies() {
    enemies.forEach(e => {
        ctx.fillStyle = "#8b4513";
        ctx.fillRect(e.x, e.y, e.width, e.height);

        ctx.fillStyle = "white";
        ctx.fillRect(e.x + 5, e.y + 7, 7, 7);
        ctx.fillRect(e.x + 19, e.y + 7, 7, 7);
    });
}

function updatePlayer() {
    if (keys["ArrowRight"]) player.x += player.speed;
    if (keys["ArrowLeft"]) player.x -= player.speed;

    if (keys["Space"] && player.grounded) {
        player.velocityY = player.jumpPower;
        player.grounded = false;
    }

    player.velocityY += gravity;
    player.y += player.velocityY;

    player.grounded = false;

    platforms.forEach(p => {
        if (
            player.x + player.width > p.x &&
            player.x < p.x + p.width &&
            player.y + player.height >= p.y &&
            player.y + player.height <= p.y + p.height + 15 &&
            player.velocityY >= 0
        ) {
            player.y = p.y - player.height;
            player.velocityY = 0;
            player.grounded = true;
        }
    });

    player.x = Math.max(0, Math.min(
        canvas.width - player.width, player.x
    ));

    if (player.y > canvas.height) {
        loseLife();
    }
}

function updateCoins() {
    coins.forEach(c => {
        if (!c.collected &&
            player.x < c.x + 10 &&
            player.x + player.width > c.x - 10 &&
            player.y < c.y + 10 &&
            player.y + player.height > c.y - 10
        ) {
            c.collected = true;
            score += 10;
            document.getElementById("score").textContent = score;
        }
    });
}

function updateEnemies() {
    enemies.forEach(e => {
        e.x += e.speed;

        if (e.x < 0 || e.x + e.width > canvas.width) {
            e.speed *= -1;
        }

        if (
            player.x < e.x + e.width &&
            player.x + player.width > e.x &&
            player.y < e.y + e.height &&
            player.y + player.height > e.y
        ) {
            loseLife();
        }
    });
}

function loseLife() {
    lives--;
    document.getElementById("lives").textContent = lives;

    player.x = 50;
    player.y = 300;
    player.velocityY = 0;

    if (lives <= 0) {
        gameRunning = false;
        alert("Game Over! Your score: " + score);
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Clouds
    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(150, 70, 25, 0, Math.PI * 2);
    ctx.arc(180, 70, 30, 0, Math.PI * 2);
    ctx.arc(210, 70, 25, 0, Math.PI * 2);
    ctx.fill();

    drawPlatforms();
    drawCoins();
    drawEnemies();
    drawPlayer();
}

function gameLoop() {
    if (!gameRunning) return;

    updatePlayer();
    updateCoins();
    updateEnemies();
    draw();

    requestAnimationFrame(gameLoop);
}

function restartGame() {
    score = 0;
    lives = 3;
    gameRunning = true;

    player.x = 50;
    player.y = 300;
    player.velocityY = 0;

    coins.forEach(c => c.collected = false);

    enemies[0].x = 350;
    enemies[0].speed = 2;
    enemies[1].x = 650;
    enemies[1].speed = -2;

    document.getElementById("score").textContent = 0;
    document.getElementById("lives").textContent = 3;

    gameLoop();
}

draw();
gameLoop();

</script>
</body>
</html>
"""

components.html(game_html, height=650, scrolling=False)
