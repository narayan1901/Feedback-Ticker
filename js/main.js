document.addEventListener("DOMContentLoaded", () => {
    const feedbackContainer = document.getElementById("feedbackContainer");

    // Simulating real-time feedback update
    function addFeedback(user, message, category, rating) {
        const feedbackCard = document.createElement("div");
        feedbackCard.classList.add("feedback-card");

        feedbackCard.innerHTML = `
            <p><strong>${user}</strong></p>
            <p>${message}</p>
            <span class="tag">${category}</span> <span class="time">Just now</span>
            <span class="rating">${rating}</span>
        `;

        feedbackContainer.prepend(feedbackCard);
    }

    // Simulated real-time updates (Every 5 seconds)
    setInterval(() => {
        const users = ["John Doe", "Jane Smith", "Attendee 12"];
        const messages = ["Loved the workshop!", "Great insights on AI.", "Well-organized event!"];
        const categories = ["Workshop", "General", "Networking"];
        const ratings = [4, 5, 3];

        const randomIndex = Math.floor(Math.random() * users.length);
        addFeedback(users[randomIndex], messages[randomIndex], categories[randomIndex], ratings[randomIndex]);
    }, 5000);
});