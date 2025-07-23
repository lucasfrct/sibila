# flake8: noqa: E501

from datetime import datetime
from src.modules.response.response import Response


async def health():
    return Response.success(200, f"OK {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}").result()
