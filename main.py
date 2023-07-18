#!/usr/bin/env python3


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware

from authlib.integrations.starlette_client import OAuth, OAuthError

import uvicorn

from src import router

app = FastAPI()
app.include_router(router.auth)
app.include_router(router.langchain)


origins = [
    "http://localhost:3000",
    "http://app.esgpilot.org:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key="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",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
