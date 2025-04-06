// Toggle Mobile Menu (if applicable)
function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}

const homeQuotes = [
    "\"Education is the key to unlocking the world, a passport to freedom.\" – Oprah Winfrey",
    "\"The roots of education are bitter, but the fruit is sweet.\" – Aristotle",
    "\"Education is the most powerful weapon which you can use to change the world.\" – Nelson Mandela",
    "\"Develop a passion for learning. If you do, you will never cease to grow.\" – Anthony J. D'Angelo",
    "\"The mind is not a vessel to be filled, but a fire to be kindled.\" – Plutarch"
];

let quoteIndex = 0;
const homeText = document.getElementById('home-quote');

function rotateHomeQuote() {
    homeText.style.opacity = 0;
    setTimeout(() => {
        quoteIndex = (quoteIndex + 1) % homeQuotes.length;
        homeText.textContent = homeQuotes[quoteIndex];
        homeText.style.opacity = 1;
    }, 500);
}

setInterval(rotateHomeQuote, 6000); // Change quote every 6 seconds
