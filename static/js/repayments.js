function filterTable() {
    const input = document.getElementById("tableSearch").value.toLowerCase();
    document.querySelectorAll("#repaymentHistory tbody tr").forEach(row => {
        row.style.display = row.textContent.toLowerCase().includes(input) ? "" : "none";
    });
}

//sort start

const table = document.getElementById('repaymentHistory');
const sortColumnSelect = document.getElementById('sortColumn');
const toggleButton = document.getElementById('toggleOrder');
let ascending = true;

// Define the type of each column by index
const columnTypes = {
1: 'date',
2: 'number',
3: 'number',
4: 'string',
5: 'number',
6: 'number',
7: 'daysLeft', // special text handling
8: 'number'
};

toggleButton.addEventListener('click', () => {
ascending = !ascending;
toggleButton.textContent = `Toggle Order (${ascending ? "Asc" : "Desc"})`;
sortTable();
});

sortColumnSelect.addEventListener('change', sortTable);

function parseCell(value, type) {
value = value.trim();

switch (type) {
case 'number':
return parseFloat(value.replace(/[^\d.-]/g, '')) || 0;

case 'date':
return new Date(value).getTime() || 0;

case 'daysLeft':
if (value.includes("Expired on")) {
return -9999;
} else if (value.includes("Expires today")) {
return 0;
} else {
const num = parseInt(value.replace(/[^\d]/g, ""));
return isNaN(num) ? 9999 : num;
}

case 'string':
default:
return value;
}
}


function sortTable() {
const columnIndex = parseInt(sortColumnSelect.value);
const type = columnTypes[columnIndex] || 'string';
const tbody = table.tBodies[0];
const rows = Array.from(tbody.rows);

rows.sort((a, b) => {
const valA = parseCell(a.cells[columnIndex]?.textContent || "", type);
const valB = parseCell(b.cells[columnIndex]?.textContent || "", type);

if (type === 'string') {
return ascending
? valA.localeCompare(valB, undefined, { numeric: true, sensitivity: 'base' })
: valB.localeCompare(valA, undefined, { numeric: true, sensitivity: 'base' });
} else {
return ascending
? valA - valB
: valB - valA;
}
});

rows.forEach(row => tbody.appendChild(row));
}


//end sort


function toggleForm() {
    document.getElementById("repaymentForm").style.display = "block";
}
 document.addEventListener("DOMContentLoaded", function () {
const searchInput = document.getElementById("search");
const suggestionsContainer = document.getElementById("suggestions");
const nameDropdown = document.getElementById("nameDropdown");

function showSuggestions() {
const query = searchInput.value.toLowerCase();
suggestionsContainer.innerHTML = ""; // Clear previous suggestions

if (query.length === 0) return; // Stop if input is empty

let suggestions = [];
[...nameDropdown.options].forEach(option => {
    if (option.value && option.textContent.toLowerCase().includes(query)) {
        suggestions.push(option);
    }
});

suggestions.forEach(option => {
    const div = document.createElement("div");
    div.textContent = option.textContent;
    div.classList.add("suggestion-item");
    div.addEventListener("click", function () {
        searchInput.value = option.textContent;
        nameDropdown.value = option.value; // Auto-update dropdown selection
        suggestionsContainer.innerHTML = ""; // Clear suggestions
    });
    suggestionsContainer.appendChild(div);
});
}

searchInput.addEventListener("keyup", showSuggestions);
});

function closeForm() {
    document.getElementById("repaymentForm").style.display = "none";
}

function openImage(imageElement){
    document.getElementById("fullImage").src = imageElement.src;
    document.getElementById("modal").style.display = "flex";
    console.log("opened");
}
    
    
    function closeImage(){
        document.getElementById("modal").style.display = "none";
        console.log("closed");
    }
