# ML-Pipeline-Group4-Group4

This project is an ML pipeline course formative 1. It provides ML model, APIs, database configuration and prediction using a developed model.

## Project Structure

```bash
project/
    ├── api
    │   ├── database.py
    │   ├── main.py
    │   ├── models.py
    │   ├── __pycache__
    │   ├── schemas.py
    │   └── seed.py
    ├── api-docs.http
    ├── database
    │   ├── mongodb_setup.py
    │   └── schema.sql
    ├── Dockerfile
    ├── model
    │   ├── ddi-documentation-english-123.pdf
    │   ├── egg_yield_model_gbr.pkl
    │   ├── EggYieldRate_Prediction.ipynb
    │   ├── filtered_egg_production_data.csv
    │   └── Microdata.zip
    ├── prediction
    │   └── predict.py
    ├── README.md
    └── requirements.txt
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ML-Pipeline-Group4
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment. You can create one using:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   You can run the FastAPI application using Uvicorn:
   ```bash
   cd api

   uvicorn api.main:app --reload
   ```

## Usage

Once the application is running, you can access the API documentation at:

OpenAPI (Swagger): `http://127.0.0.1:8000/swagger-ui`.
Redocs: `http://127.0.0.1:8000/docs`


## Docker

To build the Docker image, run:
```bash
docker build -t ML-Pipeline-Group4 .
```

To run the Docker container:
```bash
docker run -d -p 8000:8000 ML-Pipeline-Group4
```

You can then access the API documentation at `http://localhost:8000/docs`
or `http://localhost:8000/swagger-ui`.
