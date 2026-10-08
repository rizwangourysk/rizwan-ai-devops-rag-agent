import json
import subprocess


def detect_kubernetes_failures():
    result = subprocess.run(
        ["kubectl", "get", "pods", "-A", "-o", "json"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return {
            "error": result.stderr
        }

    data = json.loads(result.stdout)

    failures = []

    for pod in data["items"]:

        namespace = pod["metadata"]["namespace"]
        pod_name = pod["metadata"]["name"]

        container_statuses = pod.get("status", {}).get(
            "containerStatuses", []
        )

        for container in container_statuses:

            state = container.get("state", {})

            waiting = state.get("waiting")

            if waiting:
                reason = waiting.get("reason", "")

                if reason in [
                    "CrashLoopBackOff",
                    "ImagePullBackOff",
                    "ErrImagePull",
                    "CreateContainerConfigError",
                ]:
                    failures.append(
                        {
                            "namespace": namespace,
                            "pod": pod_name,
                            "container": container["name"],
                            "reason": reason,
                        }
                    )

    return {
        "failures": failures
    }


if __name__ == "__main__":

    result = detect_kubernetes_failures()

    print("\n--- Kubernetes Failure Detection ---\n")

    print(json.dumps(result, indent=2))
