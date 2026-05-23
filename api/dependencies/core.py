from fastapi import Header, HTTPException
from typing import Optional

async def get_token_header(x_token: Optional[str] = Header(None)):
    """
    Mock dependency for API token validation.
    """
    if x_token and x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
