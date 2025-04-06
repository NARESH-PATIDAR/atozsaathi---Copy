document.addEventListener("DOMContentLoaded", function () {
    const row = document.querySelector(".row");
    const subjects = Array.from(row.children);

    // Clear existing row content
    row.innerHTML = "";

    for (let i = 0; i < subjects.length; i += 5) {
        // Create a new row for each group of 4
        const newRow = document.createElement("div");
        newRow.classList.add("row");

        // Append 4 or fewer items into this new row
        for (let j = i; j < i + 5 && j < subjects.length; j++) {
            newRow.appendChild(subjects[j]);
        }

        // Append the new row to the original parent
        row.parentElement.appendChild(newRow);
    }
});
