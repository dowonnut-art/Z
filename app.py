

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Super Mario Adventure",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp {
        background: #16213e;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 0;
        max-width: 1200px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🍄 Super Mario Adventure")
st.caption("A five-level platform adventure built with Streamlit, HTML, CSS and JavaScript.")

game_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #16213e;
    color: white;
    text-align: center;
}

h1 {
    color: #ffdf40;
    text-shadow: 3px 3px #a83232;
    margin: 12px;
}

.subtitle {
    color: #dce7ff;
    margin-bottom: 15px;
}

.hud {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    margin: 12px;
}

.hud div {
    background: #243b65;
    border: 2px solid white;
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 16px;
    font-weight: bold;
}

canvas {
    display: block;
    margin: auto;
    background: #70c5ff;
    border: 5px solid white;
    border-radius: 10px;
    width: 100%;
    max-width: 850px;
    height: auto;
}

button {
    background: #e63946;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    margin: 12px 5px;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #ff6975;
}

#overlay {
    position: fixed;
    inset: 0;
    display: none;
    align-items: center;
    justify-content: center;
    background: rgba(0,0,0,0.78);
    z-index: 10;
}

.panel {
    background: #243b65;
    border: 4px solid #ffdf40;
    border-radius: 18px;
    padding: 30px;
    width: min(90%, 420px);
}

.panel h2 {
    color: #ffdf40;
    font-size: 28px;
}

.instructions {
    margin: 15px;
    color: #e0eaff;
    line-height: 1.8;
}

.progress {
    width: 90%;
    max-width: 500px;
    height: 15px;
    background: #34435d;
    border-radius: 20px;
    margin: 10px auto;
    overflow: hidden;
}

#progressBar {
    height: 100%;
    width: 0%;
    background: #ffdf40;
    transition: width 0.3s;
}

#status {
    color: #ffdf40;
    font-weight: bold;
    min-height: 24px;
}

.mobile-controls {
    display: none;
    justify-content: center;
    gap: 15px;
    margin: 12px;
}

.mobile-controls button {
    width: 65px;
    height: 55px;
    padding: 5px;
    font-size: 23px;
    touch-action: none;
}

@media (max-width: 600px) {
    .mobile-controls {
        display: flex;
    }

    .hud div {
        font-size: 13px;
        padding: 8px;
    }
}
</style>
</head>

<body>

<h1>🍄 SUPER MARIO ADVENTURE 🍄</h1>

<p class="subtitle">
Collect coins, overcome obstacles and complete all five levels!
</p>

<div class="hud">
    <div>🌎 Level: <span id="level">1</span>/5</div>
    <div>⭐ Score: <span id="score">0</span></div>
    <div>❤️ Lives: <span id="lives">3</span></div>
    <div>🪙 Coins: <span id="coinCount">0</span>/<span id="coinTotal">3</span></div>
</div>

<div class="progress">
    <div id="progressBar"></div>
</div>

<canvas id="gameCanvas" width="850" height="450"></canvas>

<p id="status">Collect every coin to unlock the exit!</p>

<div>
    <button onclick="restartGame()">🔄 Restart Game</button>
</div>

<div class="mobile-controls">
    <button id="leftButton">⬅️</button>
    <button id="jumpButton">⬆️</button>
    <button id="rightButton">➡️</button>
</div>

<div class="instructions">
    <b>Controls</b><br>
    ← → Move | SPACE Jump<br>
    Collect every coin to unlock the exit!<br>
    Avoid enemies and don't fall off platforms.
</div>

<div id="overlay">
    <div class="panel">
        <h2 id="overlayTitle">Level Complete!</h2>
        <p id="overlayMessage"></p>
        <button id="overlayButton" onclick="overlayAction()">
            Continue
        </button>
    </div>
</div>

<script>

// ===================================
// GAME INITIALIZATION
// ===================================

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const TOTAL_LEVELS = 5;

let level = 1;
let score = 0;
let lives = 3;

let gameRunning = true;
let gameState = "playing";
let invulnerable = 0;
let animationId = null;

const gravity = 0.65;

const keys = {};

const player = {
    x: 40,
    y: 300,
    width: 30,
    height: 40,
    speed: 5,
    velocityY: 0,
    jumpPower: -13,
    grounded: false
};

let platforms = [];
let coins = [];
let enemies = [];

// ===================================
// FIVE LEVELS
// ===================================

