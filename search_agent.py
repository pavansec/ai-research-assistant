import requests
import time
import json # Import json for better error message printing

# Semantic Scholar API endpoint for paper search - CORRECTED URL
SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1/paper/search" # <-- Corrected URL

# --- Define the Search Agent Function ---
def search_academic_papers(topic: str, limit: int = 5):
    """
    Searches Semantic Scholar for papers related to a topic.

    Args:
        topic: The research topic string.
        limit: The maximum number of papers to retrieve.

    Returns:
        A list of dictionaries, each containing 'paperId' and 'title',
        or an empty list if an error occurs or no papers are found.
    """
    print(f"\n--- Running Search Agent ---")
    print(f"Searching for topic: '{topic}'")

    papers_found = []

    try:
        # --- Prepare the API Request ---
        params = {
            'query': topic,
            'limit': limit,
            'fields': 'title,paperId' # Request only title and paperId
        }
        headers = {
            'Accept': 'application/json',
            # Add your API key here! Replace the placeholder.
            'x-api-key': "Pjn8hPFeCs62sBhLSUZX42UYCbMQ6nlS4xQgXTgm" # <--- PUT YOUR KEY HERE
        }

        # IMPORTANT: Check if the key placeholder is still there before running
        if headers.get('x-api-key') == "YOUR_SEMANTIC_SCHOLAR_API_KEY":
            print("\nERROR: Please replace 'YOUR_SEMANTIC_SCHOLAR_API_KEY' with your actual key!")
            print("--- Search Agent Failed ---")
            return [] # Stop if key is not set

        # --- Make the API Call ---
        print(f"Querying Semantic Scholar API...")
        # Add a small delay before the request to respect rate limits preemptively
        time.sleep(1.1) # Sleep for slightly more than 1 second
        response = requests.get(SEMANTIC_SCHOLAR_API_URL, params=params, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # --- Process the Response ---
        results = response.json()

        if results and 'data' in results and results['data']:
            print(f"Found {len(results['data'])} papers.")
            for paper in results['data']:
                # Ensure both paperId and title exist before adding
                if paper.get('paperId') and paper.get('title'):
                    papers_found.append({
                        'paperId': paper['paperId'],
                        'title': paper['title']
                    })
        elif results and 'data' in results and not results['data']:
             print("No papers found matching the topic.")
        else:
            # Handle unexpected response structure
            print("Received an unexpected response format from Semantic Scholar.")
            print(f"Response: {json.dumps(results, indent=2)}")


    except requests.exceptions.HTTPError as http_err:
        print(f"\n--- HTTP Error during Semantic Scholar API request ---")
        print(f"Status Code: {http_err.response.status_code}")
        try:
            error_details = http_err.response.json()
            print(f"API Response: {json.dumps(error_details, indent=2)}")
        except json.JSONDecodeError:
            print(f"API Response Text: {http_err.response.text}")
        print("Troubleshooting tips:")
        print(" - Double-check your Semantic Scholar API Key.")
        if http_err.response.status_code == 401 or http_err.response.status_code == 403:
             print("   - Ensure your API key is correct and valid.")
        elif http_err.response.status_code == 429:
             print("   - You might be making requests too fast, even with a key. Ensure sufficient delay.")
        print(" - Verify the API endpoint and parameters are correct.")
        print("-------------------------------------------------------")
        return [] # Return empty list on HTTP error

    except requests.exceptions.RequestException as e:
        print(f"\n--- Network Error during Semantic Scholar API request ---")
        print(f"Error details: {e}")
        print("Troubleshooting tips:")
        print(" - Check your internet connection.")
        print(" - Ensure the Semantic Scholar API URL is correct and reachable.")
        print("---------------------------------------------------------")
        return [] # Return empty list on network error

    except Exception as e:
        print(f"\n--- An unexpected error occurred in Search Agent ---")
        print(f"Error details: {type(e).__name__} - {e}")
        print("---------------------------------------------------")
        return [] # Return empty list on unexpected error

    print("--- Search Agent Complete ---")
    return papers_found

# --- Run a Test ---
if __name__ == "__main__":
    test_topic = "Agentic AI workflows using LangGraph" # Example topic
    # Use the actual API key provided by the user for the test run
    # (Make sure the user replaces the placeholder above)
    found_papers = search_academic_papers(test_topic, limit=5)

    if found_papers:
        print("\n--- Search Results ---")
        for i, paper in enumerate(found_papers):
            print(f"{i+1}. Title: {paper['title']}")
            print(f"   Paper ID: {paper['paperId']}")
        print("--------------------")
    else:
        print("\nNo results to display or an error occurred.")