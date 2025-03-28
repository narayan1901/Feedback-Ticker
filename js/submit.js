
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("feedbackForm");
    const ratingElements = document.querySelectorAll(".rating span");
    const ratingInput = document.getElementById("rating");
    const successMessage = document.getElementById("successMessage");

    // Handle rating selection
    ratingElements.forEach(span => {
        span.addEventListener("click", () => {
            ratingElements.forEach(el => el.classList.remove("active"));
            span.classList.add("active");
            ratingInput.value = span.dataset.value;
        });
    });

    // Handle form submission
    form.addEventListener("submit", (event) => {
        event.preventDefault();

        if (!ratingInput.value) {
            alert("Please select a rating.");
            return;
        }

        successMessage.classList.remove("hidden");
        form.reset();
        ratingElements.forEach(el => el.classList.remove("active"));
        ratingInput.value = "";

        setTimeout(() => successMessage.classList.add("hidden"), 3000);
    });
});

