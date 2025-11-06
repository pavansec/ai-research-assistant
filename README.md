# 🤖 AI Research & Report Generation Assistant

This project is an AI-powered assistant that automates the entire academic research workflow. It leverages an **agentic AI architecture** built with **LangGraph** to transform a simple user-provided topic into a comprehensive, formatted research report.

The system autonomously finds relevant papers, extracts their content, uses the **Gemini API** for deep analysis and comparison, and generates a structured `.docx` file summarizing the current state, methodologies, key findings, and future work for the given topic.

## 🏛️ System Architecture

The workflow is orchestrated by a multi-agent system defined in LangGraph. Each agent has a specialized role, passing its findings to the next agent in a stateful, collaborative process.

<img width="811" height="609" alt="architecture_diagram png" src="https://github.com/user-attachments/assets/9387381c-d2be-4ab4-bc38-8f5be4fbeac8" />


## ✨ Features

* **Topic-Based Research:** Starts the entire workflow from a single topic string.
* **Multi-Source Retrieval:** Autonomously queries the **Semantic Scholar** and **arXiv** APIs to find relevant, open-access research papers.
* **Automated PDF Parsing:** Downloads identified PDFs, extracts their full text using `pdfplumber`, and cleans up temporary files.
* **AI-Powered Analysis (Multi-Agent):**
    * **Summarizer Agent:** Uses the Gemini API to analyze each paper individually, extracting its summary, methodology, and key findings.
    * **Comparator Agent:** Uses the Gemini API to analyze all summaries collectively, generating two key sections:
        1.  **Topic Overview:** A synthesized summary of the topic's current state, common methods, performance metrics, and future work based on *all* papers.
        2.  **Detailed Comparison:** A point-by-point comparison of the papers' objectives, approaches, and results.
* **Structured Report Generation:** Dynamically creates a well-formatted `.docx` report with headings, bold sub-topics, bullet points, and a list of source URLs.
* **Web Interface:** A simple HTML/JS frontend communicates with a **FastAPI** backend, which runs the complex workflow asynchronously in the background.

## 🛠️ Technology Stack

* **Backend:** FastAPI, Uvicorn
* **AI Orchestration:** LangGraph
* **AI Model:** Google Gemini API (`gemini-2.5-flash` via Google AI Studio)
* **Data Sources:** Semantic Scholar API, arXiv API
* **Core Python Libraries:**
    * `google-generativeai`
    * `requests`
    * `pdfplumber`
    * `python-docx`
    * `arxiv`
* **Frontend:** HTML, CSS, JavaScript (served via `index.html`)
* **Automation (Triggering):** n8n (Community Edition)

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

* [Python 3.9+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)
* A code editor like [VS Code](https://code.visualstudio.com/)

### 1. Clone the Repository

```bash
git clone [https://github.com/pavansec/ai-research-assistant}

```
2. Create and Activate Virtual Environment
Windows:

```Bash

python -m venv venv
.\venv\Scripts\activate
```
macOS / Linux:

```Bash

python3 -m venv venv
source venv/bin/activate
```

3. Install Dependencies
Install all the required Python packages from the requirements.txt file.

```Bash

pip install -r requirements.txt
```
4. Set Up API Keys
You must provide your own API keys for the project to function.

Gemini API Key:

Get your key from Google AI Studio.

Open main_graph.py.

Find the line GEMINI_API_KEY = "YOUR_GEMINI_API_KEY" and replace the placeholder with your key.

Semantic Scholar API Key:

Request a key from the Semantic Scholar API page.

Open main_graph.py.

Find the line SEMANTIC_SCHOLAR_API_KEY = "YOUR_SEMANTIC_SCHOLAR_API_KEY" and replace the placeholder with your key.

🏃‍♂️ How to Run
Start the Backend API Server: In your terminal (with the venv active), run the Uvicorn server:

```Bash

uvicorn api_server:app --reload
```
The server will be running at http://127.0.0.1:8000.

Open the Frontend:

Navigate to your project folder in your file explorer.

Double-click the index.html file to open it in your default web browser.

Use the Application:

Type a research topic into the input field (e.g., "Fake News Detection using Natural Language Processing").

Click the "Generate Report" button.

Wait for the status to update. The workflow will run in the background.

When complete, the final .docx report will automatically download.

## 📁 Project Structure

```text
ai_research_assistant/
├── .gitignore
├── api_server.py           # The FastAPI backend server
├── index.html              # The HTML/JS frontend
├── main_graph.py           # The core LangGraph agent workflow
├── requirements.txt        # Python package dependencies
├── README.md               # This file
├── downloaded_pdfs/        # (Temporary folder for PDFs, created automatically)
└── venv/                   # (Python virtual environment)
