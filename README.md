# API Documentation

## Base URL
```bash
https://plantcare-api-github-920676430522.asia-southeast2.run.app
```

## API Reference

### Get All Plant Disease Identification Data

```http
GET /scanned_data
```

#### Parameters
None

#### Example Response
```json
[
    {
        "user_id": "1",
        "plant_type": "mango",
        "disease": "Bacterial Canker",
        "probability": 0.6879741549491882,
        "image_url": "https://example.com/image.jpg",
        "treatment": "Penyakit Bacterial Spot pada tomat sulit disembuhkan sepenuhnya...",
        "scanned_data": "2024:12:03"
    },
    ...
]
```

### Get Plant Disease Identification Data By User ID

```http
GET /scanned_data/${user_id}
```

#### Parameters
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `user_id` | `string` | **Required**. The ID of the user |

#### Example Response
```json
{
    "user_id": "1",
    "plant_type": "mango",
    "disease": "Bacterial Canker",
    "probability": 0.6879741549491882,
    "image_url": "https://example.com/image.jpg",
    "treatment": null,
    "scanned_data": "2024:12:03"
}
```

### Predict Plant Disease

```http
POST /predict
```

#### Parameters
| Parameter    | Type     | Description                              |
| :----------- | :------- | :--------------------------------------- |
| `plant_type` | `string` | **Required**. The type of plant          |
| `user_id`    | `string` | **Required**. The ID of the user         |
| `file`       | `file`   | **Required**. The image file of the plant leaf |

#### Example Request
```json
POST /predict
Content-Type: multipart/form-data

{
    "plant_type": "tomato",
    "user_id": "12345",
    "file": <image_file>
}
```
#### Example Response
```json
{
    "user_id": "12345",
    "plant_type": "tomato",
    "disease": "Bacterial_spot",
    "probability": 0.85,
    "image_url": "https://example.com/image.jpg",
    "treatment": null,
    "scanned_data": "2024:12:03"
}
```

### Delete All Predictions for a Specific User ID
```http
DELETE /scanned_data/{user_id}
```

#### Parameters
| Parameter    | Type     | Description                              |
| :----------- | :------- | :--------------------------------------- |
| `user_id`    | `string` | **Required**. The ID of the user         |

#### Example Response
```json
{
    "message": "Deleted 3 prediction(s) successfully."
}
```

#### Example Error Response
```json
{
    "detail": "Invalid plant type"
}
```