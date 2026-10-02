import os
from crewai import Crew, Process, Task
from truvia.agents import build_agents
from truvia.evidence import extract_input

def analyze(kind,content,context="",strict=True):
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is missing. Add it to .env or Streamlit secrets.")
    evidence=extract_input(kind,content,context)
    intake,msg,url,verify,risk,reporter=build_agents()
    ev=repr(evidence)
    t1=Task(description=f"Summarize input type, exact artifacts, and limitations. Do not classify yet.\nEvidence: {ev}",expected_output="Concise inventory of observed artifacts and unknowns.",agent=intake)
    t2=Task(description=f"Analyze the message for specific social-engineering indicators. Quote short exact evidence snippets. If not applicable, say so.\nEvidence: {ev}",expected_output="Indicators with evidence snippets, counter-indicators, and unknowns.",agent=msg,context=[t1])
    t3=Task(description=f"Analyze any supplied URLs structurally (hostname, deceptive subdomain patterns, IP literal, unusual encoding). Do not claim live checks. If none, say no URL supplied.\nEvidence: {ev}",expected_output="URL observations tied to exact strings; explicit lack of live reputation check.",agent=url,context=[t1])
    t4=Task(description=f"Audit the preceding findings against this original evidence: {ev}. Mark each as supported, unsupported, or uncertain. Correct overclaims and contradictions.",expected_output="Verification notes separating supported facts, uncertain inferences, and unsupported claims.",agent=verify,context=[t1,t2,t3])
    t5=Task(description="Create a cautious triage label: High concern / Some concern / Insufficient evidence. Explain using only verified indicators. Do not present label as proof. Include confidence as Low/Moderate only if justified; otherwise Unknown.",expected_output="Risk label, rationale, confidence/limitations, and immediate safe actions.",agent=risk,context=[t1,t2,t3,t4])
    t6=Task(description="Write a concise Markdown report with: Summary, Evidence observed, Assessment, What remains unverified, Recommended safe next steps. Avoid repeating the same point. Never claim an external scan or verification occurred.",expected_output="User-facing Markdown report.",agent=reporter,context=[t1,t2,t3,t4,t5])
    crew=Crew(agents=[intake,msg,url,verify,risk,reporter],tasks=[t1,t2,t3,t4,t5,t6],process=Process.sequential,verbose=False)
    output=crew.kickoff()
    return {"report":str(output),"evidence":evidence,"tasks":[{"task":"Intake"},{"task":"Message analysis"},{"task":"URL analysis"},{"task":"Evidence audit"},{"task":"Risk triage"},{"task":"Report"}]}
