import pdfplumber
import os

def extract_pdf_text(pdf_path):
    print(f"\n{'='*60}")
    print(f"FILE: {pdf_path}")
    print(f"{'='*60}")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages, start=1):
            print(f"\n--- PAGE {i} ---")
            text = page.extract_text()
            if text:
                print(text)
            else:
                print("[NO TEXT EXTRACTED - may be scanned image]")

def main():
    policy_dir = "data/raw/policies"
    
    pdfs = [f for f in os.listdir(policy_dir) if f.endswith(".pdf")]
    
    if not pdfs:
        print("No PDFs found in data/raw/policies/")
        return
    
    print(f"Found {len(pdfs)} PDFs: {pdfs}")
    
    # Just extract the first one for now — observe the output
    first_pdf = os.path.join(policy_dir, pdfs[0])
    extract_pdf_text(first_pdf)

if __name__ == "__main__":
    main()