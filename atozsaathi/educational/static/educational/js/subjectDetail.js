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
                    console.log(`Category ID: ${category.id}, Category Name: ${category.name}`);
                    const button = document.createElement('button');
                    button.innerText = category.name;
                    button.onclick = () => {
                        console.log(`Button clicked for category ID: ${category.id}`);
                        loadCategory(chapterId, category.id, button);
                    };
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

function loadCategory(chapterId, categoryId, button) {
    console.log(`Loading content for category: ${categoryId} in chapter: ${chapterId}`);
    // Implement the logic to load category content dynamically
    fetch(`/api/chapters/${chapterId}/content/${categoryId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Content data:', data);
            const contentDisplay = document.getElementById('content-display');
            contentDisplay.innerHTML = `<h2></h2>`;
            if (data.content && data.content.length > 0) {
                data.content.forEach((item, index) => {
                    console.log('Content item:', item); // Log each content item to verify its structure
                    const contentItem = document.createElement('div');
                    if (item.type && item.type.toLowerCase() === 'mcq') {
                        contentItem.classList.add('mcq-question');
                        contentItem.innerHTML = `
                            <p>Question ${index + 1}: ${item.question}</p>
                            <ul class="mcq-options">
                                <li data-label="A">${item.option1}</li>
                                <li data-label="B">${item.option2}</li>
                                <li data-label="C">${item.option3}</li>
                                <li data-label="D">${item.option4}</li>
                            </ul>
                            <p class="mcq-correct">Correct Option: ${item.correct_option}</p>
                        `;
                    } else if (item.type && item.type.toLowerCase() === 'short_answer') {
                        contentItem.innerHTML = `<p>Question ${index + 1}: ${item.question}</p><p>Answer: ${item.answer || 'N/A'}</p>`;
                    } else if (item.type && item.type.toLowerCase() === 'detailed_answer') {
                        contentItem.innerHTML = `<p>Question ${index + 1}: ${item.question}</p><p>Detailed Answer: ${item.detailed_answer || 'N/A'}</p>`;
                    } else {
                        contentItem.innerHTML = `<p>Question ${index + 1}: ${item.question}</p><p>Answer: ${item.answer || 'N/A'}</p>`;
                    }
                    contentDisplay.appendChild(contentItem);
                });
            } else {
                contentDisplay.innerHTML += '<p>No content available for this category.</p>';
            }
            
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