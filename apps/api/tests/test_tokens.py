"""
Token type separation and reset-link logging. These tests need no database.
"""

from __future__ import annotations

import uuid

import pytest
from fastapi import HTTPException

from app.core.config import settings
from app.core.security import create_access_token, verify_token
from app.models.user import User
from app.services import auth_service
from app.services.auth_service import AuthService


def _user() -> User:
    return User(id=uuid.uuid4(), email="tokens@jobsense.dev", full_name="Token User")


def test_access_token_is_accepted():
    user = _user()
    token = create_access_token({"sub": str(user.id), "email": user.email})

    assert verify_token(token).user_id == user.id


def test_refresh_token_is_not_accepted_as_access_token():
    refresh_token = AuthService(None)._create_refresh_token(_user())  # type: ignore[arg-type]

    with pytest.raises(HTTPException) as error:
        verify_token(refresh_token)

    assert error.value.status_code == 401


@pytest.mark.parametrize(("environment", "logged"), [("development", True), ("production", False)])
async def test_reset_link_is_only_logged_in_development(
    monkeypatch: pytest.MonkeyPatch, environment: str, logged: bool
):
    user = _user()

    class _Result:
        def scalar_one_or_none(self) -> User:
            return user

    class _Session:
        async def execute(self, _statement) -> _Result:
            return _Result()

    events: list[dict] = []
    monkeypatch.setattr(settings, "ENVIRONMENT", environment)
    monkeypatch.setattr(
        auth_service.logger, "info", lambda _event, **details: events.append(details)
    )

    await AuthService(_Session()).initiate_password_reset(user.email)  # type: ignore[arg-type]

    assert ("reset_url" in events[0]) is logged
