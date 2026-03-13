"""
ui.py — HTML rendering helpers.

Person C owns this file.
Every function returns an HTML string that gets injected via st.markdown(..., unsafe_allow_html=True).
"""


# ── Navbar ───────────────────────────────────────────────────────────────────────
def navbar_html() -> str:
    return """
<div class="km-navbar">
  <div class="km-brand">🌿 KrishiMitra AI</div>
  <div class="km-nav-links">
    <a href="#">Home</a>
    <a href="#">Diseases</a>
    <a href="#">Prevention</a>
    <a href="#" class="active">Detect</a>
  </div>
</div>"""


# ── Detect card heading ──────────────────────────────────────────────────────────
def detect_heading_html() -> str:
    return """
<div style="text-align:center;">
  <div class="section-label">AI Powered</div>
  <h2 class="detect-heading">Crop Disease Detection</h2>
  <p class="detect-sub">Upload a leaf image, describe symptoms, or both — our AI will diagnose instantly.</p>
</div>"""


# ── Upload area states ───────────────────────────────────────────────────────────
def upload_empty_html() -> str:
    return """
<div class="upload-area">
  <span class="upload-icon">🍃</span>
  <span class="upload-lbl">Click or drag to upload leaf photo</span>
  <p class="upload-hint">Supports JPG, PNG, WEBP — max 10MB</p>
</div>"""


def upload_preview_html(b64: str, ext: str) -> str:
    return f"""
<div class="upload-area has-image">
  <img class="preview-img" src="data:image/{ext};base64,{b64}" alt="Leaf preview">
</div>"""


# ── Confidence bars ───────────────────────────────────────────────────────────────
def confidence_bars_html(preds: list[dict]) -> str:
    html = "<div class='conf-bar-wrap'>"
    for i, p in enumerate(preds):
        icon = "⭐ " if i == 0 else ""
        pct = p["confidence"] * 100
        html += f"""
  <div style="margin-bottom:10px;">
    <div class="conf-bar-label">
      <span>{icon}{p['label']}</span>
      <span>{pct:.1f}%</span>
    </div>
    <div class="conf-bar-bg">
      <div class="conf-bar-fill" style="width:{pct:.1f}%"></div>
    </div>
  </div>"""
    html += "</div>"
    return html


# ── Severity badge ────────────────────────────────────────────────────────────────
def severity_badge_html(severity: str) -> str:
    cls_map = {
        "Low":      "sev-low",
        "Medium":   "sev-medium",
        "High":     "sev-high",
        "Critical": "sev-critical",
    }
    cls = cls_map.get(severity, "sev-medium")
    return f'<span class="severity-badge {cls}">{severity}</span>'


# ── Full result card ──────────────────────────────────────────────────────────────
def result_card_html(report: dict, preds: list[dict]) -> str:
    """
    Renders the full diagnosis result card.
    Handles both successful Gemini reports and error/fallback reports.
    """
    # ── Error / no Gemini ──
    if "error" in report:
        top = preds[0]
        return f"""
<div class='result-box'>
  <div class='result-header'>🧠 AI Diagnosis Result</div>
  <div class='result-body'>
    <h3>{top['label']}</h3>
    {confidence_bars_html(preds)}
    <div class='note-box'>⚠️ {report['error']}</div>
  </div>
</div>"""

    # ── Full report ──
    sev      = report.get("severity", "Medium")
    d_type   = report.get("type", "")
    conf     = preds[0]["confidence"]

    symp_li  = "".join(f"<li>{s}</li>" for s in report.get("symptoms", []))
    treat_li = "".join(f"<li>{t}</li>" for t in report.get("treatment", []))
    prev_li  = "".join(f"<li>{p}</li>" for p in report.get("prevention", []))

    return f"""
<div class='result-box'>
  <div class='result-header'>🧠 AI Diagnosis Result</div>
  <div class='result-body'>

    <h3>{report.get('disease_name', preds[0]['label'])}</h3>

    <div class='result-meta'>
      <span class='meta-badge'>🔬 {d_type}</span>
      {severity_badge_html(sev)}
      <span class='meta-badge'>📊 {conf:.1%} confidence</span>
    </div>

    {confidence_bars_html(preds)}

    <p>{report.get('summary', '')}</p>

    <div class='report-section'>
      <h4>⚡ Immediate Action</h4>
      <p>{report.get('immediate_action', '')}</p>

      <h4>🔍 Symptoms</h4>
      <ul>{symp_li}</ul>

      <h4>💊 Treatment Steps</h4>
      <ul>{treat_li}</ul>

      <h4>🛡️ Prevention</h4>
      <ul>{prev_li}</ul>

      <h4>🌾 Economic Impact</h4>
      <p>{report.get('economic_impact', '')}</p>

      <h4>🌱 How It Spreads</h4>
      <p>{report.get('spread', '')}</p>
    </div>

    <div class='note-box'>📌 {report.get('note', '')}</div>

  </div>
</div>"""


# ── Footer ────────────────────────────────────────────────────────────────────────
def footer_html() -> str:
    return """
<div class="km-footer">
  <div class="brand">🌿 KrishiMitra AI</div>
  <p>Empowering farmers with artificial intelligence.</p>
  <div class="footer-links">
    <a href="#">Home</a>
    <a href="#">Diseases</a>
    <a href="#">Prevention</a>
    <a href="#">Detect</a>
  </div>
  <div class="copy">© 2026 KrishiMitra AI. All rights reserved.</div>
</div>"""
