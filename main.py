from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import router as api_router
from config import global_data as gd
from config import cloud_log as LOG

app = FastAPI()


@app.on_event("startup")
def startup():
    gd.get_env_config()
    # setup logging
    LOG.setup_logging(gd.get_config_val("logging"))
    logger.info("Book Cloud Backend Starting...")
    logger.debug(gd.CONFIG)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8080, log_level="info", reload=True)


@app.get("/")
def read_root():
    return {"Navigate to /docs"}

