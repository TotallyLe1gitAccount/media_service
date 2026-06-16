from fastapi import UploadFile

def save_file(file: UploadFile, path: str):
    with open(path, "wb") as buffer:
        while chunk := file.file.read(1024 * 1024):
            buffer.write(chunk)