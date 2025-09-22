# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Installation

### Prerequisites

- Python {{ cookiecutter.python_version }} or higher
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

3. Create a `.env` file by copying the example:
   ```bash
   cp .env.example .env
   ```

4. Modify the `.env` file to match your environment settings if needed.

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
