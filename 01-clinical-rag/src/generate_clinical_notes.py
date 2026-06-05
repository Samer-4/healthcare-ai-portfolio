import anthropic
import json 
import os
from dotenv import load_dotenv 

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

CLINICAL_SCENARIOS = [
    {
        "case_id": "case_001",
        "denial_file": "denial_01_step_therapy_not_completed_aetna.txt",
        "denial_reason": "step_therapy_not_completed",
        "payer": "Aetna",
        "drug": "semaglutide (Wegovy)",
        "note_type": "progress_note",
        "patient": {
            "name": "Jennifer L. Caldwell",
            "age": 45,
            "sex": "female",
            "bmi": 38,
            "diagnoses": ["E11.9", "E66.01"],
            "comorbidities": ["type 2 diabetes", "hypertension"]
        }
    },
    {
        "case_id": "case_002",
        "denial_file": "denial_02_not_medically_necessary_unitedhealthcare.txt",
        "denial_reason": "not_medically_necessary",
        "payer": "UnitedHealthcare",
        "drug": "tirzepatide (Zepbound)",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Robert M. Okafor",
            "age": 52,
            "sex": "male",
            "bmi": 35,
            "diagnoses": ["I10", "E66.09"],
            "comorbidities": ["hypertension", "obesity"]
        }
    },
    {
        "case_id": "case_003",
        "denial_file": "denial_03_insufficient_documentation_cigna.txt",
        "denial_reason": "insufficient_documentation",
        "payer": "Cigna",
        "drug": "semaglutide (Ozempic)",
        "note_type": "progress_note",
        "patient": {
            "name": "Maria T. Reyes",
            "age": 38,
            "sex": "female",
            "bmi": 33,
            "diagnoses": ["R73.09", "E66.01"],
            "comorbidities": ["prediabetes", "obesity"]
        }
    },
    {
        "case_id": "case_004",
        "denial_file": "denial_04_off_label_bluecross_blueshield.txt",
        "denial_reason": "off_label",
        "payer": "BlueCross BlueShield",
        "drug": "liraglutide (Saxenda)",
        "note_type": "specialist_consult",
        "patient": {
            "name": "David K. Nguyen",
            "age": 60,
            "sex": "male",
            "bmi": 30,
            "diagnoses": ["G47.33", "E66.09"],
            "comorbidities": ["sleep apnea", "obesity"]
        }
    },
    {
        "case_id": "case_005",
        "denial_file": "denial_05_alternative_covered_humana.txt",
        "denial_reason": "alternative_covered",
        "payer": "Humana",
        "drug": "semaglutide (Wegovy)",
        "note_type": "progress_note",
        "patient": {
            "name": "Ashley R. Patel",
            "age": 41,
            "sex": "female",
            "bmi": 37,
            "diagnoses": ["E28.2", "E66.01"],
            "comorbidities": ["PCOS", "obesity"]
        }
    },
    {
        "case_id": "case_006",
        "denial_file": "denial_06_step_therapy_not_completed_cigna.txt",
        "denial_reason": "step_therapy_not_completed",
        "payer": "Cigna",
        "drug": "tirzepatide (Zepbound)",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Sandra K. Williams",
            "age": 49,
            "sex": "female",
            "bmi": 36,
            "diagnoses": ["E03.9", "E66.01"],
            "comorbidities": ["hypothyroidism", "obesity"]
        }
    },
    {
        "case_id": "case_007",
        "denial_file": "denial_07_not_medically_necessary_bluecross_blueshield.txt",
        "denial_reason": "not_medically_necessary",
        "payer": "BlueCross BlueShield",
        "drug": "semaglutide (Wegovy)",
        "note_type": "progress_note",
        "patient": {
            "name": "James T. Morrison",
            "age": 55,
            "sex": "male",
            "bmi": 31,
            "diagnoses": ["E66.09", "Z68.31"],
            "comorbidities": ["obesity", "BMI 31-31.9"]
        }
    },
    {
        "case_id": "case_008",
        "denial_file": "denial_08_insufficient_documentation_aetna.txt",
        "denial_reason": "insufficient_documentation",
        "payer": "Aetna",
        "drug": "tirzepatide (Zepbound)",
        "note_type": "progress_note",
        "patient": {
            "name": "Rachel M. Chen",
            "age": 33,
            "sex": "female",
            "bmi": 39,
            "diagnoses": ["E28.2", "E11.65", "E66.01"],
            "comorbidities": ["PCOS", "insulin resistance", "obesity"]
        }
    },
    {
        "case_id": "case_009",
        "denial_file": "denial_09_not_medically_necessary_humana.txt",
        "denial_reason": "not_medically_necessary",
        "payer": "Humana",
        "drug": "liraglutide (Saxenda)",
        "note_type": "progress_note",
        "patient": {
            "name": "Thomas B. Jackson",
            "age": 61,
            "sex": "male",
            "bmi": 33,
            "diagnoses": ["M17.11", "E66.09"],
            "comorbidities": ["osteoarthritis", "obesity"]
        }
    },
    {
        "case_id": "case_010",
        "denial_file": "denial_10_alternative_covered_unitedhealthcare.txt",
        "denial_reason": "alternative_covered",
        "payer": "UnitedHealthcare",
        "drug": "tirzepatide (Zepbound)",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Patricia L. Davis",
            "age": 44,
            "sex": "female",
            "bmi": 40,
            "diagnoses": ["E11.9", "I10", "E66.01"],
            "comorbidities": ["type 2 diabetes", "hypertension", "obesity"]
        }
    },
    {
        "case_id": "case_011",
        "denial_file": "denial_11_off_label_cigna.txt",
        "denial_reason": "off_label",
        "payer": "Cigna",
        "drug": "semaglutide (Ozempic)",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Marcus A. Thompson",
            "age": 38,
            "sex": "male",
            "bmi": 29,
            "diagnoses": ["K76.0", "E66.09"],
            "comorbidities": ["non-alcoholic fatty liver disease", "overweight"]
        }
    },
    {
        "case_id": "case_012",
        "denial_file": "denial_12_step_therapy_not_completed_aetna.txt",
        "denial_reason": "step_therapy_not_completed",
        "payer": "Aetna",
        "drug": "tirzepatide (Zepbound)",
        "note_type": "progress_note",
        "patient": {
            "name": "Linda S. Martinez",
            "age": 52,
            "sex": "female",
            "bmi": 37,
            "diagnoses": ["G47.33", "I10", "E66.01"],
            "comorbidities": ["sleep apnea", "hypertension", "obesity"]
        }
    }
]


def generate_clinical_note(scenario):
    patient = scenario["patient"]
    icd_codes = ", ".join([f"{code}" for code in patient["diagnoses"]])
    comorbidities = ", ".join(patient["comorbidities"])
    
    if scenario["note_type"] == "specialist_consult":
        note_format = """Format this as a specialist consultation note with these sections:
- PATIENT / REFERRING PROVIDER / CONSULT DATE header
- REASON FOR CONSULTATION
- HISTORY OF PRESENT ILLNESS (detailed, 2-3 paragraphs)
- PAST MEDICAL HISTORY
- CURRENT MEDICATIONS (include doses)
- REVIEW OF SYSTEMS
- PHYSICAL EXAMINATION (include vitals, BMI)
- ASSESSMENT (use ICD-10 codes)
- PLAN (include specific drug, dose, rationale for why alternatives failed or are inappropriate)
- Signature block"""

    else:
        note_format = """Format this as a primary care progress note with these sections:
- PATIENT / DATE / PROVIDER header
- CHIEF COMPLAINT
- SUBJECTIVE (patient history, prior treatment attempts, symptoms)
- OBJECTIVE (vitals including weight and BMI, relevant exam findings)
- ASSESSMENT (use ICD-10 codes with descriptions)
- PLAN (include specific drug request, dose, clinical rationale, prior therapy tried)
- Signature block"""

    system_prompt = f"""You are a physician documenting a clinical note to support a prior 
authorization request for a GLP-1 medication that was denied by {scenario['payer']}.

The denial reason was: {scenario['denial_reason']}
Your note should contain clinical evidence that directly addresses and counters this denial reason.
For example:
- If denied for step therapy: document previous medications tried, doses, duration, and why they failed
- If denied for not medically necessary: document obesity-related comorbidities, failed conservative measures, clinical urgency
- If denied for insufficient documentation: be exhaustive — include every relevant clinical detail
- If denied for off-label: document clinical literature support and why on-label alternatives are inappropriate

Patient details:
- Name: {patient['name']}
- Age: {patient['age']}, Sex: {patient['sex']}
- BMI: {patient['bmi']} kg/m2
- Primary diagnoses (ICD-10): {icd_codes}
- Comorbidities: {comorbidities}
- Medication requested: {scenario['drug']}

{note_format}

Write in the voice of a real clinician. Use medical terminology. Be specific about 
dates, doses, and durations of prior treatments. Do not add commentary outside the note."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[
            {"role": "user", "content": f"Generate the clinical note for case {scenario['case_id']}"}
        ],
        system=system_prompt
    )

    return message.content[0].text


def save_clinical_note(scenario, note_text, index):
    base_filename = f"note_{index:02d}_{scenario['case_id']}_{scenario['note_type']}"
    
    note_path = f"data/synthetic/clinical_notes/{base_filename}.txt"
    with open(note_path, "w") as f:
        f.write(note_text)
    
    metadata = {
        "filename": f"{base_filename}.txt",
        "case_id": scenario["case_id"],
        "denial_file": scenario["denial_file"],
        "denial_reason": scenario["denial_reason"],
        "payer": scenario["payer"],
        "drug": scenario["drug"],
        "note_type": scenario["note_type"],
        "patient_name": scenario["patient"]["name"],
        "patient_age": scenario["patient"]["age"],
        "patient_bmi": scenario["patient"]["bmi"],
        "diagnoses": scenario["patient"]["diagnoses"],
        "comorbidities": scenario["patient"]["comorbidities"]
    }
    
    metadata_path = f"data/synthetic/clinical_notes/{base_filename}.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Saved: {base_filename}")


def main():
    print("Generating clinical notes...")
    
    for index, scenario in enumerate(CLINICAL_SCENARIOS, start=1):
        print(f"Generating {index}/{len(CLINICAL_SCENARIOS)}: {scenario['case_id']} — {scenario['note_type']} — {scenario['payer']}")
        
        note_text = generate_clinical_note(scenario)
        save_clinical_note(scenario, note_text, index)
    
    print(f"\nDone. {len(CLINICAL_SCENARIOS)} clinical notes saved to data/synthetic/clinical_notes/")

if __name__ == "__main__":
    main()