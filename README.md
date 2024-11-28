# API Documentation

## Base URL
```bash
http://0.0.0.0/9000
```

<ol>
  <li>
    <h2>Endpoint: /predict</h2>
    <p>Method: POST</p>
    <p>Description: Upload an image of a plant leaf to detect the disease and get the prediction result</p>
    <p>Request :</p>
    <ul>
      <li>
        user_id: The ID of the user.
      </li>
      <li>
        file: The image file of the plant leaf (e.g., .jpg, ,png).
      </li>
      <li>
        plant_type: The type of plant (e.g., mango, tomato).
      </li>
    </ul>
    <p>Content-Type Response: application/json</p>
    ```json
        {
          "user_id": "12345",
          "plant_type": "tomato",
          "class": "Bacterial_spot",
          "probability": 0.85,
          "treatment": null
        }
    ```
  </li>
</ol>
