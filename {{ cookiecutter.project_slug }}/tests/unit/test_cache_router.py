{% if cookiecutter.include_redis == "y" and cookiecutter.include_example == "y" -%}
import pytest
from unittest.mock import AsyncMock, patch

from app.utils.cache import CacheManager


def test_get_cache_success(client):
    """Test getting a value from cache."""
    with patch.object(CacheManager, "get", new=AsyncMock(return_value="test_value")):
        response = client.get("/cache/get/test_key")
        assert response.status_code == 200
        assert response.json() == {"key": "test_key", "value": "test_value"}


def test_get_cache_not_found(client):
    """Test getting a non-existent key from cache."""
    with patch.object(CacheManager, "get", new=AsyncMock(return_value=None)):
        response = client.get("/cache/get/test_key")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


def test_set_cache_success(client):
    """Test setting a value in cache."""
    with patch.object(CacheManager, "set", new=AsyncMock(return_value=True)):
        response = client.post("/cache/set/test_key?value=test_value")
        assert response.status_code == 200
        data = response.json()
        assert data["key"] == "test_key"
        assert data["status"] == "cached"


def test_set_cache_with_ttl(client):
    """Test setting a value in cache with TTL."""
    with patch.object(CacheManager, "set", new=AsyncMock(return_value=True)):
        response = client.post("/cache/set/test_key?value=test_value&ttl=300")
        assert response.status_code == 200
        data = response.json()
        assert data["key"] == "test_key"
        assert data["ttl"] == 300


def test_set_cache_failure(client):
    """Test handling cache set failure."""
    with patch.object(CacheManager, "set", new=AsyncMock(return_value=False)):
        response = client.post("/cache/set/test_key?value=test_value")
        assert response.status_code == 500
        assert "failed" in response.json()["detail"].lower()


def test_delete_cache_success(client):
    """Test deleting a key from cache."""
    with patch.object(CacheManager, "delete", new=AsyncMock(return_value=True)):
        response = client.delete("/cache/delete/test_key")
        assert response.status_code == 200
        data = response.json()
        assert data["key"] == "test_key"
        assert data["status"] == "deleted"


def test_delete_cache_not_found(client):
    """Test deleting a non-existent key."""
    with patch.object(CacheManager, "delete", new=AsyncMock(return_value=False)):
        response = client.delete("/cache/delete/test_key")
        assert response.status_code == 404


def test_check_cache_exists(client):
    """Test checking if a key exists in cache."""
    with patch.object(CacheManager, "exists", new=AsyncMock(return_value=True)):
        response = client.get("/cache/exists/test_key")
        assert response.status_code == 200
        data = response.json()
        assert data["key"] == "test_key"
        assert data["exists"] is True


def test_check_cache_not_exists(client):
    """Test checking if a non-existent key exists."""
    with patch.object(CacheManager, "exists", new=AsyncMock(return_value=False)):
        response = client.get("/cache/exists/test_key")
        assert response.status_code == 200
        data = response.json()
        assert data["key"] == "test_key"
        assert data["exists"] is False


def test_clear_cache_pattern(client):
    """Test clearing cache keys by pattern."""
    with patch.object(CacheManager, "delete_pattern", new=AsyncMock(return_value=5)):
        response = client.delete("/cache/clear/test:*")
        assert response.status_code == 200
        data = response.json()
        assert data["pattern"] == "test:*"
        assert data["deleted_count"] == 5
{%- endif %}
