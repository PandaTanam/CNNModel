# Plant Disease Identification API

Welcome to the Plant Disease Identification API! 🌱

This API is designed to help users identify diseases in plants (specifically mango, tomato, and chili) by uploading images. It utilizes machine learning models to predict the disease and provides treatment suggestions based on the identified disease.

## Features

- Upload an image of a plant to predict its disease.
- Retrieve treatment suggestions for the identified disease.
- Store and manage prediction data in Firestore.
- Fetch historical prediction data for specific users.
- Delete prediction data for specific users.
- Access the latest news articles related to plant health.

## Technologies Used

- FastAPI: A modern web framework for building APIs with Python.
- TensorFlow: For loading and using pre-trained machine learning models.
- Google Cloud Storage: For storing uploaded images.
- Firestore: For storing prediction data and treatment suggestions.
- Vertex AI: For generating treatment suggestions using generative models.
- Docker: For containerizing the application.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Google Cloud account with Firestore and Cloud Storage enabled
- Docker (for containerization)

### Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/PlantCare-Bangkit/Plant-Disease-Identification-Model.git
    
    cd plant-disease-identification-api
    ```


2. **Install Dependencies:**
   Make sure you have Python installed. Then, install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**
   Create a `.env` file in the root directory and add your Google Cloud credentials and other necessary configurations:
   ```plaintext
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
   
   BUCKET_NAME=your-bucket-name
   ```


4. **Run the Application:**
   You can run the application using Uvicorn:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8080
    ```

    Alternatively, you can build and run the Docker container:
    ```bash
    docker build -t plantcare-api .
    
    docker run -p 8080:8080 plantcare-api
    ```

## API Endpoints

### 1. Root Endpoint
- **GET** `/`
  - Returns a simple greeting message.

### 2. Predict Disease
- **POST** `/predict/`
  - **Parameters:**
    - `file`: Image file of the plant (required).
    - `plant_type`: Type of plant (mango, tomato, chili) (required).
    - `user_id`: Unique identifier for the user (required).
  - **Response:** Returns a JSON object with the predicted disease, probability, image URL, and treatment suggestion.

### 3. Get Scanned Data
- **GET** `/scanned_data/`
  - Returns all predictions stored in the database.

### 4. Get Predictions by User ID
- **GET** `/scanned_data/{user_id}`
  - **Parameters:**
    - `user_id`: Unique identifier for the user.
  - **Response:** Returns all predictions for the specified user.

### 5. Delete Predictions by User ID
- **DELETE** `/scanned_data/{user_id}`
  - **Parameters:**
    - `user_id`: Unique identifier for the user.
  - **Response:** Returns a message indicating the number of deleted predictions.

### 6. Get Latest News
- **GET** `/news/`
  - Returns the latest news articles related to plant health.

## Deployment

This application deployed on Google Cloud Run. The workflow for building and deploying the Docker container is included in the repository.
