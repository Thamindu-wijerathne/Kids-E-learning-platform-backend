import io
from fastapi import APIRouter, File, UploadFile
from app.services.speech_regocnition import SpeechRecognitionService

router = APIRouter()


@router.post("/speech-recognize-test")
async def speech_recognize(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    
    m4a_bytes = SpeechRecognitionService.convert_webm_to_wav(audio_bytes)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("m4a bytes length: ", len(m4a_bytes))
    m4a_stream = io.BytesIO(m4a_bytes)
    
    print("file : ", file)
    segments  = SpeechRecognitionService().transcribe(m4a_stream)
    print("result : ", segments)
    return {"text": "segments"}