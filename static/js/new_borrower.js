// Set default date to today
document.getElementById('date').valueAsDate = new Date();

// Section toggle functionality
const sectionHeaders = document.querySelectorAll('.section-header');
sectionHeaders.forEach(header => {
    header.addEventListener('click', () => {
        const section = header.parentElement;
        const content = header.nextElementSibling;

        // Toggle active class
        header.classList.toggle('active');
        content.classList.toggle('active');
    });
});

function togleView() {
    let pw = document.getElementById("pw");
    if (pw.type === 'password') {
        pw.type = 'text';
        pw.textContent = "Show Password 😑";
    }
    else {
        pw.type = 'password';
        pw.textContent = "Show Password 👀";
    }
}
