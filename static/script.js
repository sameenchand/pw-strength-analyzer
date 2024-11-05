// Analyze Password Function
function analyzePassword() {
    const password = document.getElementById("password").value;
    const strengthMeter = document.getElementById("strengthMeter");
    const breachWarning = document.getElementById("breachWarning");

    // Send password to Flask backend
    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
    })
    .then(response => response.json())
    .then(result => {
        // Display strength feedback
        if (result.breached) {
            breachWarning.textContent = `Warning: This password has been found in ${result.breach_count} breaches!`;
            breachWarning.style.color = 'red';
        } else {
            breachWarning.textContent = "This password is safe.";
            breachWarning.style.color = 'green';
        }

        // Password strength rating (you can enhance this section with more complex logic)
        strengthMeter.style.display = 'block';
        strengthMeter.textContent = result.strength;
        strengthMeter.style.backgroundColor = result.strengthColor;
    })
    .catch(error => console.error('Error:', error));
}
