import os
import shutil
from fastapi import UploadFile, HTTPException
from configs.app_config import AppConfig
from typing import List, Dict

conf = AppConfig()

UPLOAD_DIR = conf.UPLOAD_FOLDER
ALLOWED_EXT = {".pdf"}
os.makedirs(UPLOAD_DIR, exist_ok=True)


class FileService:
    async def save(self, file: UploadFile) -> dict:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXT:
            raise HTTPException(status_code=400, detail="Định dạng file không được phép")

        file_path = os.path.join(UPLOAD_DIR, str(file.filename))
        # Lưu file vào folder
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": file.size,
            "location": str(file_path)
        }

    def get_path(self, filename: str) -> str:
        path = os.path.join(UPLOAD_DIR, os.path.basename(filename))
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Không tìm thấy file")
        return path

    async def get_all(self) -> List[Dict[str, str]]:
        """
        return list of file name
        """
        files = os.listdir(UPLOAD_DIR)
        return [{"file": f, "path": os.path.join(UPLOAD_DIR, f)} for f in files]

    def delete_file(self, file_name: str) -> Dict[str, str]:
        if not file_name.endswith(".pdf"):
            file_name += ".pdf"
        files = os.listdir(UPLOAD_DIR)
        if file_name not in files:
            raise HTTPException(status_code=400, detail="File not found")
        abs_path = os.path.join(UPLOAD_DIR, file_name)
        try:
            os.remove(abs_path)
            return {"message": "succeed"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)