const levelData = [

    {
        name: "Green Hills",
        enemySpeed: 1.5,

        coins: [
            [220, 285],
            [410, 225],
            [640, 165]
        ],

        platforms: [
            [0,410,850,40],
            [170,330,130,15],
            [370,270,120,15],
            [570,210,140,15]
        ],

        enemies: [
            [350,380],
            [680,380]
        ]
    },

    {
        name: "Mushroom Forest",
        enemySpeed: 2.2,

        coins: [
            [150,350],
            [260,285],
            [440,225],
            [640,165]
        ],

        platforms: [
            [0,410,850,40],
            [110,365,90,15],
            [220,310,100,15],
            [390,250,110,15],
            [590,195,100,15]
        ],

        enemies: [
            [250,380],
            [480,380],
            [700,380]
        ]
    },

    {
        name: "Desert Challenge",
        enemySpeed: 2.8,

        coins: [
            [120,330],
            [270,270],
            [440,210],
            [600,150],
            [760,330]
        ],

        platforms: [
            [0,410,850,40],
            [80,350,85,15],
            [230,295,85,15],
            [400,235,85,15],
            [560,175,90,15],
            [720,350,85,15]
        ],

        enemies: [
            [180,380],
            [390,380],
            [590,380],
            [740,380]
        ]
    },

    {
        name: "Lava Castle",
        enemySpeed: 3.3,

        coins: [
            [130,320],
            [290,250],
            [460,190],
            [630,130],
            [770,320]
        ],

        platforms: [
            [0,410,850,40],
            [90,345,75,15],
            [250,275,75,15],
            [420,215,75,15],
            [590,155,75,15],
            [740,345,75,15]
        ],

        enemies: [
            [140,380],
            [330,380],
            [510,380],
            [680,380],
            [790,380]
        ]
    },

    {
        name: "Final Boss Challenge",
        enemySpeed: 4,

        coins: [
            [100,320],
            [250,260],
            [400,200],
            [550,140],
            [700,200],
            [800,320]
        ],

        platforms: [
            [0,410,850,40],
            [60,350,70,15],
            [210,290,75,15],
            [360,230,75,15],
            [510,170,75,15],
            [660,230,75,15],
            [770,350,75,15]
        ],

        enemies: [
            [110,380],
            [280,380],
            [450,380],
            [620,380],
            [770,380]
        ]
    }

];

// ===================================
// LOAD LEVEL
// ===================================

function loadLevel(number) {

    level = number;

    const data = levelData[level - 1];

    platforms = data.platforms.map(p => ({
        x: p[0],
        y: p[1],
        width: p[2],
        height: p[3]
    }));

    coins = data.coins.map(c => ({
        x: c[0],
        y: c[1],
        collected: false
    }));

    enemies = data.enemies.map((e, index) => ({
        x: e[0],
        y: e[1],
        width: 30,
        height: 30,
        speed: data.enemySpeed,
        direction: index % 2 === 0 ? 1 : -1,
        startX: e[0],
        minX: Math.max(0, e[0] - 65),
        maxX: Math.min(820, e[0] + 65)
    }));

    player.x = 40;
    player.y = 300;
    player.velocityY = 0;
    player.grounded = false;

    invulnerable = 90;

    gameState = "playing";
    gameRunning = true;

    document.getElementById("overlay").style.display = "none";

    updateHUD();

    document.getElementById("status").textContent =
        data.name + " - Collect all coins!";
}

// ===================================
// INPUT
// ===================================

document.addEventListener("keydown", e => {

    if (["ArrowLeft", "ArrowRight", "Space"].includes(e.code)) {
        e.preventDefault();
    }

    keys[e.code] = true;

});

document.addEventListener("keyup", e => {
    keys[e.code] = false;
});

// Mobile controls
function bindButton(id, key) {

    const button = document.getElementById(id);

    button.addEventListener("pointerdown", e => {
        e.preventDefault();
        keys[key] = true;
    });

    ["pointerup", "pointerleave", "pointercancel"].forEach(event => {
        button.addEventListener(event, () => {
            keys[key] = false;
        });
    });
}

bindButton("leftButton", "ArrowLeft");
bindButton("rightButton", "ArrowRight");
bindButton("jumpButton", "Space");

// ===================================
// COLLISION
// ===================================

function isColliding(a, b) {

    return (
        a.x < b.x + b.width &&
        a.x + a.width > b.x &&
        a.y < b.y + b.height &&
        a.y + a.height > b.y
    );

}

// ===================================
// PLAYER MOVEMENT
// ===================================

