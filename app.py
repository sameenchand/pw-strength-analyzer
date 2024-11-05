from flask import Flask, render_template, request, jsonify
import hashlib
import os
import requests
import re

app = Flask(__name__)

# Have I Been Pwned API URL for checking password breaches
HIBP_API_URL = "https://api.pwnedpasswords.com/range/"

# Function to check if the password has been pwned
def check_pwned_password(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_password[:5]
    response = requests.get(HIBP_API_URL + prefix)
    suffix = sha1_password[5:]
    
    for line in response.text.splitlines():
        h, count = line.split(':')
        if h == suffix:
            return True, count
    return False, 0

# Function to evaluate password strength
def evaluate_strength(password):
    length = len(password)
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    # Simple strength logic based on characteristics
    if length >= 12 and has_upper and has_lower and has_digit and has_special:
        return "Strong", "green"
    elif length >= 8 and (has_upper or has_lower) and has_digit:
        return "Moderate", "orange"
    else:
        return "Weak", "red"

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to analyze the password strength and check for breaches
@app.route('/analyze', methods=['POST'])
def analyze():
    password = request.json.get('password')
    
    # Check if password has been compromised
    breached, breach_count = check_pwned_password(password)

    # Evaluate password strength
    strength, strength_color = evaluate_strength(password)

    return jsonify({
        'breached': breached,
        'breach_count': breach_count,
        'strength': strength,
        'strengthColor': strength_color
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

