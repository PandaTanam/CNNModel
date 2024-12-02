from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
import google.generativeai as genai
from google.cloud import storage
import uuid
import logging
import requests
import io

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load models once when the application starts
mango_model = load_model('models/mango.h5')
tomato_model = load_model('models/tomato.h5')

# Class names for predictions
class_names = {
    'mango': ['Anthracnose', 'Bacterial Canker', 'Cutting Weevil', 'Die Back',
              'Gall Midge', 'Healthy', 'Powdery Mildew', 'Sooty Mould'],  
    'tomato': ['Bacterial_spot', 'Early_blight', 'Late_blight', 'Leaf_Mold',
               'Septoria_leaf_spot', 'Spider_mites', 'Target_Spot',
               'Tomato_Yellow_Leaf_Curl_Virus', 'Tomato_mosaic_virus', 'healthy']
}

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'plantcare-443106-29fd09534606.json'

# Initialize Google Cloud Storage client
storage_client = storage.Client()
BUCKET_NAME = "plantcare-api-bucket"

# Store prediction results in memory (for demonstration purposes)
predictions_data = {}

@app.route('/predict', methods=['POST'])
def predict():
    # Validate request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    plant_type = request.form.get('plant_type')
    user_id = request.form.get('user_id')
    if plant_type not in class_names:
        return jsonify({'error': 'Invalid plant type'}), 400

    try:
        # Upload the image to Google Cloud Storage
        blob = storage_client.bucket(BUCKET_NAME).blob(f"{uuid.uuid4()}_{file.filename}")
        blob.upload_from_file(file)

        # Get the public URL of the uploaded image
        image_url = blob.public_url

        # Load the image for prediction
        img = image.load_img(io.BytesIO(requests.get(image_url).content), target_size=(256, 256))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Select the appropriate model
        model = mango_model if plant_type == 'mango' else tomato_model

        # Make predictions
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions)
        disease_name = class_names[plant_type][predicted_class]

        # Store the prediction result
        result = {
            'user_id': user_id,
            'plant_type': plant_type,
            'disease': disease_name,
            'probability': float(predictions[0][predicted_class]),
            'image_url': image_url,
            'treatment': None 
        }

        # Store the result in memory using user_id as the key
        predictions_data[user_id] = result

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error processing the image: {str(e)}")
        return jsonify({'error': f'Error processing the image: {str(e)}'}), 500

@app.route('/treatment', methods=['POST'])
def treatment():
    genai.configure(api_key="AIzaSyCXrHQKYgn2VWxe3iGaxz7y55U9ogdJU3I")
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Validate request
    disease = request.json.get('disease')
    plant = request.json.get('plant')
    user_id = request.json.get('user_id')

    if not disease or not plant or not user_id:
        return jsonify({'error': 'Plant, Disease, and User ID must be provided'}), 400

    # Check if prediction data exists for the user
    if user_id not in predictions_data:
        return jsonify({'error': 'No prediction data found for this user ID.'}), 404

    prompt = f"Langkah-langkah mengatasi/merawat {plant} yang terkena penyakit {disease} dengan penjelasan singkat dan tepat"

    try:
        treatment_suggestion = model.generate_content(prompt)
        treatment_text = treatment_suggestion.text if treatment_suggestion else "No suggestion available."

        # Append treatment information to the prediction result
        predictions_data[user_id]['treatment'] = treatment_text

    except Exception as e:
        logging.error(f"Error generating treatment suggestion: {str(e)}")
        return jsonify({'error': f'Error generating treatment suggestion: {str(e)}'}), 500

    return jsonify({'treatment': treatment_text})

@app.route('/scanned_data', methods=['GET'])
def get_scanned_data():
    return jsonify(predictions_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
