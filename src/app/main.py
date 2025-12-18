from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.api.v1 import articles, auth, categories


def create_app() -> FastAPI:
    app = FastAPI(
        title="Marketplace Blog API",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # /api/v1/...
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(categories.router, prefix="/api/v1")
    app.include_router(articles.router, prefix="/api/v1")

    return app


app = create_app()
