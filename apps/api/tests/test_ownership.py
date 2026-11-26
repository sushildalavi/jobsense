"""
A user must not read or act on another user's resumes and applications.
"""

from __future__ import annotations

import uuid
from contextlib import asynccontextmanager

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.resume import MasterResume, ResumeVersion
from app.models.user import User
from app.tasks.ai_tasks import _tailor_resume_async, tailor_resume

pytestmark = pytest.mark.asyncio


@pytest.fixture
def queued_tasks(monkeypatch: pytest.MonkeyPatch) -> list[tuple]:
    """Capture tailoring dispatches instead of sending them to a broker."""
    calls: list[tuple] = []
    monkeypatch.setattr(tailor_resume, "delay", lambda *args: calls.append(args))
    return calls


@pytest.fixture
async def other_users_resume(async_session: AsyncSession) -> dict:
    owner = User(
        email="other@jobsense.dev",
        hashed_password=get_password_hash("OtherPass123"),
        full_name="Other User",
    )
    async_session.add(owner)
    await async_session.flush()
    master = MasterResume(user_id=owner.id, name="Private", raw_text="private text")
    async_session.add(master)
    await async_session.flush()
    version = ResumeVersion(
        user_id=owner.id,
        master_resume_id=master.id,
        name="Private version",
        tailored_content="private tailored text",
    )
    async_session.add(version)
    await async_session.commit()
    return {"master_id": str(master.id), "version_id": str(version.id)}


async def _own_application(client: AsyncClient, headers: dict, job_id: str) -> str:
    response = await client.post("/api/v1/applications", json={"job_id": job_id}, headers=headers)
    assert response.status_code == 201, response.text
    return response.json()["id"]


async def test_cannot_tailor_with_another_users_resume(
    client: AsyncClient,
    auth_headers: dict,
    test_job: dict,
    other_users_resume: dict,
    queued_tasks: list,
):
    app_id = await _own_application(client, auth_headers, test_job["id"])

    response = await client.post(
        f"/api/v1/applications/{app_id}/tailor-resume",
        json={"resume_id": other_users_resume["master_id"], "job_id": test_job["id"]},
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert queued_tasks == []


async def test_cannot_tailor_an_unknown_application(
    client: AsyncClient,
    auth_headers: dict,
    test_job: dict,
    other_users_resume: dict,
    queued_tasks: list,
):
    response = await client.post(
        f"/api/v1/applications/{uuid.uuid4()}/tailor-resume",
        json={"resume_id": other_users_resume["master_id"], "job_id": test_job["id"]},
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert queued_tasks == []


async def test_cannot_attach_another_users_resume_version(
    client: AsyncClient,
    auth_headers: dict,
    test_job: dict,
    other_users_resume: dict,
):
    app_id = await _own_application(client, auth_headers, test_job["id"])

    update = await client.patch(
        f"/api/v1/applications/{app_id}",
        json={"resume_version_id": other_users_resume["version_id"]},
        headers=auth_headers,
    )
    read = await client.get(f"/api/v1/applications/{app_id}/resume", headers=auth_headers)

    assert update.status_code == 404
    assert read.status_code == 404


async def test_worker_skips_records_owned_by_different_users(
    client: AsyncClient,
    auth_headers: dict,
    test_job: dict,
    other_users_resume: dict,
    async_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
):
    app_id = await _own_application(client, auth_headers, test_job["id"])

    @asynccontextmanager
    async def session_factory():
        yield async_session

    monkeypatch.setattr("app.core.database.AsyncSessionLocal", session_factory)

    result = await _tailor_resume_async(app_id, other_users_resume["master_id"])

    assert result == {"skipped": True, "reason": "resume not found"}
