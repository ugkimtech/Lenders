function searchTable() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let table = document.querySelector(".lenderData");
    let rows = table.getElementsByTagName("tr");

    for (let i = 0; i < rows.length; i++) {
        let cells = rows[i].getElementsByTagName("td");
        let match = false;

        for (let j = 0; j < cells.length; j++) {
            if (cells[j]) {
                let text = cells[j].textContent || cells[j].innerText;
                if (text.toLowerCase().includes(input)) {
                    match = true;
                    break;
                }
            }
        }

        rows[i].style.display = match ? "" : "none";
    }
}