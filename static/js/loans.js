function searchTable() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let table = document.getElementById("dataTable");
    let rows = table.getElementsByTagName("tr");
    let suggestionsBox = document.getElementById("suggestions");
    suggestionsBox.innerHTML = "";

    let suggestions = [];

    for (let i = 1; i < rows.length; i++) {
        let cells = rows[i].getElementsByTagName("td");
        let matchFound = false;

        for (let j = 0; j < cells.length; j++) {
            let cellText = cells[j].innerText.toLowerCase();
            if (cellText.includes(input)) {
                matchFound = true;
                if (!suggestions.includes(cells[j].innerText)) {
                    suggestions.push(cells[j].innerText);
                }
            }
        }
        rows[i].style.display = matchFound ? "" : "none";
    }

    if (input.length > 0) {
        suggestions.forEach(suggestion => {
            let div = document.createElement("div");
            div.innerHTML = suggestion;
            div.style.padding = "5px";
            div.style.cursor = "pointer";
            div.onclick = function () {
                document.getElementById("searchInput").value = suggestion;
                searchTable();
                suggestionsBox.innerHTML = "";
            };
            suggestionsBox.appendChild(div);
        });
    }
}

function openImage(imageElement) {
    document.getElementById("fullImage").src = imageElement.src;
    document.getElementById("modal").style.display = "flex";
    console.log("opened");
}


function closeImage() {
    document.getElementById("modal").style.display = "none";
    console.log("closed");
}



let sortOrderAsc = true;
function sortTable() {
    let table = document.getElementById("dataTable");
    let columnIndex = document.getElementById("sortDropdown").value;
    let rows = Array.from(table.rows).slice(1);
    rows.sort((a, b) => {
        let valA = a.cells[columnIndex].innerText.toLowerCase();
        let valB = b.cells[columnIndex].innerText.toLowerCase();
        return sortOrderAsc ? valA.localeCompare(valB, undefined, { numeric: true }) : valB.localeCompare(valA, undefined, { numeric: true });
    });
    rows.forEach(row => table.appendChild(row));
}

function toggleSortOrder() {
    sortOrderAsc = !sortOrderAsc;
    sortTable();
}