from fastapi import UploadFile

async def save_file(file: UploadFile, path: str):
    with open(path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            buffer.write(chunk)