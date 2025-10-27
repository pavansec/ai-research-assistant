import pdfplumber
import os # Import os to check if the file exists

# --- Define the Parser Agent Function ---
def extract_text_from_pdf(pdf_file_path: str):
    """
    Extracts all text content from a given PDF file.

    Args:
        pdf_file_path: The path to the PDF file.

    Returns:
        A single string containing all extracted text,
        or None if an error occurs or the file doesn't exist.
    """
    print(f"\n--- Running Parser Agent ---")
    print(f"Attempting to extract text from: '{pdf_file_path}'")

    # --- Check if the file exists ---
    if not os.path.exists(pdf_file_path):
        print(f"ERROR: File not found at path: {pdf_file_path}")
        print("--- Parser Agent Failed ---")
        return None
    if not pdf_file_path.lower().endswith(".pdf"):
        print(f"ERROR: File is not a PDF: {pdf_file_path}")
        print("--- Parser Agent Failed ---")
        return None

    full_text = ""
    try:
        # --- Open the PDF file ---
        with pdfplumber.open(pdf_file_path) as pdf:
            print(f"Successfully opened PDF. Number of pages: {len(pdf.pages)}")

            # --- Extract text from each page ---
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text: # Check if text was actually extracted
                    full_text += page_text + "\n" # Add text and a newline separator
                # else:
                #     print(f"Warning: No text extracted from page {i+1}. It might be image-based.")

            print(f"Finished extracting text. Total characters: {len(full_text)}")

    except Exception as e:
        print(f"\n--- Error during PDF parsing ---")
        print(f"Error details: {type(e).__name__} - {e}")
        print("Troubleshooting tips:")
        print(" - Ensure the file is a valid, non-corrupted PDF.")
        print(" - Some complex PDF layouts or scanned images might cause issues.")
        print(" - Make sure pdfplumber is installed correctly.")
        print("--------------------------------")
        return None # Return None on error

    print("--- Parser Agent Complete ---")
    return full_text

# --- Run a Test ---
if __name__ == "__main__":
    # IMPORTANT: Replace 'sample_paper.pdf' with the actual name
    #            of the PDF file you downloaded into your project folder.
    test_pdf_path = "sample_paper.pdf"

    extracted_content = extract_text_from_pdf(test_pdf_path)

    if extracted_content:
        print("\n--- Extracted Text (First 500 chars) ---")
        print(extracted_content[:500] + "...") # Print only the beginning
        print("-----------------------------------------")
        # Optional: You could save the full text to a file to review it
        with open("extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(extracted_content)
        print("\nFull extracted text saved to 'extracted_text.txt'")
    else:
        print("\nNo text extracted or an error occurred.")