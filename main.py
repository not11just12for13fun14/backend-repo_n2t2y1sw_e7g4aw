import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Candle, Inquiry, Subscriber

app = FastAPI(title="Candle Boutique API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Candle Boutique API running"}


@app.get("/api/candles", response_model=List[Candle])
def list_candles(limit: Optional[int] = 50):
    try:
        docs = get_documents("candle", {}, limit)
        # Convert ObjectId and timestamps to plain types
        cleaned = []
        for d in docs:
            d.pop("_id", None)
            if "created_at" in d:
                d["created_at"] = str(d["created_at"])  # not in model, so safe to ignore
            if "updated_at" in d:
                d["updated_at"] = str(d["updated_at"])  # not in model, so safe to ignore
            cleaned.append(d)
        return cleaned
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/inquiries")
def create_inquiry(inquiry: Inquiry):
    try:
        _id = create_document("inquiry", inquiry)
        return {"status": "ok", "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/subscribe")
def subscribe(sub: Subscriber):
    try:
        _id = create_document("subscriber", sub)
        return {"status": "ok", "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
