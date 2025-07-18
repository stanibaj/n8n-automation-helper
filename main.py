from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from routers import whois_router

app = FastAPI(
    title="Network Tools API",
    description="A modular API for network-related tools like WHOIS and DNS lookup",
    version="1.0.0"
)

# Include routers
app.include_router(whois_router.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Network Tools API", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)
