import subprocess

from langchain_core.tools import tool


@tool
def get_docker_containers() -> str:
    """Get all running Docker containers."""

    result = subprocess.run(
        ["docker", "ps"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return f"Docker error:\n{result.stderr}"

    return result.stdout


if __name__ == "__main__":
    print("--- Docker Containers ---")
    print(get_docker_containers.invoke({}))
