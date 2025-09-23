#!/usr/bin/env python
"""
Pre-generation hook for Cookiecutter.
This script runs before the project is generated.
"""

import json


def main():
    """Main pre-generation hook function."""
    print("Starting FastAPI Backend template generation...")
    print("This will create a new FastAPI project with the following structure:")
    print("- app/core/: Core application components (settings)")
    print("- app/infrastructure/: Infrastructure components (HTTP client, database)")
    print("- app/middleware/: Custom middleware")
    print("- app/models/: Data models")
    print("- app/routers/: API routers")
    print("- app/schemas/: Pydantic schemas")
    print("- app/services/: Business logic services")
    print("- app/utils/: Utility functions")
    print("- tests/: Test files (unit tests)")
    print("\nMake sure you have Python 3.13+ installed.")
    print("After generation, you can run the project with:")
    print("  uv run main.py")
    print("  or")
    print("  uvicorn main:app --reload")
    print("\nThe template includes Ruff for code formatting and linting.")
    print("After generation, Ruff will automatically format and check your code.")
    print("You can manually run Ruff with:")
    print("  uv run ruff format .")
    print("  uv run ruff check --fix .")

    # Save cookiecutter context to a file that will be read by the post-generation hook
    # This is needed because cookiecutter doesn't directly pass context to hooks
    context = {
        "project_name": "{{ cookiecutter.project_name }}",
        "project_slug": "{{ cookiecutter.project_slug }}",
        "project_description": "{{ cookiecutter.project_description }}",
        "author_name": "{{ cookiecutter.author_name }}",
        "author_email": "{{ cookiecutter.author_email }}",
        "version": "{{ cookiecutter.version }}",
        "include_example": "{{ cookiecutter.include_example }}",
        "include_tests": "{{ cookiecutter.include_tests }}",
        "include_database": "{{ cookiecutter.include_database }}",
        "database_type": "{{ cookiecutter.database_type }}",
        "database_url": "{{ cookiecutter.database_url }}",
    }

    # Write context to a file that will be included in the generated project
    with open(".cookiecutter_context.json", "w") as f:
        json.dump(context, f)


if __name__ == "__main__":
    main()
