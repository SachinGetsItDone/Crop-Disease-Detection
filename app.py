"""
app.py — Main Streamlit entry point for KrishiMitra AI.

Run with:  streamlit run app.py

Imports from:
  config.py   — constants, API keys, chip labels
  styles.py   — full CSS string
  ui.py       — HTML rendering helpers  (Person C)
  model.py    — CNN inference           (Person A)
  gemini.py   — Gemini report generator (Person B)
"""

import base64
import io

import streamlit as st
from PIL import Image

from config  import APP_TITLE, APP_ICON, SYMPTOM_CHIPS
from styles  import CSS
from ui      import (
    navbar_html,
    detect_heading_html,
    upload_empty_html,
    upload_preview_html,
    result_card_html,
    footer_html,
)
from model   import predict
from gemini  import generate_report, fallback_report

# ── Page config ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Inject CSS ───────────────────────────────────────────────────────────────────
st.markdown(CSS, unsafe_allow_html=True)

# ── Session state defaults ───────────────────────────────────────────────────────
_defaults = {
    "symptoms":       "",
    "uploaded_image": None,   # raw bytes
    "result_html":    "",
    "show_result":    False,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ════════════════════════════════════════════════════════════════════════════════
# NAVBAR
# ════════════════════════════════════════════════════════════════════════════════
st.markdown(navbar_html(), unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# DETECT CARD
# ════════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="detect-section"><div class="detect-card">', unsafe_allow_html=True)

# — Heading —
st.markdown(detect_heading_html(), unsafe_allow_html=True)
st.markdown('<div class="detect-divider"></div>', unsafe_allow_html=True)

# ── IMAGE UPLOAD ──────────────────────────────────────────────────────────────
st.markdown('<span class="detect-label">📷 Upload Leaf Image</span>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed",
    help="Supports JPG, PNG, WEBP — max 10MB",
)

if uploaded_file:
    img_bytes = uploaded_file.read()
    st.session_state.uploaded_image = img_bytes

    b64  = base64.b64encode(img_bytes).decode()
    ext  = uploaded_file.type.split("/")[-1]
    st.markdown(upload_preview_html(b64, ext), unsafe_allow_html=True)

    if st.button("✕ Remove image", key="remove_img"):
        st.session_state.uploaded_image = None
        st.session_state.show_result    = False
        st.rerun()
else:
    st.session_state.uploaded_image = None
    st.markdown(upload_empty_html(), unsafe_allow_html=True)

# ── SYMPTOMS TEXTAREA ─────────────────────────────────────────────────────────
st.markdown(
    '<br><span class="detect-label">📝 Describe Symptoms '
    '<span style="font-weight:400;color:var(--text-muted)">(optional)</span></span>',
    unsafe_allow_html=True,
)

symptoms_input = st.text_area(
    "",
    value=st.session_state.symptoms,
    key="symptom_area",
    placeholder="e.g. brown spots with yellow edges, powdery white coating on leaves...",
    height=110,
    label_visibility="collapsed",
)
st.session_state.symptoms = symptoms_input

# ── QUICK TIP CHIPS ───────────────────────────────────────────────────────────
cols = st.columns(len(SYMPTOM_CHIPS))
for i, (col, tip) in enumerate(zip(cols, SYMPTOM_CHIPS)):
    with col:
        st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
        if st.button(tip, key=f"chip_{i}"):
            cur = st.session_state.symptoms.strip()
            st.session_state.symptoms = (cur + ", " + tip) if cur else tip
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="detect-divider"></div>', unsafe_allow_html=True)

# ── DETECT BUTTON ─────────────────────────────────────────────────────────────
has_image = st.session_state.uploaded_image is not None
has_text  = bool(st.session_state.symptoms.strip())

if   has_image and has_text: btn_label = "🔍 Analyze Image + Symptoms"
elif has_image:              btn_label = "🔍 Analyze Leaf Image"
elif has_text:               btn_label = "🔍 Analyze Symptoms"
else:                        btn_label = "🔍 Start Detection"

_, mid_col, _ = st.columns([1, 2, 1])
with mid_col:
    detect_clicked = st.button(btn_label, use_container_width=True)

# ── RUN DETECTION ─────────────────────────────────────────────────────────────
if detect_clicked:
    if not has_image and not has_text:
        st.warning("Please upload a leaf image or describe symptoms to proceed.")
    else:
        with st.spinner("Analyzing your crop..."):

            # Step 1 — CNN prediction
            pil_img = (
                Image.open(io.BytesIO(st.session_state.uploaded_image)).convert("RGB")
                if has_image else None
            )
            preds = predict(pil_img, st.session_state.symptoms)

            top_disease = preds[0]["label"]
            top_conf    = preds[0]["confidence"]

            # Step 2 — Gemini report
            report = generate_report(top_disease, top_conf, st.session_state.symptoms)
            if "error" in report:
                # Gemini failed — use fallback so app still shows a useful result
                report = fallback_report(top_disease, top_conf)

            # Step 3 — Render
            st.session_state.result_html = result_card_html(report, preds)
            st.session_state.show_result = True

# ── SHOW RESULT ───────────────────────────────────────────────────────────────
if st.session_state.show_result and st.session_state.result_html:
    st.markdown(st.session_state.result_html, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)   # close detect-card + detect-section

# ════════════════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════════════════
st.markdown(footer_html(), unsafe_allow_html=True)
