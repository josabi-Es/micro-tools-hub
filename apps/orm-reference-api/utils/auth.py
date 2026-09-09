import os

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)):
    """Reject the request unless it carries the key set in the .env file."""
    # read on each request so it does not depend on when the .env was loaded
    expected = os.getenv("API_KEY")

    # a missing key closes the API instead of opening it
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The server has no API_KEY set. Add it to the .env file and restart.",
        )
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No X-API-Key header was sent. In Swagger, use the Authorize button first.",
        )
    if api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The X-API-Key header does not match the key in the .env file.",
        )
