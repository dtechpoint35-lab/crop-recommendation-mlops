from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained model and preprocessing objects
model = joblib.load('./models/crop_model.pkl')
scaler = joblib.load('./models/scaler.pkl')
label_encoder = joblib.load('./models/label_encoder.pkl')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    N = float(request.form['N'])
    P = float(request.form['P'])
    K = float(request.form['K'])
    temperature = float(request.form['temperature'])
    humidity = float(request.form['humidity'])
    ph = float(request.form['ph'])
    rainfall = float(request.form['rainfall'])

    input_data = pd.DataFrame(
        [[N, P, K, temperature, humidity, ph, rainfall]],
        columns=[
            'N',
            'P',
            'K',
            'temperature',
            'humidity',
            'ph',
            'rainfall'
        ]
    )

    input_scaled = scaler.transform(input_data)

    prediction = model.predict(input_scaled)

    crop_name = label_encoder.inverse_transform(prediction)[0]

    return render_template(
        'index.html',
        prediction_text=f"Recommended Crop: {crop_name}"
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )