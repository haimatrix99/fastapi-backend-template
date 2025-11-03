# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Installation

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd {{ cookiecutter.project_slug }}
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

   If you don't have uv installed, you can install it with:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Alternatively, you can use pip:
   ```bash
   pip install -e .
   ```
{% if cookiecutter.include_redis == "y" -%}

3. Set up Redis (optional but recommended):
   
   **Using Docker:**
   ```bash
   docker run -d -p 6379:6379 --name redis redis:latest
   ```
   
   **Or install Redis locally:**
   - Ubuntu/Debian: `sudo apt-get install redis-server`
   - macOS: `brew install redis`
   - Windows: [Download from Redis website](https://redis.io/download)
   
   To disable Redis, set `REDIS_ENABLED=false` in your `.env` file.

4. Create a `.env` file by copying the example:
{%- else -%}

3. Create a `.env` file by copying the example:
{%- endif %}
   ```bash
   cp .env.example .env
   ```
{% if cookiecutter.include_redis == "y" -%}

5. Modify the `.env` file to match your environment settings if needed.
{%- else -%}

4. Modify the `.env` file to match your environment settings if needed.
{%- endif %}

## Running the Application

To start the development server:
```bash
uv run python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8080`

## Development

### Running Tests

If tests are included in your project, run them with:
```bash
uv run pytest
```

### Adding Dependencies

To add a new dependency:
```bash
uv add <package-name>
```

To add a development dependency:
```bash
uv add --group dev <package-name>
```

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`
{% if cookiecutter.include_redis == "y" -%}

## Redis Caching

This application includes Redis caching support for improved performance.

### Configuration

Redis settings can be configured via environment variables in your `.env` file:

```env
REDIS_ENABLED=true                          # Enable/disable Redis
REDIS_URL="redis://localhost:6379/0"       # Redis connection URL
REDIS_MAX_CONNECTIONS=10                    # Maximum connection pool size
REDIS_DECODE_RESPONSES=true                 # Automatically decode responses to strings
REDIS_SOCKET_TIMEOUT=5                      # Socket timeout in seconds
REDIS_SOCKET_CONNECT_TIMEOUT=5              # Connection timeout in seconds
```

### Using Cache in Your Code

The template provides a `CacheManager` utility class for easy cache operations:

```python
from app.utils.cache import CacheManager

# Set a value in cache
await CacheManager.set("my_key", "my_value", ttl=300)  # TTL in seconds

# Get a value from cache
value = await CacheManager.get("my_key")

# Store JSON data
await CacheManager.set_json("user:1", {"name": "John", "email": "john@example.com"}, ttl=600)

# Retrieve JSON data
user_data = await CacheManager.get_json("user:1")

# Delete a key
await CacheManager.delete("my_key")

# Delete keys matching a pattern
await CacheManager.delete_pattern("user:*")
```

### Cache Decorators

You can use decorators to automatically cache function results:

```python
from app.utils.cache import cache_result, invalidate_cache

@cache_result("user", ttl=300)
async def get_user(user_id: int):
    # This function's result will be cached for 5 minutes
    return await fetch_user_from_db(user_id)

@invalidate_cache("user:*")
async def update_user(user_id: int, data: dict):
    # This will invalidate all user cache entries after execution
    return await update_user_in_db(user_id, data)
```

### Cache Endpoints

If you included example endpoints, cache management endpoints are available at:
- `GET /cache/get/{key}` - Get a cached value
- `POST /cache/set/{key}` - Set a cache value (with optional TTL)
- `DELETE /cache/delete/{key}` - Delete a cached value
- `GET /cache/exists/{key}` - Check if a key exists
- `DELETE /cache/clear/{pattern}` - Clear cache keys matching a pattern
{%- endif %}
