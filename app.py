from flask import Flask, render_template, request
from passworld_core import check_strength, estimate_crack_time, calculate_entropy, check_breach

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        password = request.form.get("password")
        result = {
            "strength": check_strength(password),
            "breached": check_breach(password),
            "crack_time": estimate_crack_time(password),
            "entropy": calculate_entropy(password)
        }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)