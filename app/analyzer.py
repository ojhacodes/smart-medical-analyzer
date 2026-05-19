import os
import json
import requests
from typing import Dict, Any

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_mock_response() -> Dict[str, Any]:
    return {
        "age": 45,
        "gender": "Unknown",
        "symptoms": ["headache", "fever"],
        "medications": [
            {
                "name": "Ibuprofen",
                "dosage": "400mg",
                "frequency": "every 6 hours",
                "duration": "3 days"
            }
        ],
        "advice": "Rest and drink plenty of fluids. This is a fallback mock response due to API failure."
    }

def analyze_medical_notes(notes: str) -> Dict[str, Any]:
    if not OPENROUTER_API_KEY:
        print("Warning: OPENROUTER_API_KEY not found. Using mock response.")
        return get_mock_response()

    system_prompt = """
You are a medical text analyzer. Extract the following information from the provided raw physician notes and output strictly as a JSON object. Do not include markdown markers (like ```json), explanations, or any other text. Output only the raw JSON.

The JSON schema must exactly match this structure:
{
  "age": integer or null,
  "gender": "Male", "Female", or "Unknown",
  "symptoms": [list of strings],
  "medications": [
    {
      "name": "string",
      "dosage": "string",
      "frequency": "string",
      "duration": "string"
    }
  ],
  "advice": string or null
}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Smart Medical Text Analyzer",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here are the notes:\n\n{notes}"}
        ],
        "temperature": 0.1
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"]["content"]
            # Clean up potential markdown formatting that the LLM might stubbornly include
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            return json.loads(content)
        else:
            print("Error: Invalid response format from API. Using mock.")
            return get_mock_response()

    except Exception as e:
        print(f"Error calling OpenRouter API: {e}. Using mock response.")
        return get_mock_response()
