from fastapi import APIRouter,UploadFile,File

from src.api.v1.ModelAnalysis.schema.model_analyze import PromptModel
from src.api.v1.ModelAnalysis.service.model_analyze import bad_word_prediction, speech_to_text_bad_word_detection

router = APIRouter()

@router.post("/analyze")
def prompt_analysis(req:PromptModel):
    return bad_word_prediction(req.text)

@router.post("/analyze-speech")
async def speech_to_text_prompt_analysis(file: UploadFile = File(...)):
    return await speech_to_text_bad_word_detection(file)