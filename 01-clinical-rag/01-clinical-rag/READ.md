A RAG pipeline that drafts grounded, citation-backed insurance appeal letters for GLP-1 medication denials [or your chosen area]. Retrieves across three document types — synthetic denial letters, Synthea-generated clinical notes, and public payer policies (CMS + commercial) — to identify contradictions between the stated denial rationale and the insurer's published approval criteria, then generates a structured appeal where every argument traces back to a specific retrieved chunk.

Users: physicians, utilization review nurses, medical billing staff
Data: CMS coverage docs + 3 commercial payer policies for the chosen area; Synthea-generated patient cases; 30+ synthetic denial letters generated for evaluation (de-identified, HIPAA-safe by design)
Eval: primary — argument-to-source traceability rate, denial-reason coverage, policy-citation accuracy (LLM-as-judge w/ rubric); secondary — small qualitative MD spot-check (best-effort)
Live demo: upload denial letter + clinical note → receive appeal letter with side-by-side source panel mapping each paragraph to its retrieved chunk and the specific policy provision it invokes
