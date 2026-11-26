"""
Apify record normalization. These tests need no database.
"""

from __future__ import annotations

import pytest

from app.integrations.apify.normalizer import normalize_apify_job

RECORD = {"title": "Engineer", "company": "Acme", "id": "1"}


@pytest.mark.parametrize("url", ["https://example.test/job", "http://example.test/job"])
def test_web_apply_url_is_kept(url: str):
    assert normalize_apify_job({**RECORD, "url": url}, source_id="s")["apply_url"] == url


@pytest.mark.parametrize("url", ["javascript:alert(1)", " JavaScript:alert(1)", "data:text/html,x"])
def test_script_apply_url_is_dropped(url: str):
    assert normalize_apify_job({**RECORD, "url": url}, source_id="s")["apply_url"] is None
