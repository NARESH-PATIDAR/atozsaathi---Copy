function loadChapter(chapterId) {
    console.log(`Loading categories for chapter: ${chapterId}`);
    // Fetch and display the content categories for the selected chapter
    fetch(`/api/chapters/${chapterId}/categories/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Categories data:', data);
            const contentCategories = document.getElementById('content-categories');
            contentCategories.innerHTML = ''; // Clear previous categories
            if (data.categories && data.categories.length > 0) {
                data.categories.forEach(category => {
                    const button = document.createElement('button');
                    button.innerText = category.name;
                    button.onclick = () => loadCategory(chapterId, category.name, button);
                    contentCategories.appendChild(button);
                });
            } else {
                contentCategories.innerHTML = '<p>No categories available for this chapter.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching categories:', error);
            const contentCategories = document.getElementById('content-categories');
            contentCategories.innerHTML = '<p>Error loading categories. Please try again later.</p>';
        });
}

function loadCategory(chapterId, category, button) {
    console.log(`Loading content for category: ${category} in chapter: ${chapterId}`);
    // Implement the logic to load category content dynamically
    fetch(`/api/chapters/${chapterId}/content/${category}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Content data:', data);
            const contentDisplay = document.getElementById('content-display');
            contentDisplay.innerHTML = `<h2>${category}</h2><p>${data.content}</p>`;
            
            // Highlight the active category button
            const buttons = document.querySelectorAll('.nav-bar button');
            buttons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
        })
        .catch(error => {
            console.error('Error fetching content:', error);
            const contentDisplay = document.getElementById('content-display');
            contentDisplay.innerHTML = '<p>Error loading content. Please try again later.</p>';
        });
}