from fastapi import FastAPI

from app.api.routes.travel_routes import (
    router as travel_router
)


app = FastAPI(

    title="Enterprise AI Travel Planner",

    version="1.0.0"
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