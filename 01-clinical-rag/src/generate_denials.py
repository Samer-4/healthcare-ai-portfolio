import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


SCENARIOS = [
    {
        "denial_reason": "step_therapy_not_completed",
        "payer": "Aetna",
        "drug": "semaglutide (Wegovy)",
        "patient": "45-year-old female, BMI 38, type 2 diabetes"
    },
    {
        "denial_reason": "not_medically_necessary",
        "payer": "UnitedHealthcare",
        "drug": "tirzepatide (Zepbound)",
        "patient": "52-year-old male, BMI 35, hypertension"
    },
    {
        "denial_reason": "insufficient_documentation",
        "payer": "Cigna",
        "drug": "semaglutide (Ozempic)",
        "patient": "38-year-old female, BMI 33, prediabetes"
    },
    {
        "denial_reason": "off_label",
        "payer": "BlueCross BlueShield",
        "drug": "liraglutide (Saxenda)",
        "patient": "60-year-old male, BMI 30, sleep apnea"
    },
    {
        "denial_reason": "alternative_covered",
        "payer": "Humana",
        "drug": "semaglutide (Wegovy)",
        "patient": "41-year-old female, BMI 37, PCOS"
    },
    {
        "denial_reason": "step_therapy_not_completed",
        "payer": "Cigna",
        "drug": "tirzepatide (Zepbound)",
        "patient": "49-year-old female, BMI 36, hypothyroidism",
        "format": "portal_message"
    },
    {
        "denial_reason": "not_medically_necessary",
        "payer": "BlueCross BlueShield",
        "drug": "semaglutide (Wegovy)",
        "patient": "55-year-old male, BMI 31, no comorbidities documented",
        "format": "fax_partial"
    },
    {
        "denial_reason": "insufficient_documentation",
        "payer": "Aetna",
        "drug": "tirzepatide (Zepbound)",
        "patient": "33-year-old female, BMI 39, PCOS, insulin resistance",
        "format": "formal_letter"
    },
    {
        "denial_reason": "not_medically_necessary",
        "payer": "Humana",
        "drug": "liraglutide (Saxenda)",
        "patient": "61-year-old male, BMI 33, osteoarthritis",
        "format": "formal_letter"
    },
    {
        "denial_reason": "alternative_covered",
        "payer": "UnitedHealthcare",
        "drug": "tirzepatide (Zepbound)",
        "patient": "44-year-old female, BMI 40, type 2 diabetes, hypertension",
        "format": "formal_letter"
    },
    {
        "denial_reason": "off_label",
        "payer": "Cigna",
        "drug": "semaglutide (Ozempic)",
        "patient": "38-year-old male, BMI 29, non-alcoholic fatty liver disease",
        "format": "formal_letter"
    },
    {
        "denial_reason": "step_therapy_not_completed",
        "payer": "Aetna",
        "drug": "tirzepatide (Zepbound)",
        "patient": "52-year-old female, BMI 37, sleep apnea, hypertension",
        "format": "formal_letter"
    },
]


def generate_denial_letter(scenario):
    format_type = scenario.get("format", "formal_letter")

    if format_type == "portal_message":
        format_instructions = """Format this as a health insurance member portal message — 
not a formal letter. It should look like a short digital notification with:
- A subject line and case/reference number
- Status field showing DENIED
- Brief 2-3 sentence denial rationale in plain language
- A link or instruction to view full details or appeal online
- Casual but official portal tone, no letterhead, no formal salutation
Keep it under 200 words — this is a portal snippet, not a full letter."""

    elif format_type == "fax_partial":
        format_instructions = """Format this as page 2 of a multi-page fax transmission — 
the reader is jumping into the middle of a denial. It should look like:
- A fax header showing page number (PAGE 2 OF 3), date, sender/receiver fax numbers
- No introduction — jump straight into the clinical rationale section mid-document
- Include a policy citation and step therapy requirements
- End mid-section as if the page continues
- Use fax-style formatting: all caps headers, minimal spacing, utilitarian tone"""

    else:
        format_instructions = """Format this as a formal denial letter with:
- Payer letterhead (name, address, phone, fax)
- Date and reference number
- Patient name and ID (synthetic/fictional)
- Prescribing physician name (synthetic/fictional)
- Specific policy citation (make it realistic e.g. "Clinical Policy Bulletin 0580")
- Clinical rationale for the denial
- Appeal rights and instructions (timeframe, address, what to include)
Write in the formal voice of {scenario['payer']}. Be specific and realistic."""

    system_prompt = f"""You are a utilization management reviewer at {scenario['payer']}.
Generate a realistic prior authorization denial for a GLP-1 medication request.

Drug requested: {scenario['drug']}
Denial reason: {scenario['denial_reason']}

{format_instructions}

Do not add any commentary outside the denial itself."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": f"Generate the denial for this patient: {scenario['patient']}"}
        ],
        system=system_prompt
    )

    return message.content[0].text


def save_denial(scenario, letter_text, index):
    base_filename = f"denial_{index:02d}_{scenario['denial_reason']}_{scenario['payer'].lower().replace(' ', '_')}"
    
    letter_path = f"data/synthetic/denials/{base_filename}.txt"
    with open(letter_path, "w") as f:
        f.write(letter_text)
    
    metadata = {
        "filename": f"{base_filename}.txt",
        "denial_reason": scenario["denial_reason"],
        "payer": scenario["payer"],
        "drug": scenario["drug"],
        "patient": scenario["patient"],
        "format": scenario.get("format", "formal_letter"),
    }
    
    metadata_path = f"data/synthetic/denials/{base_filename}.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Saved: {base_filename}")


def main():
    print("Generating GLP-1 denial letters...")
    
    for index, scenario in enumerate(SCENARIOS, start=1):
        print(f"Generating {index}/{len(SCENARIOS)}: {scenario['denial_reason']} — {scenario['payer']}")
        
        letter_text = generate_denial_letter(scenario)
        save_denial(scenario, letter_text, index)
    
    print(f"\nDone. {len(SCENARIOS)} denial letters saved to data/synthetic/denials/")

if __name__ == "__main__":
    main()