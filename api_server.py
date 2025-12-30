from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware # <--- Ensure this import is present
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import uuid # To generate unique IDs for concurrent runs

# --- Import necessary components from main_graph ---
# Make sure main_graph.py is in the same directory
try:
    from main_graph import app as langgraph_app # The compiled LangGraph app
    from main_graph import ResearchState # Import the state definition
    # Import any other necessary setup if needed, but the compiled app should be enough
except ImportError:
    print("ERROR: Could not import 'app' or 'ResearchState' from main_graph.py.")
    print("Ensure main_graph.py is in the same directory and has no errors.")
    # Define a placeholder app to allow server startup for debugging imports
    langgraph_app = None
    ResearchState = dict # Placeholder
except Exception as e:
    print(f"ERROR: An unexpected error occurred during import from main_graph: {e}")
    langgraph_app = None
    ResearchState = dict

# --- Define API Request Body ---
class ResearchRequest(BaseModel):
    topic: str
    paper_limit: int = 3 # Default paper limit

# --- Initialize FastAPI ---
app = FastAPI(
    title="AI Research Assistant API",
    description="API to trigger the agentic research workflow."
)

# --- Configure CORS (THIS IS THE ADDED SECTION) ---
# Allow requests from all origins (simplest for local testing)
origins = [
    "*", # Allows all origins
    "null", # Important for requests originating from local files (file://)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"], # Allow all headers
)
# --- END OF ADDED CORS SECTION ---
app.mount("/static", StaticFiles(directory="."), name="static")

# --- In-memory storage for results (simple approach for this project) ---
# ... (rest of the code remains exactly the same as you posted) ...
task_results = {}

# --- Background Task Function ---
def run_research_workflow(task_id: str, topic: str, paper_limit: int):
    """Runs the LangGraph workflow in the background and stores the result."""
    if not langgraph_app:
         task_results[task_id] = {"status": "error", "report_path": None, "error_message": "LangGraph app not loaded."}
         return

    print(f"\n--- Background Task {task_id} Started ---")
    print(f"Topic: {topic}, Limit: {paper_limit}")
    task_results[task_id] = {"status": "running", "report_path": None, "error_message": None}

    inputs = {"topic": topic, "paper_limit": paper_limit}
    final_state = None
    error_message = None

    try:
        # Using invoke here for simplicity in background task
        final_state = langgraph_app.invoke(inputs)

        if final_state:
            report_path = final_state.get('report_path')
            error_state = final_state.get('error')
            if report_path and os.path.exists(report_path):
                 task_results[task_id] = {"status": "completed", "report_path": report_path, "error_message": error_state}
                 print(f"--- Background Task {task_id} Completed ---")
                 print(f"Report generated: {report_path}")
            else:
                 error_message = error_state or "Workflow finished but report path missing or invalid."
                 task_results[task_id] = {"status": "error", "report_path": None, "error_message": error_message}
                 print(f"--- Background Task {task_id} Error ---")
                 print(error_message)
        else:
             error_message = "Workflow invocation returned None."
             task_results[task_id] = {"status": "error", "report_path": None, "error_message": error_message}
             print(f"--- Background Task {task_id} Error ---")
             print(error_message)

    except Exception as e:
        error_message = f"Critical error during workflow execution: {type(e).__name__} - {e}"
        task_results[task_id] = {"status": "error", "report_path": None, "error_message": error_message}
        print(f"\n--- Background Task {task_id} CRITICAL ERROR ---")
        print(error_message)
        print("---------------------------------")


# --- API Endpoint to Start Research ---
@app.post("/start-research/", status_code=202) # 202 Accepted for background tasks
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """
    Accepts a research topic and starts the generation workflow in the background.
    Returns a task ID to check status later.
    """
    if not langgraph_app:
         raise HTTPException(status_code=500, detail="LangGraph application not loaded. Check server logs.")

    task_id = str(uuid.uuid4())
    print(f"Received request for topic: '{request.topic}'. Assigning Task ID: {task_id}")

    # Add the workflow execution to background tasks
    background_tasks.add_task(run_research_workflow, task_id, request.topic, request.paper_limit)

    return {"message": "Research workflow started.", "task_id": task_id}

# --- API Endpoint to Check Status and Get Report ---
@app.get("/results/{task_id}")
async def get_results(task_id: str):
    """
    Checks the status of a task. If completed, returns the report file.
    If running, returns status. If error, returns error details.
    """
    result = task_results.get(task_id)

    if not result:
        raise HTTPException(status_code=404, detail="Task ID not found.")

    if result["status"] == "completed":
        report_path = result.get("report_path")
        if report_path and os.path.exists(report_path):
            print(f"Serving report for Task ID: {task_id} from {report_path}")
            # Extract filename for download
            filename = os.path.basename(report_path)
            return FileResponse(path=report_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=filename)
        else:
             result["status"] = "error" # Update status
             result["error_message"] = "Task marked completed but report file is missing or invalid."
             print(f"Error for Task ID {task_id}: {result['error_message']}")
             raise HTTPException(status_code=500, detail=result["error_message"])

    elif result["status"] == "running":
        return {"status": "running", "message": "Research workflow is still in progress."}

    elif result["status"] == "error":
         error_msg = result.get("error_message", "An unknown error occurred during the workflow.")
         print(f"Reporting error for Task ID {task_id}: {error_msg}")
         # Return error as JSON instead of raising HTTPException for clarity
         return JSONResponse(status_code=500, content={"status": "error", "message": error_msg})

    else:
         raise HTTPException(status_code=500, detail="Unknown task status.")

# --- Serve the Frontend ---
@app.get("/")
async def read_index():
    # Ensure index.html exists in the same folder
    if os.path.exists('index.html'):
        return FileResponse('index.html')
    return {"message": "index.html not found. API is running."}