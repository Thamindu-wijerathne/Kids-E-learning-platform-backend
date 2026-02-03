import easyocr
from fastapi import APIRouter, File, UploadFile
from app.services.ocr_service import OCRService

router = APIRouter()

@router.post("/handwriting-ocr")
async def handwriting_ocr(file: UploadFile = File(...)):
    reader = OCRService().get_reader()
    result = reader.readtext(file.file.read())
    # Convert numpy types to Python native types
    python_result = []
    for box, text, conf in result:
        python_box = [[int(coord) for coord in point] for point in box]  # ints
        python_conf = float(conf)
        python_result.append([python_box, text, python_conf])
        
    print("python_result : ", python_result)
    return {"text": python_result}