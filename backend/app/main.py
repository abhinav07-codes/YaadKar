"""FastAPI application entrypoint for YaadKar."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.summary import router as summary_router

app = FastAPI(title="YaadKar", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_origin_regex=r"chrome-extension://.*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summary_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
