from src.modules.response.response import Response


def health():
    return Response.success(200, "OK").result()
