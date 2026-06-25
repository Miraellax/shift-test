import uvicorn
from fastapi import FastAPI

from .modules.auth.router import router as router_auth
from .modules.rooms.router import router as router_room
from .modules.users.router import router as router_user
from .modules.reservations.router import router as router_reservation
from .modules.slots.router import router as router_slot

def create_app() -> FastAPI:
    _app = FastAPI()

    _app.include_router(router_auth)
    _app.include_router(router_room)
    _app.include_router(router_user)
    _app.include_router(router_reservation)
    _app.include_router(router_slot)

    return _app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
