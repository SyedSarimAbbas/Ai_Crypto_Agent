from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent.crypto_agent import crypto_agent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Crypto Knowledge Agent API",
    description="Backend API for crypto information queries",
    version="1.0.0"
)

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import StreamingResponse
import json

# Request model
class ChatRequest(BaseModel):
    message: str

# API Routes
@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Process crypto queries and return a streaming agent response
    """
    try:
        logger.info(f"Received query: {request.message}")
        
        # Call the crypto agent (returns a generator or a string)
        agent_output = crypto_agent(request.message)
        
        def event_generator():
            try:
                if isinstance(agent_output, str):
                    logger.info(f"Direct string response: {agent_output[:50]}...")
                    yield agent_output
                else:
                    logger.info("Starting stream generation...")
                    for chunk in agent_output:
                        # chunk is typically a BaseMessageChunk
                        content = ""
                        if hasattr(chunk, 'content'):
                            content = chunk.content
                        else:
                            content = str(chunk)
                            
                        if content:
                            yield content
                    logger.info("Stream generation complete.")
            except Exception as e:
                logger.error(f"Error in stream generator: {str(e)}")
                yield f"\n[System Error: {str(e)}]"

        return StreamingResponse(event_generator(), media_type="text/plain")

    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing your request: {str(e)}"
        )


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Check if the API is running"""
    return {"status": "healthy", "message": "Crypto Agent API is running"}

# Serve frontend
@app.get("/")
async def serve_frontend():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    print("Starting Crypto Agent API Server...")
    print("Frontend: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
