from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io
import google.generativeai as genai

app = Flask(__name__)

mango_model = load_model('models/mango.h5')
tomato_model = load_model('models/tomato.h5')
# apple_model = load_model('models/apple.h5')

class_names = {
    'mango': ['Anthracnose', 'Bacterial Canker', 'Cutting Weevil', 'Die Back',
              'Gall Midge', 'Healthy', 'Powdery Mildew', 'Sooty Mould'],  
    'tomato': ['Bacterial_spot', 'Early_blight', 'Late_blight', 'Leaf_Mold',
               'Septoria_leaf_spot', 'Spider_mites', 'Target_Spot',
               'Tomato_Yellow_Leaf_Curl_Virus', 'Tomato_mosaic_virus', 'healthy']
    # 'apple': ['Apple_Disease_1', 'Apple_Disease_2', 'Apple_Disease_3']  
}

scanned_data = []

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

    img = image.load_img(io.BytesIO(file.read()), target_size=(256, 256))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    if plant_type == 'mango':
        model = mango_model
    elif plant_type == 'tomato':
        model = tomato_model
    # elif plant_type == 'apple':
    #     model = apple_model

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)

    disease_name = class_names[plant_type][predicted_class]

    result = {
        'user_id': user_id,
        'plant_type': plant_type,
        'disease': disease_name,
        'probability': float(predictions[0][predicted_class]),
        'treatment': None
    }
    scanned_data.append(result)

    return jsonify(result)

@app.route('/treatment', methods=['POST'])
def treatment():
    genai.configure(api_key="AIzaSyCXrHQKYgn2VWxe3iGaxz7y55U9ogdJU3I")
    model = genai.GenerativeModel("gemini-1.5-flash")

    disease = request.json.get('disease')
    plant = request.json.get('plant')
    user_id = request.json.get('user_id')

    if not disease or not plant or not user_id:
        return jsonify({'error': 'Plant, Disease, and User ID must be provided'}), 400

    prompt = f"Langkah-langkah mengatasi/merawat {plant} yang terkena penyakit {disease} dengan penjelasan singkat dan tepat"

    treatment_suggestion = model.generate_content(prompt)

    for entry in scanned_data :
        if entry['user_id'] == user_id :
            entry['treatment'] = treatment_suggestion.text
            break

    return jsonify({'treatment': treatment_suggestion.text})

@app.route('/scanned_data', methods=['GET'])
def get_scanned_data():
    return jsonify(scanned_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
