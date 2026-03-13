"""
styles.py — Full CSS injected into Streamlit via st.markdown.

Exact match to your style.css + Streamlit widget overrides.
Person C owns this file.
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

:root {
  --green-deep:  #1a4d2e;
  --green-mid:   #2d7a4f;
  --green-light: #4caf50;
  --cream:       #f7f3ed;
  --gold:        #c9a84c;
  --text-dark:   #1a1a1a;
  --text-muted:  #5a5a5a;
}

/* ── Reset Streamlit chrome ── */
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] {
  background: var(--cream);
  font-family: 'DM Sans', sans-serif;
}
[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* ── NAVBAR ── */
.km-navbar {
  background: rgba(247,243,237,0.96);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(26,77,46,0.12);
  padding: 14px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 999;
}
.km-brand {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  color: var(--green-deep);
  font-weight: 700;
  letter-spacing: 0.5px;
}
.km-nav-links { display: flex; gap: 4px; }
.km-nav-links a {
  color: var(--text-dark);
  font-weight: 500;
  font-size: 14px;
  letter-spacing: 0.5px;
  padding: 6px 14px;
  text-decoration: none;
  border-radius: 6px;
  transition: color .2s;
}
.km-nav-links a:hover  { color: var(--green-mid); }
.km-nav-links a.active { color: var(--green-deep); font-weight: 700; }

/* ── DETECT SECTION ── */
.detect-section {
  padding: 60px 20px 80px;
  min-height: 100vh;
  background: var(--cream);
}
.detect-card {
  background: #fff;
  border-radius: 20px;
  padding: 48px 44px;
  box-shadow: 0 20px 60px rgba(26,77,46,0.10);
  border: 1px solid rgba(26,77,46,0.06);
  max-width: 680px;
  margin: 0 auto;
}
.detect-heading {
  font-family: 'Playfair Display', serif;
  font-size: clamp(24px, 3vw, 32px);
  font-weight: 700;
  color: var(--green-deep);
  margin: 8px 0 6px;
}
.detect-sub   { font-size: 14px; color: var(--text-muted); margin-bottom: 0; }
.section-label {
  font-size: 12px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--green-mid);
  font-weight: 600;
  margin-bottom: 4px;
}
.detect-divider {
  height: 1px;
  background: rgba(26,77,46,0.08);
  margin: 28px 0;
}
.detect-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--green-deep);
  margin-bottom: 8px;
  display: block;
  letter-spacing: 0.3px;
}

/* ── UPLOAD BOX ── */
.upload-area {
  border: 2px dashed rgba(26,77,46,0.25);
  padding: 36px 24px;
  text-align: center;
  border-radius: 14px;
  background: #fafdfb;
  transition: border-color .25s, background .25s;
  cursor: pointer;
}
.upload-area:hover  { border-color: var(--green-mid); background: #f2faf3; }
.upload-area.has-image {
  border-color: var(--green-light);
  border-style: solid;
  padding: 12px;
}
.upload-icon { font-size: 36px; display: block; margin-bottom: 10px; }
.upload-lbl  { font-size: 14px; font-weight: 600; color: var(--green-deep); display: block; }
.upload-hint { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.preview-img { width: 100%; max-height: 280px; object-fit: cover; border-radius: 10px; display: block; }

/* ── TIP CHIPS ── */
.tip-chips { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
.chip-btn > button {
  background: rgba(26,77,46,0.07) !important;
  color: var(--green-mid) !important;
  border-radius: 100px !important;
  font-size: 11px !important;
  padding: 4px 10px !important;
  border: none !important;
  font-weight: 500 !important;
}
.chip-btn > button:hover { background: rgba(26,77,46,0.14) !important; }

/* ── RESULT BOX ── */
.result-box {
  margin-top: 28px;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(26,77,46,0.12);
  animation: fadeUp .4s ease;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
.result-header {
  background: var(--green-deep);
  color: #fff;
  padding: 14px 20px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.result-body {
  background: #f8fdf9;
  padding: 20px 22px;
  font-size: 14px;
  color: var(--text-dark);
  line-height: 1.8;
}
.result-body h3 {
  font-family: 'Playfair Display', serif;
  color: var(--green-deep);
  font-size: 18px;
  margin: 0 0 12px;
}
.result-meta { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }
.meta-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(26,77,46,0.07);
  color: var(--green-deep);
  border-radius: 100px;
  padding: 5px 12px;
  font-size: 12px;
  font-weight: 600;
}
.severity-badge {
  border-radius: 100px;
  padding: 5px 12px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
}
.sev-low      { background: #e8f5e9; color: #1b5e20; }
.sev-medium   { background: #fff8e1; color: #f57f17; }
.sev-high     { background: #fbe9e7; color: #bf360c; }
.sev-critical { background: #ffebee; color: #b71c1c; }

/* confidence bars */
.conf-bar-wrap { margin-bottom: 16px; }
.conf-bar-label {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  font-weight: 600;
  color: var(--green-deep);
  margin-bottom: 4px;
}
.conf-bar-bg   { background: rgba(26,77,46,0.08); border-radius: 100px; height: 8px; overflow: hidden; }
.conf-bar-fill {
  height: 100%;
  border-radius: 100px;
  background: linear-gradient(90deg, var(--green-mid), var(--green-light));
  transition: width .8s ease;
}

/* report sections */
.report-section { margin-top: 16px; }
.report-section h4 {
  font-family: 'Playfair Display', serif;
  font-size: 14px;
  font-weight: 700;
  color: var(--green-deep);
  margin: 14px 0 6px;
  padding-top: 14px;
  border-top: 1px solid rgba(26,77,46,0.08);
}
.report-section p, .report-section li {
  font-size: 13.5px;
  color: var(--text-muted);
  line-height: 1.75;
  margin: 0 0 6px;
}
.report-section ul { padding-left: 18px; margin: 4px 0 8px; }
.note-box {
  background: rgba(201,168,76,0.1);
  border-left: 3px solid var(--gold);
  border-radius: 0 8px 8px 0;
  padding: 10px 14px;
  font-size: 12.5px;
  color: #7a6020;
  margin-top: 16px;
}

/* ── FOOTER ── */
.km-footer {
  background: var(--green-deep);
  color: rgba(255,255,255,0.7);
  padding: 48px 32px 32px;
  text-align: center;
  margin-top: 60px;
}
.km-footer .brand { font-family: 'Playfair Display', serif; font-size: 22px; color: #fff; margin-bottom: 8px; }
.km-footer p      { font-size: 13px; margin: 0; }
.km-footer .copy  { margin-top: 28px; font-size: 12px; color: rgba(255,255,255,0.35); }
.footer-links { display: flex; justify-content: center; gap: 24px; margin: 16px 0 0; flex-wrap: wrap; }
.footer-links a { color: rgba(255,255,255,0.55); font-size: 13px; text-decoration: none; transition: color .2s; }
.footer-links a:hover { color: #fff; }

/* ── Streamlit widget overrides ── */
[data-testid="stFileUploader"] {
  border: 2px dashed rgba(26,77,46,0.25) !important;
  border-radius: 14px !important;
  background: #fafdfb !important;
  padding: 20px !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--green-mid) !important;
  background: #f2faf3 !important;
}
[data-testid="stTextArea"] textarea {
  border: 1.5px solid rgba(26,77,46,0.18) !important;
  border-radius: 12px !important;
  background: #fafdfb !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 14px !important;
}
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--green-mid) !important;
  box-shadow: 0 0 0 3px rgba(45,122,79,0.1) !important;
}
[data-testid="stButton"] > button {
  background: var(--green-deep) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  padding: 12px 32px !important;
  transition: background .2s, transform .2s !important;
}
[data-testid="stButton"] > button:hover {
  background: var(--green-mid) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(26,77,46,0.25) !important;
}

@media (max-width: 640px) {
  .detect-card  { padding: 28px 20px; }
  .km-navbar    { padding: 12px 16px; }
}
</style>
"""
