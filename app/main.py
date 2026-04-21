from fastapi import FastAPI

app = FastAPI(title="Todo API")


@app.get("/health", tags=["monitoring"])
async def health_check():
    return {"status": "healthy"}