function updatePlayer() {

    const previousBottom = player.y + player.height;

    if (keys["ArrowRight"]) {
        player.x += player.speed;
    }

    if (keys["ArrowLeft"]) {
        player.x -= player.speed;
    }

    if (keys["Space"] && player.grounded) {
        player.velocityY = player.jumpPower;
        player.grounded = false;
    }

    player.velocityY += gravity;
    player.y += player.velocityY;

    player.grounded = false;

    platforms.forEach(p => {

        const currentBottom = player.y + player.height;

        const horizontalOverlap =
            player.x + player.width > p.x &&
            player.x < p.x + p.width;

        const crossedPlatform =
            previousBottom <= p.y &&
            currentBottom >= p.y;

        if (
            horizontalOverlap &&
            crossedPlatform &&
            player.velocityY >= 0
        ) {

            player.y = p.y - player.height;
            player.velocityY = 0;
            player.grounded = true;

        }

    });

    player.x = Math.max(
        0,
        Math.min(canvas.width - player.width, player.x)
    );

    if (player.y > canvas.height) {
        loseLife();
    }

}

// ===================================
// COINS
// ===================================

function updateCoins() {

    coins.forEach(c => {

        if (c.collected) return;

        const coinBox = {
            x: c.x - 10,
            y: c.y - 10,
            width: 20,
            height: 20
        };

        if (isColliding(player, coinBox)) {

            c.collected = true;
            score += 10;

            updateHUD();

        }

    });

    if (coins.every(c => c.collected)) {
        showLevelComplete();
    }

}

// ===================================
// ENEMIES
// ===================================

function updateEnemies() {

    enemies.forEach(e => {

        e.x += e.speed * e.direction;

        if (e.x <= e.minX || e.x >= e.maxX) {
            e.direction *= -1;
        }

        if (invulnerable > 0) return;

        if (isColliding(player, e)) {

            const playerWasAbove =
                player.y + player.height - player.velocityY <= e.y + 8;

            if (
                player.velocityY > 0 &&
                playerWasAbove
            ) {

                e.x = -100;
                player.velocityY = -8;

                score += 20;
                updateHUD();

            } else {

                loseLife();

            }

        }

    });

}

// ===================================
// LOSE LIFE
// ===================================

function loseLife() {

    if (gameState !== "playing") return;

    lives--;

    updateHUD();

    player.x = 40;
    player.y = 300;
    player.velocityY = 0;

    invulnerable = 90;

    if (lives <= 0) {

        gameState = "gameOver";
        gameRunning = false;

        showOverlay(
            "💔 GAME OVER",
            "You ran out of lives! Final score: " + score,
            "Play Again"
        );

    }

}

// ===================================
// HUD
// ===================================

function updateHUD() {

    const collected = coins.filter(c => c.collected).length;

    document.getElementById("level").textContent = level;
    document.getElementById("score").textContent = score;
    document.getElementById("lives").textContent = lives;
    document.getElementById("coinCount").textContent = collected;
    document.getElementById("coinTotal").textContent = coins.length;

    document.getElementById("progressBar").style.width =
        (collected / coins.length * 100) + "%";

}

// ===================================
// DRAW PLAYER
// ===================================

function drawPlayer() {

    // Flicker while temporarily protected
    if (invulnerable > 0 && Math.floor(invulnerable / 8) % 2 === 0) {
        return;
    }

    ctx.fillStyle = "#e63946";
    ctx.fillRect(player.x, player.y, 30, 12);

    ctx.fillStyle = "#ffcc99";
    ctx.fillRect(player.x + 5, player.y + 12, 20, 13);

    ctx.fillStyle = "#111";
    ctx.fillRect(player.x + 19, player.y + 16, 3, 3);

    ctx.fillStyle = "#2563eb";
    ctx.fillRect(player.x + 4, player.y + 25, 22, 15);

    ctx.fillStyle = "#5b2c1b";
    ctx.fillRect(player.x + 2, player.y + 37, 12, 3);
    ctx.fillRect(player.x + 17, player.y + 37, 12, 3);

}

// ===================================
// DRAW PLATFORMS
// ===================================

function drawPlatforms() {

    platforms.forEach(p => {

        ctx.fillStyle = "#8b4513";
        ctx.fillRect(p.x, p.y, p.width, p.height);

        ctx.fillStyle = "#38a169";
        ctx.fillRect(p.x, p.y, p.width, 5);

    });

}

// ===================================
// DRAW COINS
// ===================================

function drawCoins() {

    coins.forEach(c => {

        if (!c.collected) {

            ctx.beginPath();

            ctx.fillStyle = "#ffdf40";
            ctx.arc(c.x, c.y, 10, 0, Math.PI * 2);
            ctx.fill();

            ctx.strokeStyle = "#d69e00";
            ctx.lineWidth = 2;
            ctx.stroke();

        }

    });

}

