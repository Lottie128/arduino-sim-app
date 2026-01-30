from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# Import routers
from api import boards, upload, compile, libraries, projects, ports
from websocket import simulation, serial_monitor

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Arduino Simulation Platform starting...")
    # Initialize database, check Arduino CLI, etc.
    yield
    # Shutdown
    print("👋 Shutting down...")

app = FastAPI(
    title="Arduino Simulation Platform API",
    description="Backend API for Arduino & ESP32 circuit simulation and programming",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(boards.router, prefix="/api/boards", tags=["boards"])
app.include_router(ports.router, prefix="/api/ports", tags=["ports"])
app.include_router(compile.router, prefix="/api/compile", tags=["compile"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(libraries.router, prefix="/api/libraries", tags=["libraries"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])

# WebSocket endpoints
@app.websocket("/ws/simulation")
async def websocket_simulation(websocket: WebSocket):
    await simulation.handle_simulation(websocket)

@app.websocket("/ws/serial")
async def websocket_serial(websocket: WebSocket):
    await serial_monitor.handle_serial(websocket)

@app.get("/")
async def root():
    return {
        "message": "Arduino Simulation Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "arduino-sim-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
