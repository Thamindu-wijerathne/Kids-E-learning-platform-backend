import easyocr

class OCRService:
    def __init__(self):
        self.reader = None
    def get_reader(self):
        if self.reader is None:
            self.reader = easyocr.Reader(['en'])
        return self.reader