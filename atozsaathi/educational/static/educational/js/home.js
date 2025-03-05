function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}


 
    document.addEventListener('DOMContentLoaded', () => {

        const searchInputElement = document.getElementById('search-input-home');
        const placeholderText = ["RBSE", "CBSE", "Compititive Exams", "Explore history"];

        let currentIndex = 0;
        let currentCharIndex = 0;

        function typewriterEffect() {
            if (currentCharIndex < placeholderText[currentIndex].length) {
                searchInputElement.setAttribute("placeholder", placeholderText[currentIndex].substring(0, currentCharIndex + 1));
                currentCharIndex++;
                setTimeout(typewriterEffect, 100);
            } else {
                setTimeout(() => {
                    currentIndex = (currentIndex + 1) % placeholderText.length;
                    currentCharIndex = 0;
                    typewriterEffect();
                }, 2000);
            }
        }

        typewriterEffect();
    });
