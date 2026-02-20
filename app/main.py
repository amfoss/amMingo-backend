from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth

app=FastAPI(title="amMingo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api", tags=["users"])

@app.get('/')
def root():
    return {'amMingo': 'This is amMingo'}