function predict() {
    // Disable the predict button
    document.getElementById("predictButton").disabled = true;

    // Show loading indicator
    document.getElementById("loadingIndicator").style.display = "block";

    // Get user input values
    var N = document.getElementById("N").value.trim();
    var P = document.getElementById("P").value.trim();
    var K = document.getElementById("K").value.trim();
    var pH = document.getElementById("pH").value.trim();
    var temp = document.getElementById("temp").value.trim();
    var humid = document.getElementById("humid").value.trim();
    var rainfall = document.getElementById("rainfall").value.trim();

    // Validate input values
    if (!N || !P || !K || !pH || !temp || !humid || !rainfall) {
        alert('Please fill in all input fields.');

        // Hide loading indicator
        document.getElementById("loadingIndicator").style.display = "none";

        // Enable the predict button
        document.getElementById("predictButton").disabled = false;
        return;
    }

    // Display input values in the inputValues div
    var result_header = document.getElementById("result_header");
    var n_result = document.getElementById("N_result");
    var p_result = document.getElementById("P_result");
    var k_result = document.getElementById("K_result");
    var ph_result = document.getElementById("PH_result");
    var temp_result = document.getElementById("Temp_result");
    var humid_result = document.getElementById("Humid_result");
    var rainfall_result = document.getElementById("Rainfall_result");

    setTimeout(() => {
        // Send the input values to the server for prediction using a POST request
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                N: N,
                P: P,
                K: K,
                pH: pH,
                temp: temp,
                humid: humid,
                rainfall: rainfall,
            }),
        })
        .then(response => response.json())
        .then(prediction => {
            n_result.innerText = `Nitrogen: ${N}`;
            p_result.innerText = `Phosphorous: ${P}`;
            k_result.innerText = `Potassium: ${K}`;
            ph_result.innerText = `pH value: ${pH}`;
            temp_result.innerText = `Temperature: ${temp}`;
            humid_result.innerText = `Humidity: ${humid}`;
            rainfall_result.innerText = `Rainfall: ${rainfall}`;
            result_header.innerText = "Input value:";

            // Map numerical prediction to crop name
            var cropName = mapToCropName(prediction.crop);

            // Handle the prediction result
            var resultTag = document.getElementById("predictionResult");
            resultTag.innerText = 'Recommended Crop: ' + cropName;

            // Reset the form to clear input fields
            document.getElementById("information4").reset();

            // Enable the predict button after displaying the result
            document.getElementById("predictButton").disabled = false;

            // Hide loading indicator
            document.getElementById("loadingIndicator").style.display = "none";
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error occurred during prediction.');

            // Enable the predict button in case of an error
            document.getElementById("predictButton").disabled = false;

            // Hide loading indicator
            document.getElementById("loadingIndicator").style.display = "none";
        });
    }, 3500);
}

// Function to map numerical prediction to crop name
function mapToCropName(prediction) {
    var cropMapping = {
        0: 'Banana',
        1: 'Coconut',
        2: 'Coffee',
        3: 'Maize',
        4: 'Mango',
        5: 'Mungbean',
        6: 'Orange',
        7: 'Papaya',
        8: 'Rice',
        9: 'Watermelon',
    };

    return cropMapping[prediction] || 'Failed to recommend crop';
}