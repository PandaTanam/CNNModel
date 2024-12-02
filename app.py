from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io
import google.generativeai as genai
import os
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load models once when the application starts
mango_model = load_model('models/mango.h5')
tomato_model = load_model('models/tomato.h5')
# chili_model = load_model('models/chili.h5')  # Uncomment if needed

class_names = {
    'mango': ['Anthracnose', 'Bacterial Canker', 'Cutting Weevil', 'Die Back',
              'Gall Midge', 'Healthy', 'Powdery Mildew', 'Sooty Mould'],  
    'tomato': ['Bacterial_spot', 'Early_blight', 'Late_blight', 'Leaf_Mold',
               'Septoria_leaf_spot', 'Spider_mites', 'Target_Spot',
               'Tomato_Yellow_Leaf_Curl_Virus', 'Tomato_mosaic_virus', 'healthy']
    # 'chili': ['chili_Disease_1', 'chili_Disease_2', 'chili_Disease_3']  
}

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'key/service-account.json'

# Initialize Google Cloud Storage client
storage_client = storage.Client()
BUCKET_NAME = "plantcare-api-bucket"

# Initialize Firebase Admin SDK
cred = credentials.Certificate('key/firebase-sdk.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore client
firestore_client = firestore.client()

@app.route('/predict', methods=['POST'])
def predict():
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
        img = image.load_img(io.BytesIO(file.read()), target_size=(256, 256))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        model = mango_model if plant_type == 'mango' else tomato_model
        # model = chili_model if plant_type == 'chili' else None  # Uncomment if needed

        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions)

        disease_name = class_names[plant_type][predicted_class]

        # Use a unique filename for the uploaded image
        blob = storage_client.bucket(BUCKET_NAME).blob(f"{uuid.uuid4()}_{file.filename}")
        blob.upload_from_file(file)

        # Save metadata to Firestore
        firestore_client.collection('scanned_images').add({
            'user_id': user_id,
            'plant_type': plant_type,
            'disease': disease_name,
            'probability': float(predictions[0][predicted_class]),
            'image_url': blob.public_url
        })

        result = {
            'user_id': user_id,
            'plant_type': plant_type,
            'disease': disease_name,
            'probability': float(predictions[0][predicted_class]),
            'treatment': None,
            'image_url': blob.public_url 
        }

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error processing the image: {str(e)}")
        return jsonify({'error': f'Error processing the image: {str(e)}'}), 500

@app.route('/treatment', methods=['POST'])
def treatment():
    genai.configure(api_key=os.getenv("GENAI_API_KEY"))  # Use environment variable for API key
    model = genai.GenerativeModel("gemini-1.5-flash")

    disease = request.json.get('disease')
    plant = request.json.get('plant')
    user_id = request.json.get('user_id')

    if not disease or not plant or not user_id:
        return jsonify({'error': 'Plant, Disease, and User ID must be provided'}), 400

    prompt = f"Langkah-langkah mengatasi/merawat {plant} yang terkena penyakit {disease} dengan penjelasan singkat dan tepat"

    try:
        treatment_suggestion = model.generate_content(prompt)
        treatment_text = treatment_suggestion.text if treatment_suggestion else "No suggestion available."
        
    except Exception as e:
        logging.error(f"Error generating treatment suggestion: {str(e)}")
        return jsonify({'error': f'Error generating treatment suggestion: {str(e)}'}), 500

    # Update the Firestore document with treatment information
    scanned_images_ref = firestore_client.collection('scanned_images')
    query = scanned_images_ref.where('user_id', '==', user_id).where('disease', '==', disease).limit(1).get()

    for doc in query:
        doc_ref = scanned_images_ref.document(doc.id)
        doc_ref.update({'treatment': treatment_text})

    return jsonify({'treatment': treatment_text})

@app.route('/scanned_data', methods=['GET'])
def get_scanned_data():
    # Retrieve all scanned data from Firestore
    scanned_images_ref = firestore_client.collection('scanned_images')
    docs = scanned_images_ref.stream()

    scanned_data = []
    for doc in docs:
        scanned_data.append(doc.to_dict())

    return jsonify(scanned_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))