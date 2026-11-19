"""Auth config. Signup and login are specified and not mounted."""

from fastapi import APIRouter

from Repositories.Auth.controllers import auth_controller

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/config", summary="Whether public signup is open. It is closed.")
async def show_auth_config() -> dict:
    return await auth_controller.show_config()
