function toggleForm() {
    const form = document.getElementById("profileForm");
    form.style.display = form.style.display === "none" || form.style.display === "" ? "block" : "none";
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }