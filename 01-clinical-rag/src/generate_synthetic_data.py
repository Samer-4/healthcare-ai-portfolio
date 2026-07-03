import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


CASES = [
    {
        "case_id": "case_001",
        "payer": "Aetna",
        "drug": "semaglutide (Wegovy)",
        "denial_reason": "step_therapy_not_completed",
        "appeal_tier": "strong_appeal",
        "format": "formal_letter",
        "note_type": "progress_note",
        "patient": {
            "name": "Jennifer L. Caldwell",
            "mrn": "MRN-100234",
            "age": 45,
            "sex": "female",
            "bmi": 38,
            "diagnoses": ["E11.9", "E66.01"],
            "comorbidities": ["type 2 diabetes", "hypertension"],
        },
        "physician": {"name": "Dr. Susan Ramirez, MD", "npi": "1740291856", "specialty": "Internal Medicine"},
    },
    {
        "case_id": "case_002",
        "payer": "UnitedHealthcare",
        "drug": "tirzepatide (Zepbound)",
        "denial_reason": "not_medically_necessary",
        "appeal_tier": "strong_appeal",
        "format": "formal_letter",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Robert M. Okafor",
            "mrn": "MRN-100235",
            "age": 52,
            "sex": "male",
            "bmi": 35,
            "diagnoses": ["I10", "E66.09"],
            "comorbidities": ["hypertension", "obesity"],
        },
        "physician": {"name": "Dr. Andrew Kim, MD", "npi": "1922048173", "specialty": "Endocrinology"},
    },
    {
        "case_id": "case_003",
        "payer": "Cigna",
        "drug": "semaglutide (Ozempic)",
        "denial_reason": "insufficient_documentation",
        "appeal_tier": "weak_appeal",
        "format": "formal_letter",
        "note_type": "progress_note",
        "patient": {
            "name": "Maria T. Reyes",
            "mrn": "MRN-100236",
            "age": 38,
            "sex": "female",
            "bmi": 33,
            "diagnoses": ["R73.09", "E66.01"],
            "comorbidities": ["prediabetes", "obesity"],
        },
        "physician": {"name": "Dr. Priya Nandakumar, MD", "npi": "1685720349", "specialty": "Family Medicine"},
    },
    {
        "case_id": "case_004",
        "payer": "BlueCross BlueShield",
        "drug": "liraglutide (Saxenda)",
        "denial_reason": "off_label",
        "appeal_tier": "weak_appeal",
        "format": "formal_letter",
        "note_type": "specialist_consult",
        "patient": {
            "name": "David K. Nguyen",
            "mrn": "MRN-100237",
            "age": 60,
            "sex": "male",
            "bmi": 30,
            "diagnoses": ["G47.33", "E66.09"],
            "comorbidities": ["sleep apnea", "obesity"],
        },
        "physician": {"name": "Dr. Lauren Mackey, MD", "npi": "1408857261", "specialty": "Sleep Medicine"},
    },
    {
        "case_id": "case_005",
        "payer": "Humana",
        "drug": "semaglutide (Wegovy)",
        "denial_reason": "alternative_covered",
        "appeal_tier": "strong_appeal",
        "format": "formal_letter",
        "note_type": "progress_note",
        "patient": {
            "name": "Ashley R. Patel",
            "mrn": "MRN-100238",
            "age": 41,
            "sex": "female",
            "bmi": 37,
            "diagnoses": ["E28.2", "E66.01"],
            "comorbidities": ["PCOS", "obesity"],
        },
        "physician": {"name": "Dr. Karen Ostrowski, MD", "npi": "1233649087", "specialty": "Family Medicine"},
    },
    {
        "case_id": "case_006",
        "payer": "Cigna",
        "drug": "tirzepatide (Zepbound)",
        "denial_reason": "step_therapy_not_completed",
        "appeal_tier": "strong_appeal",
        "format": "portal_message",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Sandra K. Williams",
            "mrn": "MRN-100239",
            "age": 49,
            "sex": "female",
            "bmi": 36,
            "diagnoses": ["E03.9", "E66.01"],
            "comorbidities": ["hypothyroidism", "obesity"],
        },
        "physician": {"name": "Dr. Michael Ferraro, MD", "npi": "1957403812", "specialty": "Endocrinology"},
    },
    {
        "case_id": "case_007",
        "payer": "BlueCross BlueShield",
        "drug": "semaglutide (Wegovy)",
        "denial_reason": "not_medically_necessary",
        "appeal_tier": "no_viable_appeal",
        "format": "fax_partial",
        "note_type": "progress_note",
        "patient": {
            "name": "James T. Morrison",
            "mrn": "MRN-100240",
            "age": 55,
            "sex": "male",
            "bmi": 31,
            "diagnoses": ["E66.09", "Z68.31"],
            "comorbidities": ["obesity", "BMI 31-31.9"],
        },
        "physician": {"name": "Dr. Elaine Wu, MD", "npi": "1609274135", "specialty": "Internal Medicine"},
    },
    {
        "case_id": "case_008",
        "payer": "Aetna",
        "drug": "tirzepatide (Zepbound)",
        "denial_reason": "insufficient_documentation",
        "appeal_tier": "strong_appeal",
        "format": "formal_letter",
        "note_type": "progress_note",
        "patient": {
            "name": "Rachel M. Chen",
            "mrn": "MRN-100241",
            "age": 33,
            "sex": "female",
            "bmi": 39,
            "diagnoses": ["E28.2", "E11.65", "E66.01"],
            "comorbidities": ["PCOS", "insulin resistance", "obesity"],
        },
        "physician": {"name": "Dr. Natalie Brooks, MD", "npi": "1774920568", "specialty": "Family Medicine"},
    },
    {
        "case_id": "case_009",
        "payer": "Humana",
        "drug": "liraglutide (Saxenda)",
        "denial_reason": "not_medically_necessary",
        "appeal_tier": "weak_appeal",
        "format": "formal_letter",
        "note_type": "progress_note",
        "patient": {
            "name": "Thomas B. Jackson",
            "mrn": "MRN-100242",
            "age": 61,
            "sex": "male",
            "bmi": 33,
            "diagnoses": ["M17.11", "E66.09"],
            "comorbidities": ["osteoarthritis", "obesity"],
        },
        "physician": {"name": "Dr. Gregory Alston, MD", "npi": "1361780924", "specialty": "Internal Medicine"},
    },
    {
        "case_id": "case_010",
        "payer": "UnitedHealthcare",
        "drug": "tirzepatide (Zepbound)",
        "denial_reason": "alternative_covered",
        "appeal_tier": "strong_appeal",
        "format": "formal_letter",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Patricia L. Davis",
            "mrn": "MRN-100243",
            "age": 44,
            "sex": "female",
            "bmi": 40,
            "diagnoses": ["E11.9", "I10", "E66.01"],
            "comorbidities": ["type 2 diabetes", "hypertension", "obesity"],
        },
        "physician": {"name": "Dr. Omar Haddad, MD", "npi": "1845067293", "specialty": "Endocrinology"},
    },
    {
        "case_id": "case_011",
        "payer": "Cigna",
        "drug": "semaglutide (Ozempic)",
        "denial_reason": "off_label",
        "appeal_tier": "no_viable_appeal",
        "format": "formal_letter",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Marcus A. Thompson",
            "mrn": "MRN-100244",
            "age": 38,
            "sex": "male",
            "bmi": 29,
            "diagnoses": ["K76.0", "E66.09"],
            "comorbidities": ["non-alcoholic fatty liver disease", "overweight"],
        },
        "physician": {"name": "Dr. Christine Poulos, MD", "npi": "1520639487", "specialty": "Gastroenterology"},
    },
    {
        "case_id": "case_012",
        "payer": "Aetna",
        "drug": "tirzepatide (Zepbound)",
        "denial_reason": "step_therapy_not_completed",
        "appeal_tier": "strong_appeal",
        "format": "formal_letter",
        "note_type": "progress_note",
        "patient": {
            "name": "Linda S. Martinez",
            "mrn": "MRN-100245",
            "age": 52,
            "sex": "female",
            "bmi": 37,
            "diagnoses": ["G47.33", "I10", "E66.01"],
            "comorbidities": ["sleep apnea", "hypertension", "obesity"],
        },
        "physician": {"name": "Dr. Brian Fenwick, MD", "npi": "1093857462", "specialty": "Family Medicine"},
    },
    {
        "case_id": "case_013",
        "payer": "Cigna",
        "drug": "semaglutide (Wegovy)",
        "denial_reason": "non_formulary",
        "appeal_tier": "weak_appeal",
        "format": "portal_message",
        "note_type": "progress_note",
        "patient": {
            "name": "Emily J. Kowalski",
            "mrn": "MRN-100246",
            "age": 29,
            "sex": "female",
            "bmi": 41,
            "diagnoses": ["E66.01", "F33.1", "Z68.41"],
            "comorbidities": ["morbid obesity", "major depressive disorder"],
        },
        "physician": {"name": "Dr. Anita Desai, MD", "npi": "1316248790", "specialty": "Family Medicine"},
    },
    {
        "case_id": "case_014",
        "payer": "UnitedHealthcare",
        "drug": "semaglutide (Ozempic)",
        "denial_reason": "step_therapy_not_completed",
        "appeal_tier": "strong_appeal",
        "format": "formal_letter",
        "note_type": "progress_note",
        "patient": {
            "name": "Carl D. Whitfield",
            "mrn": "MRN-100247",
            "age": 58,
            "sex": "male",
            "bmi": 34,
            "diagnoses": ["E11.65", "I10", "E78.5"],
            "comorbidities": ["type 2 diabetes with hyperglycemia", "hypertension", "hyperlipidemia"],
        },
        "physician": {"name": "Dr. Paul Iverson, MD", "npi": "1487326509", "specialty": "Internal Medicine"},
    },
    {
        "case_id": "case_015",
        "payer": "Aetna",
        "drug": "liraglutide (Saxenda)",
        "denial_reason": "plan_exclusion_weight_loss",
        "appeal_tier": "no_viable_appeal",
        "format": "formal_letter",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Sofia E. Alvarez",
            "mrn": "MRN-100248",
            "age": 36,
            "sex": "female",
            "bmi": 42,
            "diagnoses": ["E66.01", "G47.33", "Z68.41"],
            "comorbidities": ["morbid obesity", "obstructive sleep apnea"],
        },
        "physician": {"name": "Dr. Rebecca Stein, MD", "npi": "1659083241", "specialty": "Bariatric Medicine"},
    },
    {
        "case_id": "case_016",
        "payer": "Humana",
        "drug": "tirzepatide (Mounjaro)",
        "denial_reason": "not_medically_necessary",
        "appeal_tier": "strong_appeal",
        "format": "fax_partial",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Walter H. Simmons",
            "mrn": "MRN-100249",
            "age": 67,
            "sex": "male",
            "bmi": 32,
            "diagnoses": ["E11.9", "N18.3", "I10"],
            "comorbidities": ["type 2 diabetes", "chronic kidney disease stage 3", "hypertension"],
        },
        "physician": {"name": "Dr. Farida Osman, MD", "npi": "1902471835", "specialty": "Nephrology"},
    },
    {
        "case_id": "case_017",
        "payer": "BlueCross BlueShield",
        "drug": "semaglutide (Rybelsus)",
        "denial_reason": "step_therapy_not_completed",
        "appeal_tier": "weak_appeal",
        "format": "formal_letter",
        "note_type": "progress_note",
        "patient": {
            "name": "Dorothy A. Kline",
            "mrn": "MRN-100250",
            "age": 63,
            "sex": "female",
            "bmi": 31,
            "diagnoses": ["E11.9", "M17.0", "E66.09"],
            "comorbidities": ["type 2 diabetes", "bilateral knee osteoarthritis", "obesity"],
        },
        "physician": {"name": "Dr. Steven Barlow, MD", "npi": "1738405926", "specialty": "Internal Medicine"},
    },
    {
        "case_id": "case_018",
        "payer": "Anthem",
        "drug": "semaglutide (Wegovy)",
        "denial_reason": "quantity_limit_exceeded",
        "appeal_tier": "weak_appeal",
        "format": "portal_message",
        "note_type": "progress_note",
        "patient": {
            "name": "Derek O. Boateng",
            "mrn": "MRN-100251",
            "age": 47,
            "sex": "male",
            "bmi": 38,
            "diagnoses": ["E66.01", "G47.33", "I10"],
            "comorbidities": ["obesity", "sleep apnea", "hypertension"],
        },
        "physician": {"name": "Dr. Monica Reyes-Chan, MD", "npi": "1264097385", "specialty": "Family Medicine"},
    },
    {
        "case_id": "case_019",
        "payer": "Cigna",
        "drug": "tirzepatide (Zepbound)",
        "denial_reason": "not_medically_necessary",
        "appeal_tier": "strong_appeal",
        "format": "formal_letter",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Barbara N. Fitzgerald",
            "mrn": "MRN-100252",
            "age": 55,
            "sex": "female",
            "bmi": 34,
            "diagnoses": ["E66.09", "I25.10", "E78.5"],
            "comorbidities": ["obesity", "coronary artery disease", "hyperlipidemia"],
        },
        "physician": {"name": "Dr. Hassan Qureshi, MD", "npi": "1573820946", "specialty": "Cardiology"},
    },
    {
        "case_id": "case_020",
        "payer": "UnitedHealthcare",
        "drug": "liraglutide (Saxenda)",
        "denial_reason": "insufficient_documentation",
        "appeal_tier": "weak_appeal",
        "format": "fax_partial",
        "note_type": "progress_note",
        "patient": {
            "name": "Alyssa M. Trần",
            "mrn": "MRN-100253",
            "age": 26,
            "sex": "female",
            "bmi": 36,
            "diagnoses": ["E66.01", "E28.2"],
            "comorbidities": ["obesity", "PCOS"],
        },
        "physician": {"name": "Dr. Janet Moreau, MD", "npi": "1849263057", "specialty": "Family Medicine"},
    },
    {
        "case_id": "case_021",
        "payer": "Aetna",
        "drug": "semaglutide (Ozempic)",
        "denial_reason": "off_label",
        "appeal_tier": "no_viable_appeal",
        "format": "portal_message",
        "note_type": "progress_note",
        "patient": {
            "name": "Kevin R. Sullivan",
            "mrn": "MRN-100254",
            "age": 42,
            "sex": "male",
            "bmi": 30,
            "diagnoses": ["K76.0", "R73.03", "E66.09"],
            "comorbidities": ["non-alcoholic fatty liver disease", "prediabetes", "obesity"],
        },
        "physician": {"name": "Dr. Leonard Achebe, MD", "npi": "1420685379", "specialty": "Gastroenterology"},
    },
    {
        "case_id": "case_022",
        "payer": "Kaiser Permanente",
        "drug": "semaglutide (Wegovy)",
        "denial_reason": "step_therapy_not_completed",
        "appeal_tier": "strong_appeal",
        "format": "formal_letter",
        "note_type": "progress_note",
        "patient": {
            "name": "Gloria P. Mendoza",
            "mrn": "MRN-100255",
            "age": 50,
            "sex": "female",
            "bmi": 39,
            "diagnoses": ["E66.01", "I10", "E78.5"],
            "comorbidities": ["obesity", "hypertension", "hyperlipidemia"],
        },
        "physician": {"name": "Dr. Timothy Rourke, MD", "npi": "1596047283", "specialty": "Internal Medicine"},
    },
    {
        "case_id": "case_023",
        "payer": "Humana",
        "drug": "tirzepatide (Zepbound)",
        "denial_reason": "insufficient_documentation",
        "appeal_tier": "strong_appeal",
        "format": "portal_message",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Frank J. Delgado",
            "mrn": "MRN-100256",
            "age": 59,
            "sex": "male",
            "bmi": 35,
            "diagnoses": ["E66.09", "G47.33", "I48.91"],
            "comorbidities": ["obesity", "sleep apnea", "atrial fibrillation"],
        },
        "physician": {"name": "Dr. Vivian Cho, MD", "npi": "1387250614", "specialty": "Sleep Medicine"},
    },
    {
        "case_id": "case_024",
        "payer": "BlueCross BlueShield",
        "drug": "semaglutide (Wegovy)",
        "denial_reason": "alternative_covered",
        "appeal_tier": "weak_appeal",
        "format": "formal_letter",
        "note_type": "progress_note",
        "patient": {
            "name": "Nicole B. Harrington",
            "mrn": "MRN-100257",
            "age": 44,
            "sex": "female",
            "bmi": 36,
            "diagnoses": ["E66.01", "M17.11", "R73.03"],
            "comorbidities": ["obesity", "right knee osteoarthritis", "prediabetes"],
        },
        "physician": {"name": "Dr. Marcus Feldman, MD", "npi": "1750392468", "specialty": "Family Medicine"},
    },
    {
        "case_id": "case_025",
        "payer": "Cigna",
        "drug": "liraglutide (Saxenda)",
        "denial_reason": "quantity_limit_exceeded",
        "appeal_tier": "weak_appeal",
        "format": "formal_letter",
        "note_type": "progress_note",
        "patient": {
            "name": "Antonio V. Russo",
            "mrn": "MRN-100258",
            "age": 39,
            "sex": "male",
            "bmi": 40,
            "diagnoses": ["E66.01", "I10", "Z68.41"],
            "comorbidities": ["morbid obesity", "hypertension"],
        },
        "physician": {"name": "Dr. Ingrid Halvorsen, MD", "npi": "1602849371", "specialty": "Internal Medicine"},
    },
    {
        "case_id": "case_026",
        "payer": "Aetna",
        "drug": "semaglutide (Rybelsus)",
        "denial_reason": "not_medically_necessary",
        "appeal_tier": "strong_appeal",
        "format": "fax_partial",
        "note_type": "progress_note",
        "patient": {
            "name": "Margaret E. O'Rourke",
            "mrn": "MRN-100259",
            "age": 66,
            "sex": "female",
            "bmi": 33,
            "diagnoses": ["E11.9", "E78.2", "I10"],
            "comorbidities": ["type 2 diabetes", "mixed hyperlipidemia", "hypertension"],
        },
        "physician": {"name": "Dr. Charles Lindqvist, MD", "npi": "1934706258", "specialty": "Internal Medicine"},
    },
    {
        "case_id": "case_027",
        "payer": "UnitedHealthcare",
        "drug": "tirzepatide (Zepbound)",
        "denial_reason": "plan_exclusion_weight_loss",
        "appeal_tier": "no_viable_appeal",
        "format": "formal_letter",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Brandon T. Ellison",
            "mrn": "MRN-100260",
            "age": 35,
            "sex": "male",
            "bmi": 43,
            "diagnoses": ["E66.01", "G47.33", "K76.0"],
            "comorbidities": ["morbid obesity", "sleep apnea", "non-alcoholic fatty liver disease"],
        },
        "physician": {"name": "Dr. Yolanda Pierce, MD", "npi": "1275839406", "specialty": "Bariatric Medicine"},
    },
    {
        "case_id": "case_028",
        "payer": "Anthem",
        "drug": "semaglutide (Ozempic)",
        "denial_reason": "alternative_covered",
        "appeal_tier": "strong_appeal",
        "format": "formal_letter",
        "note_type": "progress_note",
        "patient": {
            "name": "Denise W. Abernathy",
            "mrn": "MRN-100261",
            "age": 57,
            "sex": "female",
            "bmi": 32,
            "diagnoses": ["E11.9", "E66.09"],
            "comorbidities": ["type 2 diabetes", "obesity"],
        },
        "physician": {"name": "Dr. Raj Venkataraman, MD", "npi": "1468025793", "specialty": "Endocrinology"},
    },
    {
        "case_id": "case_029",
        "payer": "Humana",
        "drug": "semaglutide (Wegovy)",
        "denial_reason": "off_label",
        "appeal_tier": "no_viable_appeal",
        "format": "formal_letter",
        "note_type": "specialist_consult",
        "patient": {
            "name": "Harold G. Weinstein",
            "mrn": "MRN-100262",
            "age": 71,
            "sex": "male",
            "bmi": 29,
            "diagnoses": ["I25.10", "E66.3", "E78.5"],
            "comorbidities": ["coronary artery disease", "overweight", "hyperlipidemia"],
        },
        "physician": {"name": "Dr. Sylvia Marchetti, MD", "npi": "1815394027", "specialty": "Cardiology"},
    },
    {
        "case_id": "case_030",
        "payer": "BlueCross BlueShield",
        "drug": "tirzepatide (Zepbound)",
        "denial_reason": "step_therapy_not_completed",
        "appeal_tier": "weak_appeal",
        "format": "portal_message",
        "note_type": "progress_note",
        "patient": {
            "name": "Tiffany S. Okonkwo",
            "mrn": "MRN-100263",
            "age": 31,
            "sex": "female",
            "bmi": 37,
            "diagnoses": ["E66.01", "E28.2", "R73.03"],
            "comorbidities": ["obesity", "PCOS", "prediabetes"],
        },
        "physician": {"name": "Dr. Adam Kowalczyk, MD", "npi": "1529476380", "specialty": "Family Medicine"},
    },
]


def generate_denial_letter(case):
    patient = case["patient"]
    physician = case["physician"]
    format_type = case["format"]
    patient_summary = f"{patient['age']}-year-old {patient['sex']}, BMI {patient['bmi']}, {', '.join(patient['comorbidities'])}"

    identity_block = f"""Use these exact identifiers throughout — do not invent different ones:
- Patient name: {patient['name']}
- Patient member ID / MRN: {patient['mrn']}
- Prescribing physician: {physician['name']} ({physician['specialty']}), NPI {physician['npi']}"""

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
        format_instructions = f"""Format this as a formal denial letter with:
- Payer letterhead (name, address, phone, fax)
- Date and reference number
- Patient name and member ID / MRN
- Prescribing physician name and NPI
- Specific policy citation (make it realistic e.g. "Clinical Policy Bulletin 0580")
- Clinical rationale for the denial
- Appeal rights and instructions (timeframe, address, what to include)
Write in the formal voice of {case['payer']}. Be specific and realistic."""

    system_prompt = f"""You are a utilization management reviewer at {case['payer']}.
Generate a realistic prior authorization denial for a GLP-1 medication request.

Drug requested: {case['drug']}
Denial reason: {case['denial_reason']}

{identity_block}

{format_instructions}

Do not add any commentary outside the denial itself."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": f"Generate the denial for this patient: {patient_summary}"}
        ],
        system=system_prompt
    )

    return message.content[0].text


def generate_clinical_note(case):
    patient = case["patient"]
    physician = case["physician"]
    icd_codes = ", ".join(patient["diagnoses"])
    comorbidities = ", ".join(patient["comorbidities"])

    if case["appeal_tier"] == "strong_appeal":
        tier_instructions = """This is a STRONG appeal case: the chart genuinely contains everything needed
to overturn the denial. The note must directly and completely counter the denial reason:
- If denied for step therapy: document each previous medication tried with drug, dose, duration, dates, and why it failed or was not tolerated
- If denied for not medically necessary: document obesity-related comorbidities with objective findings, failed conservative measures (supervised diet, exercise program, dietitian referral with dates), and clinical urgency
- If denied for insufficient documentation: be exhaustive — include every relevant clinical detail
- If denied for off-label: document guideline and literature support and why on-label alternatives are inappropriate
- If denied because an alternative is covered or the drug is non-formulary: document that the covered alternative was tried and failed or is contraindicated, with specifics
- If denied for quantity limits: document the clinical justification for the prescribed dose and quantity
- If denied for a plan exclusion: document the severe comorbidity burden supporting a benefit exception"""

    elif case["appeal_tier"] == "weak_appeal":
        tier_instructions = """This is a WEAK appeal case: the chart contains some supporting evidence, but
with real gaps. Partially address the denial reason — include one or two relevant facts, but
leave the documentation incomplete: mention a prior medication without dose or duration,
reference lifestyle changes without specifics or dates, note a comorbidity without severity
or objective findings. Do NOT fully satisfy the payer's criteria. A utilization reviewer
reading this note should find it suggestive but insufficient on its own."""

    else:  # no_viable_appeal
        tier_instructions = """This is a NO-VIABLE-APPEAL case: the chart genuinely lacks the evidence
needed to counter the denial. Write a realistic, competent note for this visit, but the
record must NOT contain what the payer requires: no prior step-therapy medications
documented, no failed or contraindicated covered alternatives, borderline severity,
criteria unmet. Do not invent supporting evidence — the honest clinical picture here
simply does not support the appeal."""

    identity_block = f"""Use these exact identifiers throughout — do not invent different ones:
- Patient name: {patient['name']}
- Patient MRN: {patient['mrn']}
- Author / signing physician: {physician['name']} ({physician['specialty']}), NPI {physician['npi']}"""

    if case["note_type"] == "specialist_consult":
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

    system_prompt = f"""You are a physician documenting a clinical note for a patient whose GLP-1
prior authorization request was denied by {case['payer']}.

The denial reason was: {case['denial_reason']}

{tier_instructions}

{identity_block}

Patient details:
- Age: {patient['age']}, Sex: {patient['sex']}
- BMI: {patient['bmi']} kg/m2
- Primary diagnoses (ICD-10): {icd_codes}
- Comorbidities: {comorbidities}
- Medication requested: {case['drug']}

{note_format}

Write in the voice of a real clinician. Use medical terminology. Be specific about
dates, doses, and durations of prior treatments. Do not add commentary outside the note."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[
            {"role": "user", "content": f"Generate the clinical note for case {case['case_id']}"}
        ],
        system=system_prompt
    )

    return message.content[0].text


