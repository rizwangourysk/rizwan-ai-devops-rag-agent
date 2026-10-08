import subprocess
import time

from langchain_core.tools import tool


@tool
def restart_deployment(namespace: str, deployment: str) -> str:
    """
    Restart a Kubernetes deployment.
    """

    result = subprocess.run(
        [
            "kubectl",
            "rollout",
            "restart",
            f"deployment/{deployment}",
            "-n",
            namespace,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return f"Kubernetes restart failed:\n{result.stderr}"

    return result.stdout


@tool
def check_deployment_health(
    namespace: str,
    deployment: str,
) -> str:
    """
    Check whether a Kubernetes deployment is healthy.
    """

    result = subprocess.run(
        [
            "kubectl",
            "rollout",
            "status",
            f"deployment/{deployment}",
            "-n",
            namespace,
            "--timeout=30s",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        return f"Deployment is healthy:\n{result.stdout}"

    return (
        "Deployment is NOT healthy.\n"
        f"{result.stdout}\n"
        f"{result.stderr}"
    )


if __name__ == "__main__":

    print("--- Kubernetes Healing Tools ---")
    print("restart_deployment()")
    print("check_deployment_health()")

@tool
def fix_test_deployment(namespace: str, deployment: str) -> str:
    """
    Fix the intentionally broken test deployment.

    This is a controlled demo healing action.
    It removes the failing 'exit 1' command and restores nginx.
    """

    patch = (
        '{"spec":{"template":{"spec":{"containers":[{"name":"app",'
        '"command":["/bin/sh","-c"],'
        '"args":["nginx -g \\"daemon off;\\""]}]}}}}'
    )

    result = subprocess.run(
        [
            "kubectl",
            "patch",
            f"deployment/{deployment}",
            "-n",
            namespace,
            "--type=strategic",
            "-p",
            patch,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return f"Deployment healing failed:\n{result.stderr}"

    return result.stdout    
