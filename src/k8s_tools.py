import subprocess

from langchain_core.tools import tool


@tool
def get_pods() -> str:
    """Get all Kubernetes pods from the cluster."""

    result = subprocess.run(
        ["kubectl", "get", "pods", "-A"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return f"Kubernetes error:\n{result.stderr}"

    return result.stdout


if __name__ == "__main__":
    print("--- Kubernetes Pods ---")
    print(get_pods.invoke({}))
