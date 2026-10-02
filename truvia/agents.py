from crewai import Agent, LLM
def make_llm():
    return LLM(model="groq/llama-3.3-70b-versatile", temperature=0.1, max_tokens=1800)
def build_agents():
    llm=make_llm()
    common="Use only supplied evidence. Never invent facts, sources, scans, domain ownership, or external checks. Separate observations from inferences. If uncertain, say unknown. Return concise, non-repetitive findings."
    intake=Agent(role="Evidence Intake Specialist",goal="Normalize the supplied input and identify what is and is not present.",backstory="A careful digital-forensics intake analyst.",llm=llm,allow_delegation=False,verbose=False)
    message=Agent(role="Social Engineering Analyst",goal="Identify concrete persuasion, impersonation, urgency, and credential/payment cues in the evidence.",backstory="An analyst who distinguishes suspicious patterns from proof.",llm=llm,allow_delegation=False,verbose=False)
    url=Agent(role="URL Structure Analyst",goal="Inspect only the literal URL strings supplied and explain structural indicators.",backstory="A URL parsing specialist; you do not claim to browse or check reputation.",llm=llm,allow_delegation=False,verbose=False)
    verifier=Agent(role="Evidence Verification Auditor",goal="Audit specialist claims against the original evidence and flag unsupported claims.",backstory="A skeptical reviewer who actively checks overclaims and contradictions.",llm=llm,allow_delegation=False,verbose=False)
    risk=Agent(role="Risk Triage Analyst",goal="Produce a calibrated, evidence-linked risk assessment with uncertainty.",backstory="A safety analyst using transparent indicators, not intuition.",llm=llm,allow_delegation=False,verbose=False)
    reporter=Agent(role="User Report Writer",goal="Produce a clear, actionable report without duplicating findings.",backstory="A plain-language digital safety communicator.",llm=llm,allow_delegation=False,verbose=False)
    for a in [intake,message,url,verifier,risk,reporter]: a.allow_delegation=False
    return intake,message,url,verifier,risk,reporter
