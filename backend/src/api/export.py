"""API эндпоинты для экспорта переписок."""

import json
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.chat import Chat, ChatMember, Message
from src.models.user import User
from src.schemas.export import (
    ExportChatRequest,
    ExportFormat,
    ExportJobResponse,
    ExportListResponse,
    ExportProgressResponse,
    ExportStatus,
    ExportedChat,
    ExportedMessage,
)

router = APIRouter(prefix="/export", tags=["export"])

EXPORT_JOBS: dict[str, dict] = {}


async def check_chat_access(
    db: AsyncSession, user_id: uuid.UUID, chat_id: uuid.UUID
) -> Chat:
    """Проверяет доступ пользователя к чату."""
    chat = await db.get(Chat, chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Чат не найден", "code": "chat_not_found"},
        )

    member_result = await db.execute(
        select(ChatMember)
        .where(ChatMember.chat_id == chat_id)
        .where(ChatMember.user_id == user_id)
    )
    if not member_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет доступа к чату", "code": "no_access"},
        )

    return chat


@router.post("/chat", response_model=ExportJobResponse, status_code=status.HTTP_202_ACCEPTED)
async def start_export(
    request: ExportChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ExportJobResponse:
    """Начать экспорт чата."""
    await check_chat_access(db, current_user.id, request.chat_id)

    job_id = uuid.uuid4()
    now = datetime.now(UTC)

    job = {
        "id": job_id,
        "chat_id": request.chat_id,
        "user_id": current_user.id,
        "format": request.format,
        "status": ExportStatus.PENDING,
        "include_media": request.include_media,
        "file_url": None,
        "file_size": None,
        "message_count": None,
        "error_message": None,
        "created_at": now,
        "completed_at": None,
    }
    EXPORT_JOBS[str(job_id)] = job

    return ExportJobResponse(**job)


@router.get("/jobs", response_model=ExportListResponse)
async def list_exports(
    current_user: User = Depends(get_current_user),
) -> ExportListResponse:
    """Получить список экспортов пользователя."""
    user_jobs = [
        ExportJobResponse(**job)
        for job in EXPORT_JOBS.values()
        if job["user_id"] == current_user.id
    ]
    return ExportListResponse(exports=user_jobs, total=len(user_jobs))


@router.get("/jobs/{job_id}", response_model=ExportJobResponse)
async def get_export_status(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> ExportJobResponse:
    """Получить статус экспорта."""
    job = EXPORT_JOBS.get(str(job_id))
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Экспорт не найден", "code": "export_not_found"},
        )

    if job["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет доступа к экспорту", "code": "no_access"},
        )

    return ExportJobResponse(**job)


@router.get("/jobs/{job_id}/progress", response_model=ExportProgressResponse)
async def get_export_progress(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> ExportProgressResponse:
    """Получить прогресс экспорта."""
    job = EXPORT_JOBS.get(str(job_id))
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Экспорт не найден", "code": "export_not_found"},
        )

    if job["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет доступа к экспорту", "code": "no_access"},
        )

    progress = 100 if job["status"] == ExportStatus.COMPLETED else 50

    return ExportProgressResponse(
        job_id=job_id,
        status=job["status"],
        progress=progress,
        message_count=job.get("message_count"),
        current_message=None,
    )


@router.get("/jobs/{job_id}/download")
async def download_export(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """Скачать экспортированный чат."""
    job = EXPORT_JOBS.get(str(job_id))
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Экспорт не найден", "code": "export_not_found"},
        )

    if job["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет доступа к экспорту", "code": "no_access"},
        )

    chat = await db.get(Chat, job["chat_id"])
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Чат не найден", "code": "chat_not_found"},
        )

    messages_result = await db.execute(
        select(Message)
        .where(Message.chat_id == job["chat_id"])
        .order_by(Message.created_at.asc())
        .limit(1000)
    )
    messages = messages_result.scalars().all()

    exported_messages = [
        {
            "id": str(m.id),
            "sender_id": str(m.sender_id),
            "content": m.content,
            "message_type": m.message_type,
            "created_at": m.created_at.isoformat(),
        }
        for m in messages
    ]

    export_data = {
        "chat_id": str(job["chat_id"]),
        "chat_name": chat.name or "Чат",
        "exported_at": datetime.now(UTC).isoformat(),
        "message_count": len(exported_messages),
        "messages": exported_messages,
    }

    job["status"] = ExportStatus.COMPLETED
    job["completed_at"] = datetime.now(UTC)
    job["message_count"] = len(exported_messages)

    if job["format"] == ExportFormat.JSON:
        content = json.dumps(export_data, ensure_ascii=False, indent=2)
        media_type = "application/json"
        filename = f"chat_export_{job['chat_id']}.json"
    elif job["format"] == ExportFormat.TXT:
        lines = [f"Экспорт чата: {export_data['chat_name']}", f"Дата: {export_data['exported_at']}", ""]
        for msg in exported_messages:
            lines.append(f"[{msg['created_at']}] {msg['content']}")
        content = "\n".join(lines)
        media_type = "text/plain; charset=utf-8"
        filename = f"chat_export_{job['chat_id']}.txt"
    else:
        lines = [
            "<!DOCTYPE html>",
            "<html><head><meta charset='utf-8'><title>Экспорт чата</title></head>",
            "<body><h1>Экспорт чата</h1>",
        ]
        for msg in exported_messages:
            lines.append(f"<p><small>{msg['created_at']}</small><br>{msg['content']}</p>")
        lines.append("</body></html>")
        content = "\n".join(lines)
        media_type = "text/html; charset=utf-8"
        filename = f"chat_export_{job['chat_id']}.html"

    async def generate():
        yield content.encode("utf-8")

    return StreamingResponse(
        generate(),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_export(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> None:
    """Удалить экспорт."""
    job = EXPORT_JOBS.get(str(job_id))
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Экспорт не найден", "code": "export_not_found"},
        )

    if job["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет доступа к экспорту", "code": "no_access"},
        )

    del EXPORT_JOBS[str(job_id)]
