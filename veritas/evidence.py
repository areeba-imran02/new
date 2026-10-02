import re
from urllib.parse import urlparse

MAX_CHARS=12000
def extract_input(kind: str, content: str, context: str="") -> dict:
    raw=(content or "").strip()
    if not raw: raise ValueError("Evidence is empty.")
    if len(raw)>MAX_CHARS: raise ValueError(f"Evidence exceeds {MAX_CHARS} characters.")
    urls=re.findall(r'https?://[^\s<>()\[\]{}"\']+',raw,flags=re.I)
    normalized=[]
    for u in urls:
        try:
            p=urlparse(u.rstrip(".,;"))
            if p.scheme in ("http","https") and p.hostname:
                normalized.append({"url":u.rstrip(".,;"),"host":p.hostname.lower()})
        except ValueError: pass
    return {"type":kind,"content":raw,"context":context.strip(),"urls":normalized,
            "note":"URLs are extracted from user-provided text only; no live reputation or ownership check has been performed."}
