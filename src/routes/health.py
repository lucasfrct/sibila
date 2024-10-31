from src.modules.response.response import Response


async def health():
    return Response.success(200, "OK").result()
