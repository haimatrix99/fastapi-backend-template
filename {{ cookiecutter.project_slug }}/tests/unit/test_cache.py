{% if cookiecutter.include_redis == "y" -%}
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.utils.cache import CacheManager, cache_result, invalidate_cache


@pytest.mark.asyncio
async def test_cache_manager_get_success():
    """Test CacheManager.get returns value when Redis is available."""
    mock_redis = AsyncMock()
    mock_redis.get.return_value = "test_value"
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        result = await CacheManager.get("test_key")
        assert result == "test_value"
        mock_redis.get.assert_called_once_with("test_key")


@pytest.mark.asyncio
async def test_cache_manager_get_no_redis():
    """Test CacheManager.get returns None when Redis is not available."""
    with patch("app.utils.cache.get_redis", return_value=None):
        result = await CacheManager.get("test_key")
        assert result is None


@pytest.mark.asyncio
async def test_cache_manager_get_exception():
    """Test CacheManager.get returns None on exception."""
    mock_redis = AsyncMock()
    mock_redis.get.side_effect = Exception("Redis error")
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        result = await CacheManager.get("test_key")
        assert result is None


@pytest.mark.asyncio
async def test_cache_manager_set_success():
    """Test CacheManager.set stores value successfully."""
    mock_redis = AsyncMock()
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        result = await CacheManager.set("test_key", "test_value")
        assert result is True
        mock_redis.set.assert_called_once_with("test_key", "test_value")


@pytest.mark.asyncio
async def test_cache_manager_set_with_ttl():
    """Test CacheManager.set stores value with TTL."""
    mock_redis = AsyncMock()
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        result = await CacheManager.set("test_key", "test_value", ttl=300)
        assert result is True
        mock_redis.setex.assert_called_once_with("test_key", 300, "test_value")


@pytest.mark.asyncio
async def test_cache_manager_set_no_redis():
    """Test CacheManager.set returns False when Redis is not available."""
    with patch("app.utils.cache.get_redis", return_value=None):
        result = await CacheManager.set("test_key", "test_value")
        assert result is False


@pytest.mark.asyncio
async def test_cache_manager_delete_success():
    """Test CacheManager.delete removes key successfully."""
    mock_redis = AsyncMock()
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        result = await CacheManager.delete("test_key")
        assert result is True
        mock_redis.delete.assert_called_once_with("test_key")


@pytest.mark.asyncio
async def test_cache_manager_delete_pattern():
    """Test CacheManager.delete_pattern removes matching keys."""
    mock_redis = AsyncMock()
    mock_redis.keys.return_value = ["key1", "key2", "key3"]
    mock_redis.delete.return_value = 3
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        result = await CacheManager.delete_pattern("key*")
        assert result == 3
        mock_redis.keys.assert_called_once_with("key*")
        mock_redis.delete.assert_called_once_with("key1", "key2", "key3")


@pytest.mark.asyncio
async def test_cache_manager_exists_true():
    """Test CacheManager.exists returns True when key exists."""
    mock_redis = AsyncMock()
    mock_redis.exists.return_value = 1
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        result = await CacheManager.exists("test_key")
        assert result is True
        mock_redis.exists.assert_called_once_with("test_key")


@pytest.mark.asyncio
async def test_cache_manager_exists_false():
    """Test CacheManager.exists returns False when key doesn't exist."""
    mock_redis = AsyncMock()
    mock_redis.exists.return_value = 0
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        result = await CacheManager.exists("test_key")
        assert result is False


@pytest.mark.asyncio
async def test_cache_manager_get_json():
    """Test CacheManager.get_json returns parsed JSON."""
    mock_redis = AsyncMock()
    mock_redis.get.return_value = '{"name": "John", "age": 30}'
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        result = await CacheManager.get_json("test_key")
        assert result == {"name": "John", "age": 30}


@pytest.mark.asyncio
async def test_cache_manager_get_json_invalid():
    """Test CacheManager.get_json returns None for invalid JSON."""
    mock_redis = AsyncMock()
    mock_redis.get.return_value = "not valid json"
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        result = await CacheManager.get_json("test_key")
        assert result is None


@pytest.mark.asyncio
async def test_cache_manager_set_json():
    """Test CacheManager.set_json stores JSON data."""
    mock_redis = AsyncMock()
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        data = {"name": "John", "age": 30}
        result = await CacheManager.set_json("test_key", data, ttl=300)
        assert result is True
        mock_redis.setex.assert_called_once()
        args = mock_redis.setex.call_args[0]
        assert args[0] == "test_key"
        assert args[1] == 300
        # Verify JSON is valid
        import json
        assert json.loads(args[2]) == data


@pytest.mark.asyncio
async def test_cache_result_decorator_cache_hit():
    """Test cache_result decorator returns cached value."""
    mock_redis = AsyncMock()
    mock_redis.get.return_value = '"cached_result"'
    
    @cache_result("test", ttl=300)
    async def test_func(arg1: str):
        return f"result_{arg1}"
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        result = await test_func("value1")
        assert result == "cached_result"


@pytest.mark.asyncio
async def test_cache_result_decorator_cache_miss():
    """Test cache_result decorator executes function on cache miss."""
    mock_redis = AsyncMock()
    mock_redis.get.return_value = None
    
    @cache_result("test", ttl=300)
    async def test_func(arg1: str):
        return f"result_{arg1}"
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        result = await test_func("value1")
        assert result == "result_value1"
        # Verify it tried to cache the result
        mock_redis.setex.assert_called_once()


@pytest.mark.asyncio
async def test_invalidate_cache_decorator():
    """Test invalidate_cache decorator invalidates cache after execution."""
    mock_redis = AsyncMock()
    mock_redis.keys.return_value = ["test:key1", "test:key2"]
    mock_redis.delete.return_value = 2
    
    @invalidate_cache("test:*")
    async def test_func():
        return "result"
    
    with patch("app.utils.cache.get_redis", return_value=mock_redis):
        result = await test_func()
        assert result == "result"
        mock_redis.keys.assert_called_once_with("test:*")
        mock_redis.delete.assert_called_once_with("test:key1", "test:key2")
{%- endif %}
