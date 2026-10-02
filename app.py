import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from truvia.workflow import analyze
from truvia.evidence import extract_input

load_dotenv()
st.set_page_config(page_title="TRUVIA | Digital Trust", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
:root{--ink:#eaf0ff;--muted:#9aa8c7;--panel:#111b31;--line:#263654;--accent:#8b9cff}
.stApp{background:linear-gradient(135deg,#080e1c 0%,#0d1730 55%,#10162b 100%);color:var(--ink)}
.block-container{max-width:1400px;padding-top:1.6rem}
[data-testid="stSidebar"]{background:#0a1224;border-right:1px solid #263654}
[data-testid="stMetric"]{background:#111b31;border:1px solid #263654;padding:16px;border-radius:16px}
div.stButton>button{border-radius:12px;font-weight:650;min-height:2.8rem}
.hero{padding:24px 28px;border:1px solid #263654;border-radius:20px;background:linear-gradient(120deg,#151f3b,#10182b);margin-bottom:20px}
.hero h1{letter-spacing:.04em;margin:0}.muted{color:#9aa8c7}
</style>
""", unsafe_allow_html=True)
with st.sidebar:
    st.markdown("## 🛡️ TRUVIA")
    st.caption("Multi-Agent Digital Trust & Safety")
    page=st.radio("Workspace",["Analyze evidence","How it works","Team & project"],label_visibility="collapsed")
    st.divider()
    st.markdown("**Analysis settings**")
    strict=st.toggle("Evidence-first mode",value=True,help="Require explicit evidence and label uncertainty.")
    show_steps=st.toggle("Show agent reasoning summary",value=True,help="Shows concise task summaries, not hidden chain-of-thought.")
    st.caption("Groq key is read from environment / Streamlit secrets.")
st.markdown('<div class="hero"><h1>TRUVIA</h1><p class="muted">Digital Trust & Safety · Evidence-led, explainable triage</p></div>',unsafe_allow_html=True)
if page=="Analyze evidence":
    st.write("Submit a suspicious message, URL, or text extracted from a screenshot, QR code, or audio recording.")
    with st.form("analysis_form",clear_on_submit=False):
        kind=st.selectbox("Evidence type",["Suspicious message","URL","Screenshot / image (paste OCR text)","QR code (paste decoded URL/text)","Audio (paste transcript)"])
        content=st.text_area("Evidence to analyze",height=190,placeholder="Paste the message, URL, OCR text, decoded QR content, or transcript…")
        context=st.text_input("Optional context",placeholder="Where did you receive it? What was expected?")
        submitted=st.form_submit_button("Analyze with TRUVIA agents",type="primary",use_container_width=True)
    if submitted:
        if not content.strip(): st.warning("Please provide evidence to analyze.")
        else:
            with st.spinner("Coordinating evidence analysis…"):
                try:
                    result=analyze(kind,content,context,strict)
                    st.session_state["last_result"]=result
                except Exception as e:
                    st.error(f"Analysis could not be completed: {e}")
                    st.info("Check GROQ_API_KEY and install dependencies. No verdict was generated.")
    result=st.session_state.get("last_result")
    if result:
        st.divider(); st.subheader("Assessment")
        st.warning("AI-assisted triage is not proof of fraud. Verify through an independently obtained official channel.")
        st.markdown(result.get("report","No report returned."))
        with st.expander("Evidence extracted and agent task summaries"):
            st.json(result.get("evidence",{}))
            if show_steps: st.json(result.get("tasks",[]))
        st.download_button("Download assessment (Markdown)",result.get("report",""),file_name="truvia_assessment.md",mime="text/markdown")
elif page=="How it works":
    st.subheader("Evidence-first multi-agent workflow")
    st.write("Input normalization → specialist analysis → independent verification → risk synthesis → user-facing report.")
    st.markdown("- Agents receive the same source evidence and return structured findings.\n- The verifier checks whether each claim is supported by supplied evidence.\n- Missing information is labelled unknown; the system must not invent URLs, identities, or verification results.\n- No automatic blocking, reporting, or contacting third parties is performed.")
else:
    st.subheader("Six-person hackathon work split")
    st.markdown("""
| Member | Suggested ownership |
|---|---|
| 1 | Streamlit UI, design system, UX and demo |
| 2 | CrewAI orchestration and agent/task definitions |
| 3 | Evidence ingestion, validation and file handling |
| 4 | Groq integration, prompts and structured outputs |
| 5 | Verification, risk rubric, testing and evaluation |
| 6 | Documentation, deployment, security and presentation |
""")
    st.caption("Replace Member 1–6 with your team's names and confirm ownership together.")
