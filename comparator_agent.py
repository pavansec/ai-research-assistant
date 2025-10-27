import google.generativeai as genai
import os
import json # For structured output parsing later if needed

# --- Configuration ---
API_KEY = "" # <-- PUT YOUR GEMINI API KEY HERE
MODEL_NAME = "models/gemini-2.5-flash" # Use the model confirmed in Step 1

# --- Define the Comparator Agent Function ---
def compare_paper_analyses(analysis_list: list):
    """
    Compares analyses (summary, methodology, findings) from multiple papers using Gemini.

    Args:
        analysis_list: A list of dictionaries, where each dictionary contains
                       'summary', 'methodology', and 'key_findings' for one paper.

    Returns:
        A string containing the comparative analysis, or None if an error occurs.
    """
    print(f"\n--- Running Comparator Agent ---")
    print(f"Received analyses for {len(analysis_list)} papers.")

    if not API_KEY or API_KEY == "YOUR_API_KEY":
        print("ERROR: Gemini API Key not set. Please update the script.")
        print("--- Comparator Agent Failed ---")
        return None
    if not analysis_list or len(analysis_list) < 2:
        print("ERROR: Need analyses from at least two papers to compare.")
        print("--- Comparator Agent Failed ---")
        return None

    comparison_text = None
    try:
        # --- Configure Gemini ---
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(MODEL_NAME)

        # --- Prepare Input Text for Comparison ---
        comparison_input = "Please provide a comparative analysis of the following research paper summaries:\n\n"
        for i, analysis in enumerate(analysis_list):
            comparison_input += f"--- Paper {i+1} ---\n"
            comparison_input += f"Summary: {analysis.get('summary', 'N/A')}\n"
            comparison_input += f"Methodology: {analysis.get('methodology', 'N/A')}\n"
            comparison_input += f"Key Findings: {analysis.get('key_findings', 'N/A')}\n\n"

        # --- Create the Prompt ---
        prompt = f"""{comparison_input}
--- Comparative Analysis Task ---
Compare the papers based on their summaries, methodologies, and key findings. Highlight:
1.  **Similarities:** Any common goals, methods, or conclusions.
2.  **Differences:** Contrasting approaches, findings, or scope.
3.  **Overall Theme/Contribution:** What is the main area these papers contribute to?

Provide a concise comparative analysis.
"""
        print("Sending request to Gemini API for comparison...")

        # --- Call Gemini API ---
        # Increase timeout if comparing many summaries
        request_options = {"timeout": 120} # Timeout in seconds
        response = model.generate_content(prompt, request_options=request_options)

        # --- Process the Response ---
        if response.parts:
            comparison_text = response.text
            print("Received comparison from Gemini.")
        elif response.prompt_feedback:
             print(f"Gemini request blocked due to: {response.prompt_feedback.block_reason}")
             if response.prompt_feedback.safety_ratings:
                 print("Safety Ratings:")
                 for rating in response.prompt_feedback.safety_ratings:
                      print(f"  - {rating.category}: {rating.probability}")
        else:
             print("Received an empty response from Gemini for comparison.")


    except Exception as e:
        print(f"\n--- Error during Gemini API request for comparison ---")
        print(f"Error details: {type(e).__name__} - {e}")
        print("Troubleshooting tips:")
        print(" - Check your Gemini API Key and internet connection.")
        print(" - The combined input text might be too long or contain issues.")
        print(f" - Ensure the model '{MODEL_NAME}' is correct.")
        print("-----------------------------------------------------")
        return None # Return None on error

    print("--- Comparator Agent Complete ---")
    return comparison_text

# --- Run a Test ---
if __name__ == "__main__":
    # --- Sample Analysis 1 (Use the output from previous step) ---
    # Manually copy the output from the summarizer test run here
    analysis_1 = {
        'summary': """This paper proposes a real-time Sign Language to Speech Conversion system specifically designed for Tamil-speaking communities. The system captures hand gestures via a standard webcam, utilizes MediaPipe for accurate hand landmark detection, and then classifies these gestures using a Convolutional Neural Network (CNN) trained on Tamil sign language. The recognized Tamil alphabets or words are subsequently converted into spoken Tamil using the Google Text-to-Speech (gTTS) API. This accessible and cost-effective solution aims to overcome communication barriers for individuals with hearing or speech impairments in Tamil-speaking regions.""",
        'methodology': """The primary methodology involves a multi-stage machine learning and computer vision approach. It begins with data collection of Tamil sign language gestures using a webcam. Preprocessing involves extracting 21 hand landmarks using MediaPipe and normalizing them. These landmarks are then fed into a Convolutional Neural Network (CNN) for model training and real-time gesture recognition, classifying the gestures into specific Tamil alphabets or words. Finally, the recognized text is converted into spoken Tamil through the Speech Synthesis Module utilizing the gTTS API, enabling real-time audio output.""",
        'key_findings': """1. The system achieved a high accuracy of 92% in controlled settings and 85% in real-world environments for Tamil sign language gesture recognition. 2. It consistently provided speech output with minimal latency, typically within 1-2 seconds after gesture recognition, making it practical for real-time communication."""
    }

    # --- Sample Analysis 2 (Hypothetical related paper) ---
    analysis_2 = {
        'summary': """This study explores the use of Long Short-Term Memory (LSTM) networks combined with computer vision for recognizing dynamic American Sign Language (ASL) gestures from video sequences. It focuses on capturing temporal dependencies in sign movements. The system uses OpenPose for body and hand keypoint extraction and feeds these sequences into an LSTM model for classification. Text-to-speech is handled by a standard offline library.""",
        'methodology': """The methodology uses video input, processed frame-by-frame with OpenPose to extract skeletal keypoints. These time-series keypoint sequences are then fed into a Long Short-Term Memory (LSTM) recurrent neural network trained to classify dynamic ASL gestures. Speech synthesis is done using an offline text-to-speech engine.""",
        'key_findings': """1. The LSTM model achieved 88% accuracy on a dataset of dynamic ASL signs. 2. Capturing temporal information via LSTM significantly outperformed static image classifiers for dynamic gestures. 3. OpenPose keypoints provided a robust feature set, reducing sensitivity to background variations."""
    }

    # --- Combine analyses into a list ---
    test_analyses = [analysis_1, analysis_2]

    # --- Run the comparison ---
    comparison_result = compare_paper_analyses(test_analyses)

    if comparison_result:
        print("\n--- Gemini Comparative Analysis ---")
        print(comparison_result)
        print("-----------------------------------")
    else:
        print("\nNo comparison generated or an error occurred.")