#!/usr/bin/env python
"""
Post-generation hook for Cookiecutter.
This script runs after the project is generated.
"""

import json
import os
import subprocess


def run_command(command, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return None


def main():
    """Main post-generation hook function."""
    project_dir = os.getcwd()

    print("\nProject generated successfully!")
    print(f"Project directory: {project_dir}")

    # Get cookiecutter context
    # Cookiecutter doesn't directly pass context to hooks, so we need to read it from a file
    # that contains the context. We'll look for a file named .cookiecutter_context.json
    context_file_path = os.path.join(project_dir, ".cookiecutter_context.json")
    include_example = "y"  # Default value
    include_database = "n"  # Default value
    database_type = "sqlite"  # Default value

    if os.path.exists(context_file_path):
        try:
            with open(context_file_path, "r") as f:
                context = json.load(f)
                include_example = context.get("include_example", "y")
                include_database = context.get("include_database", "n")
                database_type = context.get("database_type", "sqlite")
            # Remove the context file as it's no longer needed
            os.remove(context_file_path)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read context file: {e}")

    # Remove example files if include_example is not "y"
    if include_example != "y":
        print("\nRemoving example files...")
        example_files = [
            "app/models/user.py",
            "app/routers/users.py",
            "app/schemas/user.py",
            "tests/unit/test_users.py",
        ]

        for file_path in example_files:
            full_path = os.path.join(project_dir, file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                print(f"Removed: {file_path}")

    # Remove database files if include_database is not "y"
    if include_database != "y":
        print("\nRemoving database files...")
        database_files = [
            "app/infrastructure/database.py",
        ]

        for file_path in database_files:
            full_path = os.path.join(project_dir, file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                print(f"Removed: {file_path}")

    # Initialize git repository
    print("\nInitializing git repository...")
    run_command("git init", cwd=project_dir)

    # Create initial commit
    print("Creating initial commit...")
    run_command("git add .", cwd=project_dir)
    run_command(
        "git commit -m 'Initial commit from FastAPI Backend template'", cwd=project_dir
    )

    # Run ruff format and check
    print("\nRunning code formatting and linting...")
    result = run_command("which uv")
    if result:
        print("Using uv to run ruff...")
        run_command("uv run ruff format .", cwd=project_dir)
        run_command("uv run ruff check --fix .", cwd=project_dir)
    else:
        print("uv not found. Running ruff with pip...")
        run_command("pip install ruff", cwd=project_dir)
        run_command("ruff format .", cwd=project_dir)
        run_command("ruff check --fix .", cwd=project_dir)

    print("\nNext steps:")
    print("1. cd into your project directory")
    print("2. Copy .env.example to .env and update the configuration")

    if include_database == "y":
        print("3. Set up your database:")
        if database_type == "sqlite":
            print("   - SQLite will create the database file automatically")
        elif database_type == "postgresql":
            print("   - Create a PostgreSQL database")
            print("   - Update the DATABASE_URL in .env with your database credentials")
        elif database_type == "mysql":
            print("   - Create a MySQL database")
            print("   - Update the DATABASE_URL in .env with your database credentials")

    print("4. Run the development server:")
    print("   uv run main.py")
    print("   or")
    print("   uvicorn main:app --reload")
    print("5. Open http://localhost:8080 in your browser")
    print("6. Check the health endpoint at http://localhost:8080/health")

    if include_example == "y":
        print("7. Try the user endpoints at http://localhost:8080/users")

    print("\nHappy coding!")


if __name__ == "__main__":
    main()
