from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.route.router import router

app = FastAPI(debug=True)

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=("DELETE", "GET", "PATCH", "POST", "PUT"),
                   allow_headers=["*"])

app.include_router(router)