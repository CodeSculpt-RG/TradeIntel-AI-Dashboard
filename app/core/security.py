from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from starlette.requests import Request

# This is the EXACT key you must use
API_KEY = "appscrip_assignment_secret"

# name="X-API-KEY" tells FastAPI to look for this specific header name
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def validate_auth(header_val: str = Security(api_key_header)):
    if header_val == API_KEY:
        return header_val
    
    # If the key is missing or wrong, return 403
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, 
        detail="Invalid API Key"
    )