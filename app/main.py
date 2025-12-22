import os
import time
from fastapi import FastAPI, Depends, HTTPException, Security, Response
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import PlainTextResponse
from duckduckgo_search import DDGS
from google import genai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Appscrip Trade Intel - Free Tier")

# Security
API_KEY_NAME = "X-API-KEY"
SECRET_KEY = "appscrip_assignment_secret"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(header_value: str = Security(api_key_header)):
    if header_value != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key.")
    return header_value

@app.get("/analyze/{sector}", response_class=PlainTextResponse)
async def analyze_sector(
    sector: str, 
    model: str = "gemini-2.5-flash-lite", 
    api_key: str = Depends(verify_api_key)
):
    news = ""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(f"Indian {sector} market trends 2025", max_results=3))
            news = "\n".join([r['body'] for r in results])
    except:
        news = "General 2025 market context."

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    # FREE TIER FALLBACK (Latest December 2025 strings)
    for m in [model, "gemini-2.5-flash-lite", "gemini-2.0-flash"]:
        try:
            response = client.models.generate_content(
                model=m,
                contents=f"Generate a professional trade report for {sector} in India. Context: {news}"
            )
            return Response(content=response.text, media_type="text/plain")
        except Exception as e:
            err_str = str(e)
            if "429" in err_str:
                # Explicitly signal rate limit to the frontend
                raise HTTPException(status_code=429, detail="RATE_LIMIT_HIT")
            if "404" in err_str:
                continue
            raise HTTPException(status_code=500, detail=err_str)

    raise HTTPException(status_code=500, detail="No models accessible.")

@app.get("/health")
async def health(): return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)