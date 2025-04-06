function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}

document.addEventListener('DOMContentLoaded', () => {
    const searchInputElement = document.getElementById('search-input-home');
    const resultsContainer = document.getElementById('search-results-container');

    const placeholderText = ["RBSE", "CBSE", "Competitive Exams", "Explore history"];
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

    // Live search AJAX
    searchInputElement.addEventListener('input', function () {
        const query = this.value.trim();

        if (query.length === 0) {
            resultsContainer.classList.add('hidden');
            resultsContainer.innerHTML = '';
            return;
        }

        fetch(`/search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = '';

                if (data.results.length === 0) {
                    resultsContainer.innerHTML = `<div class="search-result-item">No results found</div>`;
                } else {
                    data.results.forEach(item => {
                        const div = document.createElement('div');
                        div.classList.add('search-result-item');
                        div.textContent = item.display;
                        div.addEventListener('click', () => {
                            window.location.href = item.url;
                        });
                        resultsContainer.appendChild(div);
                    });
                }

                resultsContainer.classList.remove('hidden');
            });
    });

    document.addEventListener('click', function (event) {
        if (!resultsContainer.contains(event.target) && event.target !== searchInputElement) {
            resultsContainer.classList.add('hidden');
        }
    });
});
