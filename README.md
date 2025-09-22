# FastAPI Backend Cookiecutter Template

A Cookiecutter template for creating a FastAPI backend with best practices and a structured project layout.

## Features

- FastAPI framework with async support
- Structured project layout
- Configurable settings with Pydantic
- Colored logging
- Database support (optional)
- CORS support (optional)
- HTTP client (optional)
- Health check endpoint (optional)
- User management with models, schemas, and services (optional)
- Test setup with pytest (optional)
- Pre and post-generation hooks

## Requirements

- Python 3.13+
- Cookiecutter: `pip install cookiecutter`
- UV (recommended): `pip install uv`

## Usage

1. Install Cookiecutter:
   ```bash
   pip install cookiecutter
   ```

2. Generate a new project:
   ```bash
   cookiecutter https://github.com/haimatrix99/fastapi-backend-template
   ```

3. Follow the prompts to configure your project.

## Project Structure

```
{{ cookiecutter.project_slug }}/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── settings.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── http_client.py
│   ├── middleware/
│   │   └── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── utils/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_health.py
│   │   └── test_users.py
├── .env.example
├── .gitignore
├── main.py
├── pyproject.toml
└── README.md
```

## Running the Generated Project

After generating your project:

1. Navigate to the project directory:
   ```bash
   cd {{ cookiecutter.project_slug }}
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```
   or if you don't have uv:
   ```bash
   pip install -e .
   pip install -e '.[dev]'
   ```

3. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

4. Run the development server:
   ```bash
   uv run main.py
   ```
   or
   ```bash
   uvicorn main:app --reload
   ```

5. Open http://localhost:8080 in your browser

6. Check the health endpoint at http://localhost:8080/health

7. If user management was included, check the users endpoint at http://localhost:8080/users

## Running Tests

If you included tests in your project:

```bash
pytest
```

This will run all tests including:
- Unit tests for health endpoints
- Unit tests for user management (if included)

## Configuration

The application can be configured through environment variables. See `.env.example` for available options.

Key configuration options include:
- Application settings (host, port, debug mode)
- Database connection settings (if database support is included)
- CORS settings (if CORS support is included)
- Logging configuration
- API versioning

## Hooks

The template includes pre and post-generation hooks that:

- Pre-generation: Display information about the template and its features
- Post-generation:
  - Initialize git repository
  - Create initial commit
  - Install dependencies using UV or pip
  - Set up the project structure based on user selections

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Submit a pull request

## License

This project is licensed under the MIT License.