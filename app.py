from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load("cyber_threat_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:
        # Taking 42 input features
        features = []

        for i in range(42):
            value = request.form.get(f"feature{i}")
            features.append(float(value))

        # Convert to numpy array
        input_data = np.array(features).reshape(1, -1)

        # Prediction
        prediction = model.predict(input_data)

        if prediction[0] == 0:
            result = "Normal Traffic ✅"
        else:
            result = "Attack Detected ⚠️"

        return render_template(
            "index.html",
            prediction=result
        )

    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)