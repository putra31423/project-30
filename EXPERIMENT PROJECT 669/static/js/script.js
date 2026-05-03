document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("booking-form");
  const responseDiv = document.getElementById("form-response");

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(form);
      const data = Object.fromEntries(formData.entries());

      // Disable button
      const btn = form.querySelector("button");
      const originalText = btn.textContent;
      btn.disabled = true;
      btn.textContent = "Sending...";
      responseDiv.textContent = "";
      responseDiv.style.color = "#333";

      try {
        const response = await fetch("/api/inquiry", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        const result = await response.json();

        if (response.ok) {
          responseDiv.textContent = result.message;
          responseDiv.style.color = "green";
          form.reset();
        } else {
          responseDiv.textContent =
            "Error: " + (result.error || "Something went wrong");
          responseDiv.style.color = "red";
        }
      } catch (error) {
        console.error("Error:", error);
        responseDiv.textContent = "Network error. Please try again.";
        responseDiv.style.color = "red";
      } finally {
        btn.disabled = false;
        btn.textContent = originalText;
      }
    });
  }
});
