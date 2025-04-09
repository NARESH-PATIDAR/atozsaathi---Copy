function loadChapter(chapterId) {
    console.log(`Loading categories for chapter: ${chapterId}`);

    // 🔹 1. Highlight the active chapter button
    document.querySelectorAll('.mobile-chapter-nav button').forEach(btn => {
        btn.classList.remove('active');
    });

    const activeBtn = Array.from(document.querySelectorAll('.mobile-chapter-nav button'))
        .find(btn => btn.getAttribute('onclick')?.includes(chapterId));

    if (activeBtn) {
        activeBtn.classList.add('active');

        // 🔸 Optional: scroll into view for better UX
        activeBtn.scrollIntoView({ behavior: 'smooth', inline: 'center' });
    }

    // 🔹 2. Fetch and display the content categories
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
                        console.log(`Button clicked for category ID: ${category.id}, Category Name: ${category.name}`);
                        loadCategory(chapterId, category.id, category.name, button);
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



function loadCategory(chapterId, categoryId, categoryName, button) {
        console.log(`Loading content for category: ${categoryName} (ID: ${categoryId}) in chapter: ${chapterId}`);
    
        // If the category is "test", load google.com in an iframe
        if (categoryName.toLowerCase() === "test") {
            const contentDisplay = document.getElementById('content-display');
            contentDisplay.innerHTML = ''; // Clear previous content
    
            const iframe = document.createElement('iframe');
            iframe.src = "/static/educational/testInstruction.html";
            iframe.width = "100%";
            iframe.height = "600px";
            iframe.style.border = "none";
    
            contentDisplay.appendChild(iframe);

            fetch(`/api/chapters/${chapterId}/content/${categoryId}/`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                // Store the fetched data in the variable
                testCategoryData = data.content || [];  // Adjust the property if needed

                // Optionally log the data or use it elsewhere
                console.log('Fetched test category data:', testCategoryData);
            })
            .catch(error => {
                console.error('Error fetching test content:', error);
            });



            return;
        }

    
    fetch(`/api/chapters/${chapterId}/content/${categoryId}/`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            const contentDisplay = document.getElementById('content-display');
            contentDisplay.innerHTML = '';

            if (data.content?.length > 0) {
                data.content.forEach((item, index) => {
                    const contentItem = document.createElement('div');
                    contentItem.classList.add('content-item');

                    const questionHeader = `<h3 class="question-title">Q${index + 1}: ${item.question || item.title || ''}</h3>`;

                    switch ((item.type || '').toLowerCase()) {
                        case 'mcq':
                            contentItem.classList.add('mcq');
                            contentItem.innerHTML = `
                                ${questionHeader}
                                <ul class="mcq-options">
                                    <li>A. ${item.option1}</li>
                                    <li>B. ${item.option2}</li>
                                    <li>C. ${item.option3}</li>
                                    <li>D. ${item.option4}</li>
                                </ul>
                                <p class="answer">✅ Correct: ${item.correct_option}</p>
                            `;
                            break;
                        case 'short_answer':
                            contentItem.classList.add('short-answer');
                            contentItem.innerHTML = `
                                ${questionHeader}
                                <p class="answer">✍️ Answer: ${item.answer || 'N/A'}</p>
                            `;
                            break;
                        case 'detailed_answer':
                            contentItem.classList.add('detailed-answer');
                            contentItem.innerHTML = `
                                ${questionHeader}
                                <div class="answer detailed">${item.detailed_answer || 'N/A'}</div>
                            `;
                            break;
                        case 'true_or_false':
                            contentItem.classList.add('true-false');
                            const tf = item.is_true ? 'True ✅' : 'False ❌';
                            contentItem.innerHTML = `
                                ${questionHeader}
                                <p class="answer">${tf}</p>
                            `;
                            break;

                        case 'fill_in_the_blanks':
                            contentItem.classList.add('fill-blanks');
                            contentItem.innerHTML = `
                                ${questionHeader}
                                <p class="answer">📝 ${item.answer || 'N/A'}</p>
                            `;
                            break;
                        case 'notes':
                            contentItem.classList.add('notes');
                            contentItem.innerHTML = `
                                <h3 class="notes-title">🗒️ ${item.title}</h3>
                                <div class="notes-body">${item.content}</div>
                            `;
                            break;
                        case 'chapter_content':
                            contentItem.classList.add('chapter-file');
                            const file = item.file_url;
                            // if (file.endsWith('.pdf')) {
                            //     contentItem.innerHTML = `
                            //         <h3>${item.title}</h3>
                            //         <iframe src="https://docs.google.com/viewer?url=${encodeURIComponent(file)}&embedded=true" width="100%" height="600px"></iframe>
                            //     `;
                            
                            if (file.endsWith('.pdf')) {
                                contentItem.innerHTML = `<h3>${item.title}</h3><iframe src="${file}" width="100%" height="600px"></iframe>`;

                            } else if (file.endsWith('.docx')) {
                                contentItem.innerHTML = `
                                    <h3>${item.title}</h3>
                                    <iframe src="https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(file)}" width="100%" height="600px"></iframe>
                                `;
                            } else {
                                contentItem.innerHTML = `
                                    <h3>${item.title}</h3>
                                    <a href="${file}" target="_blank" class="download-link">📥 Download</a>
                                `;
                            }
                            break;
                        default:
                            contentItem.innerHTML = `
                                ${questionHeader}
                                <p class="answer">Answer: ${item.answer || 'N/A'}</p>
                            `;
                    }

                    contentDisplay.appendChild(contentItem);
                });
            } else {
                contentDisplay.innerHTML = '<p>No content available for this category.</p>';
            }

            // Highlight active button
            document.querySelectorAll('.nav-bar button').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
        })
        .catch(error => {
            console.error('Error fetching content:', error);
            document.getElementById('content-display').innerHTML = '<p>Error loading content. Please try again later.</p>';
        });
}
