import easyocr

class OCRService:
    _reader = None  # class-level (shared)

    @classmethod
    def get_reader(cls):
        if cls._reader is None:
            cls._reader = easyocr.Reader(['en'])
        return cls._reader