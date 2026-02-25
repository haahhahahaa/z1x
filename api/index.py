import sys
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Add the root directory to the path so we can import from backend
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.index import app

# Serve static files from the frontend build
static_dir = root_dir / "frontend" / "dist"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
else:
    # Fallback route if static files don't exist
    @app.get("/{full_path:path}")
    async def fallback(full_path: str):
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"error": "Frontend not built yet", "status": 404}


