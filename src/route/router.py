from fastapi import APIRouter,Depends
from src.api.v1.ModelAnalysis.views import model_analyze

router = APIRouter(prefix="/api")

router.include_router(model_analyze.router,tags=["Prompt Analysis"])