// ===================================
// DRAW ENEMIES
// ===================================

function drawEnemies() {

    enemies.forEach(e => {

        if (e.x < -50) return;

        ctx.fillStyle = "#8b4513";
        ctx.fillRect(e.x, e.y, e.width, e.height);

        ctx.fillStyle = "white";
        ctx.fillRect(e.x + 5, e.y + 7, 7, 7);
        ctx.fillRect(e.x + 19, e.y + 7, 7, 7);

        ctx.fillStyle = "black";
        ctx.fillRect(e.x + 8, e.y + 9, 3, 3);
        ctx.fillRect(e.x + 22, e.y + 9, 3, 3);

    });

}

// ===================================
// DRAW EXIT
// ===================================

function drawExit() {

    const unlocked = coins.every(c => c.collected);

    ctx.fillStyle = unlocked ? "#20c997" : "#777";
    ctx.fillRect(795, 340, 35, 70);

    ctx.fillStyle = "white";
    ctx.font = "13px Arial";

    ctx.fillText(
        unlocked ? "OPEN" : "LOCKED",
        785,
        330
    );

    ctx.fillStyle = unlocked ? "#ffdf40" : "#aaa";

    ctx.beginPath();
    ctx.arc(812, 375, 5, 0, Math.PI * 2);
    ctx.fill();

}

// ===================================
// BACKGROUND
// ===================================

function drawBackground() {

    ctx.fillStyle = "#70c5ff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "white";

    [100, 400, 680].forEach(x => {

        ctx.beginPath();
        ctx.arc(x, 75, 22, 0, Math.PI * 2);
        ctx.arc(x + 28, 75, 28, 0, Math.PI * 2);
        ctx.arc(x + 55, 75, 22, 0, Math.PI * 2);
        ctx.fill();

    });

    ctx.fillStyle = "#48b66a";

    ctx.beginPath();
    ctx.arc(200, 450, 100, Math.PI, 0);
    ctx.fill();

    ctx.beginPath();
    ctx.arc(650, 450, 130, Math.PI, 0);
    ctx.fill();

}

// ===================================
// DRAW
// ===================================

function draw() {

    drawBackground();
    drawPlatforms();
    drawExit();
    drawCoins();
    drawEnemies();
    drawPlayer();

}

// ===================================
// LEVEL COMPLETION
// ===================================

function showLevelComplete() {

    if (gameState !== "playing") return;

    gameState = "levelComplete";
    gameRunning = false;

    if (level === TOTAL_LEVELS) {

        showOverlay(
            "🏆 YOU WIN!",
            "Congratulations! You completed all five levels! Final score: " + score,
            "Play Again"
        );

    } else {

        showOverlay(
            "⭐ LEVEL " + level + " COMPLETE!",
            "Excellent! You collected every coin. Score: " + score,
            "Next Level"
        );

    }

}

// ===================================
// OVERLAY
// ===================================

function showOverlay(title, message, buttonText) {

    document.getElementById("overlayTitle").textContent = title;
    document.getElementById("overlayMessage").textContent = message;
    document.getElementById("overlayButton").textContent = buttonText;

    document.getElementById("overlay").style.display = "flex";

}

function overlayAction() {

    document.getElementById("overlay").style.display = "none";

    if (
        gameState === "gameOver" ||
        level === TOTAL_LEVELS
    ) {

        restartGame();

    } else if (gameState === "levelComplete") {

        loadLevel(level + 1);

        gameRunning = true;

        gameLoop();

    }

}

// ===================================
// RESTART
// ===================================

function restartGame() {

    if (animationId !== null) {
        cancelAnimationFrame(animationId);
    }

    score = 0;
    lives = 3;

    loadLevel(1);

    gameRunning = true;

    gameLoop();

}

// ===================================
// MAIN GAME LOOP
// ===================================

function gameLoop() {

    if (!gameRunning) return;

    if (invulnerable > 0) {
        invulnerable--;
    }

    updatePlayer();

    if (gameState === "playing") {
        updateCoins();
    }

    if (gameState === "playing") {
        updateEnemies();
    }

    draw();

    if (gameRunning) {
        animationId = requestAnimationFrame(gameLoop);
    }

}

// ===================================
// START GAME
// ===================================

loadLevel(1);
draw();
gameLoop();

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=850,
    scrolling=False
)

st.caption(
    "Super Mario Adventure | 5 Levels | HTML + CSS + JavaScript + Streamlit"
)
