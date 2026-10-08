import subprocess

from langchain_core.tools import tool


@tool
def get_pod_logs(namespace: str, pod: str) -> str:
    """
    Get the logs of a Kubernetes pod.
    """

    result = subprocess.run(
        [
            "kubectl",
            "logs",
            pod,
            "-n",
            namespace,
            "--tail=100",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return f"Failed to get pod logs:\n{result.stderr}"

    return result.stdout


@tool
def get_pod_details(namespace: str, pod: str) -> str:
    """
    Get detailed Kubernetes information about a pod.
    """

    result = subprocess.run(
        [
            "kubectl",
            "describe",
            "pod",
            pod,
            "-n",
            namespace,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return f"Failed to describe pod:\n{result.stderr}"

    return result.stdout


if __name__ == "__main__":

    print("--- Kubernetes Diagnosis Tools ---")
    print("get_pod_logs()")
    print("get_pod_details()")
