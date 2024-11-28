from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io

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

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    plant_type = request.form.get('plant_type')
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

    return jsonify({
        'class': class_names[plant_type][predicted_class],
        'probability': float(predictions[0][predicted_class])
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
