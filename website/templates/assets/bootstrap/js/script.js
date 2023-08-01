
function isValidEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

document.getElementById("contactForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const name = formData.get("name");
    const email = formData.get("email");
    const country = formData.get("country");
    const message = formData.get("message");

    // Validate email format before submitting the form
    if (!isValidEmail(email)) {
        alert("Please enter a valid email address.");
        return;
    }

    const jsonData = {
        name: name,
        email: email,
        country: country,
        message: message,
    };

    fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.message === "Message sent successfully") {
                alert("Message sent successfully!");
            } else {
                alert("Error sending the message. Please try again later.");
            }
            event.target.reset();
        })
        .catch((error) => {
            alert("Error sending the message. Please try again later.");
            console.error("Error:", error);
        });
});
