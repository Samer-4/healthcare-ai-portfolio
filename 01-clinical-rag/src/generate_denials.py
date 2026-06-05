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
]


def generate_denial_letter(scenario):
    system_prompt = f"""You are a utilization management reviewer at {scenario['payer']}.
Generate a realistic prior authorization denial letter for a GLP-1 medication request.

The letter must include:
- Payer letterhead (name, address, phone, fax)
- Date and reference number
- Patient name and ID (synthetic/fictional)
- Prescribing physician name (synthetic/fictional)
- Drug requested: {scenario['drug']}
- Denial reason: {scenario['denial_reason']}
- Specific policy citation (make it realistic, e.g. "Clinical Policy Bulletin 0580")
- Clinical rationale for the denial
- Appeal rights and instructions (timeframe, address, what to include)

Write in the formal voice of {scenario['payer']}. Be specific and realistic.
Do not add any commentary outside the letter itself."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": f"Generate the denial letter for this patient: {scenario['patient']}"}
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