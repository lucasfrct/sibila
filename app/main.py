from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.modules.auth.controller import router as auth_router
from app.modules.users.controller import router as users_router

API_TITLE = "Sibila API"
HEALTH_ROUTE = "/health"
HEALTH_STATUS_OK = "ok"


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


def create_app() -> FastAPI:
    application = FastAPI(title=API_TITLE)
    application.include_router(auth_router)
    application.include_router(users_router)

    @application.get(HEALTH_ROUTE)
    async def health() -> dict[str, str]:
        return {"status": HEALTH_STATUS_OK}

    application.add_exception_handler(ValueError, value_error_handler)
    return application
