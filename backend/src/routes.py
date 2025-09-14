from fastapi import APIRouter

from .support.controllers import category_controller, support_controller, questions_controller


def get_apps_router():
    router = APIRouter()
    router.include_router(category_controller.router)
    router.include_router(questions_controller.router)
    router.include_router(support_controller.router)
    return router
