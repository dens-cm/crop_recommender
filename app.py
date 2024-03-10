from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

#load the trained model and scaler
knn_model = joblib.load('knn_model.joblib')
scaler = joblib.load('model_scaler.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values from the request
        input_data = request.json
        input_values = [float(input_data['N']), float(input_data['P']), float(input_data['K']),
                        float(input_data['pH']), float(input_data['temp']), float(input_data['humid']),
                        float(input_data['rainfall'])]

        # Perform the prediction using the loaded KNN model and the loaded scaler
        scaled_inputs = scaler.transform([input_values])
        prediction = int(knn_model.predict(scaled_inputs)[0])

        # Return the prediction as JSON
        return jsonify({'crop': prediction})

    except Exception as e:
        print('Error:', str(e))
        return jsonify({'error': 'An error occurred during prediction.'}), 500

if __name__ == '__main__':
    app.run()
