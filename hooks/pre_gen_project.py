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
    print("- app/core: Core application components (settings, logging)")
    print("- app/infrastructure: Infrastructure components (HTTP client, database)")
    print("- app/middleware: Custom middleware")
    print("- app/models: Data models")
    print("- app/routers: API routers")
    print("- app/schemas: Pydantic schemas")
    print("- app/utils: Utility functions")
    print("- tests: Test files")
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
        "include_example": "{{ cookiecutter.include_example }}",
        "include_database": "{{ cookiecutter.include_database }}",
        "database_type": "{{ cookiecutter.database_type }}",
    }

    # Write context to a file that will be included in the generated project
    with open(".cookiecutter_context.json", "w") as f:
        json.dump(context, f)


if __name__ == "__main__":
    main()
