from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import base64
from PIL import Image

app = Flask(__name__)
model = tf.keras.models.load_model('') 
rescale_layer = tf.keras.layers.Rescaling(1./255)

def preprocess_image(image_data):
    image = Image.open(BytesIO(base64.b64decode(image_data))).convert('RGB')
    image = image.resize((256, 256))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/detect', methods=['POST'])
def detect_disease():
    try:
        image_data = request.json['image']
        image = preprocess_image(image_data)
        prediction = model.predict(image, verbose=0)[0]
        # Asumsikan kelas 0 adalah Bacterial spot dan kelas 1 adalah Early blight, sesuaikan dengan model Anda
        classes = ["Bacterial spot", "Early blight"] # Tambahkan semua kelas yang ada di model Anda
        result = classes[np.argmax(prediction)]
        probability = prediction[np.argmax(prediction)]
        return jsonify({"disease": result, "probability": float(probability)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
