from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Load the pre-trained KNN model
with open('knn_model.pkl', 'rb') as model_file:
    loaded_classifier = pickle.load(model_file)

def preprocess_and_predict(user_inputs, loaded_classifier):
    # Convert user inputs to a DataFrame
    user_data = pd.DataFrame(user_inputs, index=[0])

    # One-hot encode categorical variables if needed
    user_data_encoded = pd.get_dummies(user_data, columns=['type_of_soil'])  # Adjust the columns as needed

    # Ensure that the user data has the same columns as the training data
    required_columns = ['type_of_soil', 'temperature', 'humidity', 'ph', 'rainfall']
    for col in required_columns:
        if col not in user_data_encoded.columns:
            user_data_encoded[col] = 0  # Add missing columns with default value

    # Select only the relevant columns for prediction
    user_data_encoded = user_data_encoded[['type_of_soil', 'temperature', 'humidity', 'ph', 'rainfall']]

    # Make predictions using the loaded KNN model
    predictions = loaded_classifier.predict(user_data_encoded)

    return predictions[0]

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Extract user inputs
        user_inputs = {
            'type_of_soil': request.form.get('soil'),
            'temperature': float(request.form.get('temp', 0.0)),  # Use a default value if 'temp' is not provided
            'humidity': float(request.form.get('humi', 0.0)),     # Use a default value if 'humi' is not provided
            'ph': float(request.form.get('ph', 0.0)),              # Use a default value if 'ph' is not provided
            'rainfall': float(request.form.get('rain', 0.0))       # Use a default value if 'rain' is not provided
        }

        # Predict the label
        predicted_label = preprocess_and_predict(user_inputs, loaded_classifier)

        # Mapping for numerical labels to categories
        label_mapping = {0: 'Coffee', 1: 'Corn', 2: 'Mungbean', 3: 'Papaya', 4: 'rice'}
        predicted_category = label_mapping[predicted_label]

        # Prepare a response message
        result_message = f"Recommended Crop: {predicted_category}"

        return jsonify({'result': result_message})  # Return a JSON response for AJAX

    return render_template('index.html', result='')

if __name__ == '__main__':
    app.run(debug=True)