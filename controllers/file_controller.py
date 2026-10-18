from fastapi import APIRouter, Depends, File, UploadFile
from services.file_serivce import FileService
from common.dependencies import get_file_service

router = APIRouter(
    prefix="/files",
    tags=["File"] # Dùng để hiện trong swagger
)

@router.post("/upload")
async def upload_file(file: UploadFile, service: FileService = Depends(get_file_service)):
    return await service.save(file)

@router.get("/")
async def get_all_files(service: FileService = Depends(get_file_service)):
    return await service.get_all()

@router.delete("/{file_name}")
def delete_file(file_name: str, service: FileService = Depends(get_file_service)):
    return service.delete_file(file_name)