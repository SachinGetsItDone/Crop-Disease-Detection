"""
gemini.py — Gemini API integration for generating crop disease reports.

Person B owns this file.
Call generate_report() after CNN prediction to get the full structured report.
"""

import json
import requests
import streamlit as st

from config import GEMINI_URL, GEMINI_TIMEOUT, GEMINI_MAX_TOKENS, GEMINI_TEMPERATURE


# ── Build the prompt ────────────────────────────────────────────────────────────
def _build_prompt(disease_name: str, confidence: float, symptoms: str) -> str:
    return f"""You are an expert agricultural plant pathologist. Generate a detailed crop disease report.

Disease detected: {disease_name}
Confidence: {confidence:.1%}
Farmer's symptom description: "{symptoms if symptoms else 'Not provided'}"

Return ONLY a valid JSON object with this exact structure (no markdown, no backticks, no extra text):
{{
  "disease_name": "{disease_name}",
  "type": "Fungal|Bacterial|Viral|Oomycete",
  "severity": "Low|Medium|High|Critical",
  "summary": "2-sentence plain English summary of this disease",
  "symptoms": ["symptom 1", "symptom 2", "symptom 3"],
  "spread": "How this disease spreads (1-2 sentences)",
  "immediate_action": "What the farmer should do TODAY (1-2 sentences)",
  "treatment": ["treatment step 1", "treatment step 2", "treatment step 3"],
  "prevention": ["prevention tip 1", "prevention tip 2", "prevention tip 3"],
  "economic_impact": "Estimated yield loss if untreated (1 sentence)",
  "note": "Important disclaimer or consult advice"
}}"""


# ── Call Gemini ─────────────────────────────────────────────────────────────────
def generate_report(disease_name: str, confidence: float, symptoms: str) -> dict:
    """
    Call Gemini Flash to generate a structured disease report.

    Returns a parsed dict on success.
    Returns {"error": "..."} on failure — caller should handle gracefully.
    """
    # Try Streamlit secrets first, then environment variable
    api_key = st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, "secrets") else ""
    if not api_key:
        from config import GEMINI_API_KEY
        api_key = GEMINI_API_KEY

    if not api_key:
        return {"error": "GEMINI_API_KEY not set. Add it to .streamlit/secrets.toml"}

    prompt = _build_prompt(disease_name, confidence, symptoms)

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": GEMINI_TEMPERATURE,
            "maxOutputTokens": GEMINI_MAX_TOKENS,
        },
    }

    try:
        resp = requests.post(
            f"{GEMINI_URL}?key={api_key}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=GEMINI_TIMEOUT,
        )
        resp.raise_for_status()

        raw = resp.json()["candidates"][0]["content"]["parts"][0]["text"]

        # Strip markdown fences if Gemini wraps in ```json ... ```
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```", 2)[-1]          # remove opening fence
            raw = raw.rsplit("```", 1)[0].strip()   # remove closing fence
        if raw.startswith("json"):
            raw = raw[4:].strip()

        return json.loads(raw)

    except requests.exceptions.Timeout:
        return {"error": "Gemini API timed out. Using fallback report."}
    except requests.exceptions.HTTPError as e:
        return {"error": f"Gemini HTTP error: {e.response.status_code}"}
    except json.JSONDecodeError as e:
        return {"error": f"Could not parse Gemini response as JSON: {e}"}
    except Exception as e:
        return {"error": str(e)}


# ── Fallback report (when Gemini unavailable) ────────────────────────────────────
def fallback_report(disease_name: str, confidence: float) -> dict:
    """
    Minimal hardcoded report used when Gemini API key is missing or call fails.
    Keeps the app functional during development / demo without internet.
    """
    return {
        "disease_name": disease_name,
        "type": "Fungal",
        "severity": "Medium",
        "summary": (
            f"{disease_name} detected with {confidence:.1%} confidence. "
            "This disease commonly affects crops in warm, humid conditions and "
            "can spread rapidly if left untreated."
        ),
        "symptoms": [
            "Visible lesions or spots on leaves",
            "Discoloration — yellowing or browning of leaf tissue",
            "Reduced photosynthesis leading to stunted growth",
        ],
        "spread": (
            "Spreads through rain splash, wind-carried spores, "
            "and contact with infected plant material."
        ),
        "immediate_action": (
            "Isolate affected plants immediately. "
            "Remove and destroy visibly infected leaves to slow spread."
        ),
        "treatment": [
            "Apply appropriate fungicide or bactericide as per local guidelines",
            "Remove and destroy all infected plant material",
            "Improve field drainage and air circulation around plants",
        ],
        "prevention": [
            "Use certified disease-resistant seed varieties",
            "Practice crop rotation — avoid same crop in same field each season",
            "Monitor crops regularly for early signs and act at first detection",
        ],
        "economic_impact": (
            "Can reduce yield by 20–40% if left untreated for more than two weeks."
        ),
        "note": (
            "This is an AI-assisted prediction based on visual analysis. "
            "Add GEMINI_API_KEY to .streamlit/secrets.toml for detailed AI reports. "
            "Always consult a local agricultural expert for final confirmation."
        ),
    }
