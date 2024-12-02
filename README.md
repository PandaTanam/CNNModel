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
        "treatment": "Penyakit Bacterial Spot pada tomat sulit disembuhkan sepenuhnya..."
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
    "treatment": null
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

#### Example Response
```json
{
    "user_id": "12345",
    "plant_type": "tomato",
    "disease": "Bacterial_spot",
    "probability": 0.85,
    "treatment": null
}
```

### Get Treatment Suggestion Based on The Detected Disease and Plant Type

```http
POST /treatment
```

#### Parameters
| Parameter  | Type     | Description                |
| :--------- | :------- | :------------------------- |
| `user_id`  | `string` | **Required**. The ID of the user |
| `plant`    | `string` | **Required**. The type of plant |
| `disease`  | `string` | **Required**. The disease of the plant |

#### Example Response
```json
{
    "treatment": "Langkah-langkah mengatasi/merawat tanaman yang terkena penyakit..."
}
```