#!/usr/bin/env python
"""
Post-generation hook for Cookiecutter.
This script runs after the project is generated.
"""

import json
import os
import subprocess
import sys


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

    # Get cookiecutter context from environment variables
    # Cookiecutter sets COOKIECUTTER_* environment variables
    include_example = "{{ cookiecutter.include_example }}"
    include_database = "{{ cookiecutter.include_database }}"
    include_redis = "{{ cookiecutter.include_redis }}"
    database_type = "{{ cookiecutter.database_type }}"

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

    # Remove Redis files if include_redis is not "y"
    if include_redis != "y":
        print("\nRemoving Redis files...")
        redis_files = [
            "app/infrastructure/redis.py",
            "app/routers/cache.py",
            "app/utils/cache.py",
            "tests/unit/test_cache.py",
            "tests/unit/test_cache_router.py",
        ]

        for file_path in redis_files:
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

    # Run ruff format and check
    print("\nRunning code formatting and linting...")
    result = run_command("which uv")
    if result:
        print("Using uv to run ruff...")
        ruff_prefix = "uv run "
    else:
        print("uv not found. Running ruff with pip...")
        run_command("pip install ruff", cwd=project_dir)
        ruff_prefix = ""
    
    run_command(f"{ruff_prefix}ruff format .", cwd=project_dir)
    run_command(f"{ruff_prefix}ruff check --fix .", cwd=project_dir)

    print("\nNext steps:")
    print("1. cd into your project directory")
    print("2. Copy .env.example to .env and update the configuration")

    step_num = 3
    if include_database == "y":
        print(f"{step_num}. Set up your database:")
        if database_type == "sqlite":
            print("   - SQLite will create the database file automatically")
        elif database_type == "postgresql":
            print("   - Create a PostgreSQL database")
            print("   - Update the DATABASE_URL in .env with your database credentials")
        elif database_type == "mysql":
            print("   - Create a MySQL database")
            print("   - Update the DATABASE_URL in .env with your database credentials")
        step_num += 1

    if include_redis == "y":
        print(f"{step_num}. Set up Redis (optional):")
        print("   - Run Redis locally or use Docker: docker run -d -p 6379:6379 redis:latest")
        print("   - Or set REDIS_ENABLED=false in .env to disable")
        step_num += 1

    print(f"{step_num}. Run the development server:")
    print("   uv run main.py")
    print("   or")
    print("   uvicorn main:app --reload")
    step_num += 1
    print(f"{step_num}. Open http://localhost:8080 in your browser")
    step_num += 1
    print(f"{step_num}. Check the health endpoint at http://localhost:8080/health")
    step_num += 1

    if include_example == "y":
        print(f"{step_num}. Try the user endpoints at http://localhost:8080/users")
        if include_redis == "y":
            print(f"{step_num + 1}. Try the cache endpoints at http://localhost:8080/cache")

    # Initialize git repository
    print("\nInitializing git repository...")
    run_command("git init", cwd=project_dir)

    # Create initial commit
    print("Creating initial commit...")
    run_command("git add .", cwd=project_dir)
    run_command(
        "git commit -m 'Initial commit from FastAPI Backend template'", cwd=project_dir
    )

    print("\nHappy coding!")


if __name__ == "__main__":
    main()
