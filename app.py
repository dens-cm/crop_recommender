from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

#load the trained model
model_path = Path(__file__).resolve().parent / 'model' / 'knn_model2.joblib'
knn_model = joblib.load(model_path)

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

        # Perform the prediction using the loaded KNN model
        prediction = knn_model.predict([input_values])[0]

        # Convert the NumPy integer to a native Python integer
        prediction = int(prediction)

        # Return the prediction as JSON
        return jsonify({'crop': prediction})
    
    except Exception as e:
        print('Error:', str(e))
        return jsonify({'error': 'An error occurred during prediction.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
