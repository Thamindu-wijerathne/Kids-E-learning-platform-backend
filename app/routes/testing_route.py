import easyocr
from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file.file.read())
    # Convert numpy types to Python native types
    python_result = []
    for box, text, conf in result:
        python_box = [[int(coord) for coord in point] for point in box]  # ints
        python_conf = float(conf)
        python_result.append([python_box, text, python_conf])
        
    return {"text": python_result}