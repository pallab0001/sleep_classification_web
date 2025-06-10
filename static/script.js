// static/script.js

// Toggle light/dark mode by toggling a CSS class on <body>
function toggleTheme() {
  document.body.classList.toggle("dark-mode");
}

// Handle form submission: send Bengali text to backend and show prediction
document.getElementById("textForm").addEventListener("submit", async function(e) {
  e.preventDefault();
  const text = document.getElementById("textInput").value;
  if (!text) return;
  // Send POST request with JSON body { text: "..."}
  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: text })
  });
  const data = await response.json();
  // Display result
  document.getElementById("result").innerText = "Prediction: " + data.prediction;
});
