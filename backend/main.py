from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_feed import router as feed_router

app = FastAPI(
    title="GeoPulse AI API",
    description="News-to-market-impact prediction API",
    version="1.0.0",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(feed_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
