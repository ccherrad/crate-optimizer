from fastapi import FastAPI

from api import router as api_router

app = FastAPI(
    title="crate optimizer",
)

app.include_router(api_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
