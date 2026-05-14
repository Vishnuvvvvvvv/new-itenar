from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.api.routes.travel_routes import (
    router as travel_router
)

from app.api.routes.frontend_routes import (
    router as frontend_router
)
from app.api.routes.auth_routes import (
    router as auth_router
)
from app.api.routes.booking_routes import (
    router as booking_router
)

app = FastAPI(

    title="Enterprise AI Travel Planner",

    version="1.0.0"
)

# =========================
# CORS
# =========================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)



@app.get("/")
def home():

    return {
        "message": "Enterprise AI Travel Planner Running"
    }


app.include_router(

    travel_router,

    prefix="/api"
)

app.include_router(

    frontend_router
)

app.include_router(

    auth_router
)

app.include_router(

    booking_router
)
