from fastapi import Request, HTTPException

VALID_TOKEN = "72b507a14e702a622f69f0154ca1db7888ec2e8f14a34727fe63389e74207a7e"

def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {VALID_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
