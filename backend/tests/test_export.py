"""Тесты для экспорта переписок."""

import uuid
from datetime import UTC, datetime

import pytest


class TestExportSchemas:
    """Тесты схем экспорта."""

    def test_export_format_enum(self):
        """ExportFormat enum."""
        from src.schemas.export import ExportFormat

        assert ExportFormat.JSON.value == "json"
        assert ExportFormat.HTML.value == "html"
        assert ExportFormat.TXT.value == "txt"

    def test_export_status_enum(self):
        """ExportStatus enum."""
        from src.schemas.export import ExportStatus

        assert ExportStatus.PENDING.value == "pending"
        assert ExportStatus.PROCESSING.value == "processing"
        assert ExportStatus.COMPLETED.value == "completed"
        assert ExportStatus.FAILED.value == "failed"

    def test_export_chat_request(self):
        """ExportChatRequest валидация."""
        from src.schemas.export import ExportChatRequest, ExportFormat

        chat_id = uuid.uuid4()
        data = ExportChatRequest(
            chat_id=chat_id,
            format=ExportFormat.JSON,
            include_media=True,
        )
        assert data.chat_id == chat_id
        assert data.format == ExportFormat.JSON
        assert data.include_media is True

    def test_export_chat_request_defaults(self):
        """ExportChatRequest с дефолтными значениями."""
        from src.schemas.export import ExportChatRequest, ExportFormat

        data = ExportChatRequest(chat_id=uuid.uuid4())
        assert data.format == ExportFormat.JSON
        assert data.include_media is True
        assert data.start_date is None
        assert data.end_date is None

    def test_export_chat_request_with_dates(self):
        """ExportChatRequest с датами."""
        from src.schemas.export import ExportChatRequest

        now = datetime.now(UTC)
        data = ExportChatRequest(
            chat_id=uuid.uuid4(),
            start_date=now,
            end_date=now,
        )
        assert data.start_date == now
        assert data.end_date == now

    def test_export_job_response(self):
        """ExportJobResponse валидация."""
        from src.schemas.export import ExportFormat, ExportJobResponse, ExportStatus

        now = datetime.now(UTC)
        data = ExportJobResponse(
            id=uuid.uuid4(),
            chat_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            format=ExportFormat.HTML,
            status=ExportStatus.COMPLETED,
            include_media=False,
            file_url="/exports/chat.html",
            file_size=1024,
            message_count=50,
            error_message=None,
            created_at=now,
            completed_at=now,
        )
        assert data.format == ExportFormat.HTML
        assert data.status == ExportStatus.COMPLETED
        assert data.file_size == 1024

    def test_export_list_response(self):
        """ExportListResponse валидация."""
        from src.schemas.export import ExportListResponse

        data = ExportListResponse(exports=[], total=0)
        assert data.exports == []
        assert data.total == 0

    def test_export_progress_response(self):
        """ExportProgressResponse валидация."""
        from src.schemas.export import ExportProgressResponse, ExportStatus

        data = ExportProgressResponse(
            job_id=uuid.uuid4(),
            status=ExportStatus.PROCESSING,
            progress=50,
            message_count=100,
            current_message=50,
        )
        assert data.progress == 50
        assert data.status == ExportStatus.PROCESSING

    def test_exported_message(self):
        """ExportedMessage валидация."""
        from src.schemas.export import ExportedMessage

        now = datetime.now(UTC)
        data = ExportedMessage(
            id=uuid.uuid4(),
            sender_id=uuid.uuid4(),
            sender_name="Иван",
            content="Привет!",
            message_type="text",
            created_at=now,
            edited_at=None,
            attachments=None,
            reactions=None,
        )
        assert data.sender_name == "Иван"
        assert data.content == "Привет!"

    def test_exported_chat(self):
        """ExportedChat валидация."""
        from src.schemas.export import ExportedChat

        now = datetime.now(UTC)
        data = ExportedChat(
            id=uuid.uuid4(),
            name="Рабочий чат",
            chat_type="group",
            created_at=now,
            exported_at=now,
            message_count=100,
            participants=[],
            messages=[],
        )
        assert data.name == "Рабочий чат"
        assert data.message_count == 100
