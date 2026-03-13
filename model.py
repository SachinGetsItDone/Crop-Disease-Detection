"""
model.py — CNN inference using your trained EfficientNet model.

Person A owns this file. Swap mock_predict() with real_predict()
once crop_model.h5 is ready and tested.
"""

import os
import numpy as np
from PIL import Image
import streamlit as st

from config import MODEL_PATH, CLASS_NAMES_PATH, DEFAULT_CLASS_NAMES, IMG_SIZE, TOP_K


# ── Load class names ────────────────────────────────────────────────────────────
def load_class_names() -> list[str]:
    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
            names = [line.strip() for line in f if line.strip()]
        return names
    return DEFAULT_CLASS_NAMES


CLASS_NAMES = load_class_names()


# ── Load model (cached so it only loads once) ───────────────────────────────────
@st.cache_resource
def load_model():
    """
    Load the trained EfficientNetB0 model from disk.
    Returns (model, error_message). If model file missing, returns (None, msg).
    """
    if not os.path.exists(MODEL_PATH):
        return None, f"Model file '{MODEL_PATH}' not found. Using mock predictions."

    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(MODEL_PATH)
        return model, None
    except Exception as e:
        return None, f"Failed to load model: {e}"


# ── Preprocess image ────────────────────────────────────────────────────────────
def preprocess(image: Image.Image) -> np.ndarray:
    """Resize and normalise a PIL image for EfficientNetB0."""
    img = image.convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0   # [0,1]
    return np.expand_dims(arr, axis=0)               # (1, 224, 224, 3)


# ── Real prediction ─────────────────────────────────────────────────────────────
def real_predict(image: Image.Image) -> list[dict]:
    """
    Run the real CNN model on a PIL image.
    Returns a list of dicts: [{"label": str, "confidence": float}, ...]
    """
    model, err = load_model()
    if model is None:
        # Fall back to mock so the app still works during development
        return mock_predict(image, "")

    tensor = preprocess(image)
    probs = model.predict(tensor, verbose=0)[0]          # shape: (num_classes,)
    top_indices = np.argsort(probs)[::-1][:TOP_K]

    results = []
    for idx in top_indices:
        label = CLASS_NAMES[idx] if idx < len(CLASS_NAMES) else f"class_{idx}"
        # Clean up PlantVillage underscore format → readable name
        label = label.replace("___", " — ").replace("_", " ")
        results.append({"label": label, "confidence": float(probs[idx])})

    return results


# ── Mock prediction (used during dev / when model not ready) ────────────────────
def mock_predict(image, symptoms: str) -> list[dict]:
    """
    Keyword-based mock. Remove this once real_predict() is wired up.
    Person A: swap the call in predict() below when model.h5 is ready.
    """
    sym = symptoms.lower() if symptoms else ""

    if "rust" in sym or "orange" in sym or "pustule" in sym:
        return [
            {"label": "Corn — Common rust", "confidence": 0.88},
            {"label": "Apple — Cedar apple rust", "confidence": 0.08},
            {"label": "healthy", "confidence": 0.04},
        ]
    elif "powder" in sym or "white" in sym:
        return [
            {"label": "Squash — Powdery mildew", "confidence": 0.91},
            {"label": "Cherry — Powdery mildew", "confidence": 0.06},
            {"label": "healthy", "confidence": 0.03},
        ]
    elif "curl" in sym or "mosaic" in sym or "distort" in sym:
        return [
            {"label": "Tomato — Tomato mosaic virus", "confidence": 0.85},
            {"label": "Tomato — Yellow Leaf Curl Virus", "confidence": 0.10},
            {"label": "healthy", "confidence": 0.05},
        ]
    elif "dark" in sym or "blight" in sym or "wet" in sym:
        return [
            {"label": "Tomato — Late blight", "confidence": 0.93},
            {"label": "Potato — Late blight", "confidence": 0.05},
            {"label": "healthy", "confidence": 0.02},
        ]
    else:
        return [
            {"label": "Tomato — Early blight", "confidence": 0.76},
            {"label": "Tomato — Bacterial spot", "confidence": 0.15},
            {"label": "healthy", "confidence": 0.09},
        ]


# ── Public entry point ──────────────────────────────────────────────────────────
def predict(image: Image.Image | None, symptoms: str) -> list[dict]:
    """
    Main prediction function called by app.py.

    - If image is provided → run real CNN (falls back to mock if model missing)
    - If only symptoms → run mock keyword logic
    """
    if image is not None:
        return real_predict(image)
    else:
        return mock_predict(None, symptoms)
