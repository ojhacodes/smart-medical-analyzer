# Smart Medical Text Analyzer (https://smart-medical-analyzer.onrender.com/)

A lightweight FastAPI service that processes unstructured medical notes into structured data using the Llama-3-8b model via OpenRouter.

## Requirements

- Python 3.11+
- Docker (optional)

## Setup and Local Execution

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variable for OpenRouter API:**
   ```bash
   export OPENROUTER_API_KEY="your_api_key_here"
   ```
   *Note: If the key is omitted or invalid, the application will fallback to returning mock JSON data.*

3. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Verification and Endpoints

- **Swagger UI**: Go to `http://127.0.0.1:8000/docs` to test the API directly from your browser.
- **POST `/analyze`**: Submit raw text notes to get a structured JSON response (age, gender, symptoms, medications, advice). The response is saved to the local SQLite database (`medical_analyzer.db`).
- **GET `/history`**: Retrieve a list of previously processed records.

## Docker Deployment

To build and run via Docker:

```bash
docker build -t smart-medical-analyzer .
docker run -p 8000:8000 -e OPENROUTER_API_KEY="your_api_key_here" smart-medical-analyzer
```
