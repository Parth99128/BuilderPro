"""Run the BuildPro backend server."""
import uvicorn
import os

if __name__ == "__main__":
    # Use PORT from environment (Railway/Render) or default to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
    )