def save_case(case, denial_text, note_text):
    case_id = case["case_id"]
    patient = case["patient"]

    denial_filename = f"{case_id}_denial"
    note_filename = f"{case_id}_note"

    with open(f"data/synthetic/denials/{denial_filename}.txt", "w") as f:
        f.write(denial_text)

    with open(f"data/synthetic/clinical_notes/{note_filename}.txt", "w") as f:
        f.write(note_text)

    shared_fields = {
        "case_id": case_id,
        "patient_name": patient["name"],
        "patient_mrn": patient["mrn"],
        "payer": case["payer"],
        "drug": case["drug"],
        "denial_reason": case["denial_reason"],
        "appeal_tier": case["appeal_tier"],
    }

    denial_metadata = {
        **shared_fields,
        "filename": f"{denial_filename}.txt",
        "format": case["format"],
        "note_file": f"{note_filename}.txt",
    }
    with open(f"data/synthetic/denials/{denial_filename}.json", "w") as f:
        json.dump(denial_metadata, f, indent=2)

    note_metadata = {
        **shared_fields,
        "filename": f"{note_filename}.txt",
        "note_type": case["note_type"],
        "denial_file": f"{denial_filename}.txt",
        "patient_age": patient["age"],
        "patient_bmi": patient["bmi"],
        "diagnoses": patient["diagnoses"],
        "comorbidities": patient["comorbidities"],
    }
    with open(f"data/synthetic/clinical_notes/{note_filename}.json", "w") as f:
        json.dump(note_metadata, f, indent=2)

    print(f"Saved: {denial_filename} + {note_filename}")


def main():
    print("Generating synthetic GLP-1 denial letters + clinical notes...")

    for index, case in enumerate(CASES, start=1):
        print(f"Case {index}/{len(CASES)}: {case['case_id']} — {case['payer']} — {case['denial_reason']}")

        denial_text = generate_denial_letter(case)
        note_text = generate_clinical_note(case)
        save_case(case, denial_text, note_text)

    print(f"\nDone. {len(CASES)} matched denial/note pairs saved to "
          f"data/synthetic/denials/ and data/synthetic/clinical_notes/")


if __name__ == "__main__":
    main()
