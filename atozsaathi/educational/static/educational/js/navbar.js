function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active'); // Toggle 'active' class to show/hide menu
}

function toggleSearch() {
    const searchBar = document.querySelector('.search-bar-container');
    searchBar.classList.toggle('active'); // Toggle visibility of search bar

    // Toggle the visibility of the search input
    const searchInput = document.querySelector('.input');
    searchInput.classList.toggle('active'); // Show the input field when search is toggled
}
