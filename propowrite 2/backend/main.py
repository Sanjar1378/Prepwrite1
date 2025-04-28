
import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import openai
from pathlib import Path
from string import Template

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY not set")

app = FastAPI(title="PropoWrite API", version="0.1.0")

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "proposal_prompt.txt"
prompt_template = Template(TEMPLATE_PATH.read_text())

class ProposalRequest(BaseModel):
    client_name: str
    project_name: str
    site_description: str
    services_required: str
    budget: str
    deadline: str

class ProposalResponse(BaseModel):
    proposal_markdown: str

def generate_proposal(payload: ProposalRequest) -> str:
    filled_prompt = prompt_template.substitute(
        client_name=payload.client_name,
        project_name=payload.project_name,
        site_description=payload.site_description,
        services_required=payload.services_required,
        budget=payload.budget,
        deadline=payload.deadline
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": filled_prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

@app.post("/generate-proposal", response_model=ProposalResponse)
def create_proposal(data: ProposalRequest, authorization: str | None = Header(default=None)):
    # TODO: Validate JWT token here for paid tier
    try:
        proposal_md = generate_proposal(data)
        return ProposalResponse(proposal_markdown=proposal_md)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
