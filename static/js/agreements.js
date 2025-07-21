document.getElementById("searchBox").addEventListener("input", function () {
    let query = this.value.trim().toLowerCase(); // Remove leading/trailing spaces
    let items = document.querySelectorAll(".section");

    items.forEach(item => {
        item.style.display = item.textContent.toLowerCase().includes(query) ? "block" : "none";

    });
});

function openImage(imageElement) {
    document.getElementById("fullImage").src = imageElement.src;
    document.getElementById("modal").style.display = "flex";
    console.log("opened");
}


function closeImage() {
    document.getElementById("modal").style.display = "none";
    console.log("closed");
}
