import google.generativeai as genai
import os
import json # For potentially parsing structured output later

# --- Configuration ---
API_KEY = "" # <-- PUT YOUR GEMINI API KEY HERE
MODEL_NAME = "models/gemini-2.5-flash" # Use the model confirmed in Step 1

# --- Define the Summarizer Agent Function ---
def summarize_text_with_gemini(paper_text: str):
    """
    Summarizes the given text using the Gemini API and extracts key info.

    Args:
        paper_text: The full text content of the research paper.

    Returns:
        A dictionary containing 'summary', 'methodology', and 'key_findings',
        or None if an error occurs.
    """
    print(f"\n--- Running Summarizer Agent ---")
    print(f"Received text length: {len(paper_text)} characters.")

    if not API_KEY or API_KEY == "YOUR_API_KEY":
        print("ERROR: Gemini API Key not set. Please update the script.")
        print("--- Summarizer Agent Failed ---")
        return None
    if not paper_text.strip():
        print("ERROR: Input text is empty.")
        print("--- Summarizer Agent Failed ---")
        return None

    analysis_result = None
    try:
        # --- Configure Gemini ---
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(MODEL_NAME)

        # --- Create the Prompt ---
        # This prompt asks for specific pieces of information.
        # We could later ask for JSON output for easier parsing.
        prompt = f"""Analyze the following research paper text and provide:
1.  **Summary:** A concise summary of the paper's objectives, methods, and main conclusions (approx. 3-5 sentences).
2.  **Methodology:** Briefly describe the primary methodology or approach used in the paper.
3.  **Key Findings:** List the most important 2-3 findings or results reported.

--- START OF PAPER TEXT ---
{paper_text[:30000]}
--- END OF PAPER TEXT ---

Provide the output clearly structured under the headings "Summary:", "Methodology:", and "Key Findings:".
"""
        # Note: Truncated input text to 30k chars for this example prompt length.
        # Gemini 1.5 Flash has a large context, but extremely large inputs
        # might still hit processing limits or increase cost/latency in paid tiers.
        # For the free tier and typical papers, this should be fine.
        print("Sending request to Gemini API...")

        # --- Call Gemini API ---
        # Increase timeout if needed for very long documents or slower connections
        request_options = {"timeout": 120} # Timeout in seconds (e.g., 2 minutes)
        response = model.generate_content(prompt, request_options=request_options)

        # --- Process the Response ---
        if response.parts:
            generated_text = response.text
            print("Received response from Gemini.")
            # Basic parsing assumes Gemini follows the structure requested
            # A more robust approach would involve asking for JSON output
            summary = generated_text.split("Methodology:")[0].replace("Summary:", "").strip()
            methodology = generated_text.split("Key Findings:")[0].split("Methodology:")[-1].strip()
            key_findings = generated_text.split("Key Findings:")[-1].strip()

            analysis_result = {
                'summary': summary,
                'methodology': methodology,
                'key_findings': key_findings
            }
        elif response.prompt_feedback:
             print(f"Gemini request blocked due to: {response.prompt_feedback.block_reason}")
             if response.prompt_feedback.safety_ratings:
                 print("Safety Ratings:")
                 for rating in response.prompt_feedback.safety_ratings:
                      print(f"  - {rating.category}: {rating.probability}")
        else:
             print("Received an empty response from Gemini.")


    except Exception as e:
        print(f"\n--- Error during Gemini API request ---")
        print(f"Error details: {type(e).__name__} - {e}")
        print("Troubleshooting tips:")
        print(" - Check your Gemini API Key and internet connection.")
        print(" - The input text might be too long or contain problematic content.")
        print(f" - Ensure the model '{MODEL_NAME}' is correct and available.")
        print(" - Consider increasing the timeout if the error is related to deadlines.")
        print("-------------------------------------")
        return None # Return None on error

    print("--- Summarizer Agent Complete ---")
    return analysis_result

# --- Run a Test ---
if __name__ == "__main__":
    # Load the extracted text from the file saved in Step 3
    input_text_file = "extracted_text.txt" # Assumes you saved the text

    if os.path.exists(input_text_file):
        with open(input_text_file, "r", encoding="utf-8") as f:
            test_paper_content = f.read()

        summary_output = summarize_text_with_gemini(test_paper_content)

        if summary_output:
            print("\n--- Gemini Analysis ---")
            print(f"Summary:\n{summary_output['summary']}\n")
            print(f"Methodology:\n{summary_output['methodology']}\n")
            print(f"Key Findings:\n{summary_output['key_findings']}")
            print("-----------------------")
        else:
            print("\nNo summary generated or an error occurred.")
    else:
        print(f"\nERROR: Input text file '{input_text_file}' not found.")
        print("Please run parser_agent.py first (with saving enabled) or provide valid text.")