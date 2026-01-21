"""API эндпоинты для медиафайлов."""

import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.media import MediaFile
from src.models.user import User
from src.schemas.media import MediaFileResponse, UploadResponse
from src.services.media import (
    generate_storage_path,
    get_file_url,
    get_media_type,
    guess_mime_type,
    is_allowed_file,
    validate_file_size,
)

router = APIRouter(prefix="/media", tags=["media"])


def _build_media_response(media: MediaFile) -> MediaFileResponse:
    """Построить ответ медиафайла."""
    return MediaFileResponse(
        id=media.id,
        media_type=media.media_type,
        filename=media.filename,
        original_filename=media.original_filename,
        mime_type=media.mime_type,
        file_size=media.file_size,
        url=get_file_url(media.storage_path),
        thumbnail_url=get_file_url(media.thumbnail_path) if media.thumbnail_path else None,
        duration_seconds=media.duration_seconds,
        width=media.width,
        height=media.height,
        created_at=media.created_at,
    )


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    is_voice: bool = Form(False),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UploadResponse:
    """Загрузить медиафайл."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Имя файла обязательно", "code": "filename_required"},
        )

    mime_type = file.content_type or guess_mime_type(file.filename)

    if not is_allowed_file(mime_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Тип файла не разрешён", "code": "file_type_not_allowed"},
        )

    media_type = get_media_type(mime_type, is_voice)

    content = await file.read()
    file_size = len(content)

    if not validate_file_size(file_size, media_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Файл слишком большой", "code": "file_too_large"},
        )

    filename, storage_path = generate_storage_path(
        current_user.id, media_type, file.filename
    )

    with open(storage_path, "wb") as f:
        f.write(content)

    media = MediaFile(
        uploader_id=current_user.id,
        media_type=media_type.value,
        filename=filename,
        original_filename=file.filename,
        mime_type=mime_type,
        file_size=file_size,
        storage_path=storage_path,
    )
    db.add(media)
    await db.flush()
    await db.refresh(media)

    return UploadResponse(
        media=_build_media_response(media),
        message="Файл успешно загружен",
    )


@router.get("/{media_id}")
async def get_media_info(
    media_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MediaFileResponse:
    """Получить информацию о медиафайле."""
    media = await db.get(MediaFile, media_id)

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Файл не найден", "code": "file_not_found"},
        )

    return _build_media_response(media)


@router.get("/{media_id}/download")
async def download_media(
    media_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    """Скачать медиафайл."""
    media = await db.get(MediaFile, media_id)

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Файл не найден", "code": "file_not_found"},
        )

    return FileResponse(
        path=media.storage_path,
        filename=media.original_filename,
        media_type=media.mime_type,
    )


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(
    media_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Удалить медиафайл."""
    media = await db.get(MediaFile, media_id)

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Файл не найден", "code": "file_not_found"},
        )

    if media.uploader_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Можно удалять только свои файлы", "code": "not_owner"},
        )

    import os
    if os.path.exists(media.storage_path):
        os.remove(media.storage_path)
    if media.thumbnail_path and os.path.exists(media.thumbnail_path):
        os.remove(media.thumbnail_path)

    await db.delete(media)


@router.get("/user/files")
async def get_user_files(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[MediaFileResponse]:
    """Получить список файлов пользователя."""
    result = await db.execute(
        select(MediaFile)
        .where(MediaFile.uploader_id == current_user.id)
        .order_by(MediaFile.created_at.desc())
        .limit(100)
    )
    files = result.scalars().all()

    return [_build_media_response(media) for media in files]
