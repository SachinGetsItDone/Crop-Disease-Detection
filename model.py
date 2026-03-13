"""
model.py — CNN inference using your trained PyTorch EfficientNet model.
Person A owns this file.
"""

import os
import numpy as np
from PIL import Image
import streamlit as st
import torch

from config import MODEL_PATH, CLASS_NAMES_PATH, DEFAULT_CLASS_NAMES, IMG_SIZE, TOP_K

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MEAN = [0.485, 0.456, 0.406]
STD  = [0.229, 0.224, 0.225]


def load_class_names() -> list:
    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return DEFAULT_CLASS_NAMES

CLASS_NAMES = load_class_names()


@st.cache_resource
def load_model():
    """
    Supports two formats:
      torch.save(model, path)              — full model object
      torch.save(model.state_dict(), path) — weights only
    Returns (model, error_string).
    """
    if not os.path.exists(MODEL_PATH):
        return None, f"'{MODEL_PATH}' not found. Place it next to app.py."

    try:
        checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)

        # Full model
        if isinstance(checkpoint, torch.nn.Module):
            checkpoint.eval()
            return checkpoint, None

        # State dict (plain dict or nested)
        if isinstance(checkpoint, dict):
            state_dict = (
                checkpoint.get("model_state_dict")
                or checkpoint.get("state_dict")
                or checkpoint
            )
            from torchvision.models import efficientnet_b0
            import torch.nn as nn
            model = efficientnet_b0(weights=None)
            model.classifier[1] = nn.Linear(
                model.classifier[1].in_features, len(CLASS_NAMES)
            )
            model.load_state_dict(state_dict)
            model.to(DEVICE).eval()
            return model, None

        return None, "Unrecognised checkpoint format."

    except Exception as e:
        return None, f"Failed to load model: {e}"


def preprocess(image: Image.Image) -> torch.Tensor:
    img = image.convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = (arr - np.array(MEAN)) / np.array(STD)
    tensor = torch.from_numpy(arr).permute(2, 0, 1)   # (3, H, W)
    return tensor.unsqueeze(0).to(DEVICE)              # (1, 3, H, W)


def real_predict(image: Image.Image) -> list:
    model, err = load_model()
    if model is None:
        return mock_predict(image, "")

    with torch.no_grad():
        outputs = model(preprocess(image))
        if isinstance(outputs, (tuple, list)):
            outputs = outputs[0]
        probs = torch.softmax(outputs, dim=1)[0]

    top_vals, top_idx = torch.topk(probs, k=min(TOP_K, probs.shape[0]))
    results = []
    for val, idx in zip(top_vals.cpu().numpy(), top_idx.cpu().numpy()):
        label = CLASS_NAMES[idx] if idx < len(CLASS_NAMES) else f"class_{idx}"
        label = label.replace("___", " — ").replace("_", " ")
        results.append({"label": label, "confidence": float(val)})
    return results


def mock_predict(image, symptoms: str) -> list:
    sym = symptoms.lower() if symptoms else ""
    if "rust" in sym or "orange" in sym or "pustule" in sym:
        return [
            {"label": "Corn — Common rust",       "confidence": 0.88},
            {"label": "Apple — Cedar apple rust",  "confidence": 0.08},
            {"label": "Healthy",                   "confidence": 0.04},
        ]
    elif "powder" in sym or "white" in sym:
        return [
            {"label": "Squash — Powdery mildew",   "confidence": 0.91},
            {"label": "Cherry — Powdery mildew",   "confidence": 0.06},
            {"label": "Healthy",                   "confidence": 0.03},
        ]
    elif "curl" in sym or "mosaic" in sym or "distort" in sym:
        return [
            {"label": "Tomato — Mosaic virus",     "confidence": 0.85},
            {"label": "Tomato — Yellow Leaf Curl", "confidence": 0.10},
            {"label": "Healthy",                   "confidence": 0.05},
        ]
    elif "dark" in sym or "blight" in sym or "wet" in sym:
        return [
            {"label": "Tomato — Late blight",      "confidence": 0.93},
            {"label": "Potato — Late blight",      "confidence": 0.05},
            {"label": "Healthy",                   "confidence": 0.02},
        ]
    else:
        return [
            {"label": "Tomato — Early blight",     "confidence": 0.76},
            {"label": "Tomato — Bacterial spot",   "confidence": 0.15},
            {"label": "Healthy",                   "confidence": 0.09},
        ]


def predict(image, symptoms: str) -> list:
    if image is not None:
        return real_predict(image)
    return mock_predict(None, symptoms)
