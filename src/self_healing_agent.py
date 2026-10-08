import json
import subprocess

from detect_failures import detect_kubernetes_failures
from diagnose import diagnose_failure
from healing_tools import (
    restart_deployment,
    check_deployment_health,
    fix_test_deployment,
)
from k8s_diagnosis_tools import (
    get_pod_logs,
    get_pod_details,
)


def get_deployment_name(namespace, pod_name):

    pod_result = subprocess.run(
        [
            "kubectl",
            "get",
            "pod",
            pod_name,
            "-n",
            namespace,
            "-o",
            "json",
        ],
        capture_output=True,
        text=True,
    )

    if pod_result.returncode != 0:
        return None

    pod_data = json.loads(pod_result.stdout)

    owners = pod_data.get(
        "metadata",
        {}
    ).get(
        "ownerReferences",
        []
    )

    replica_set = None

    for owner in owners:

        if owner.get("kind") == "ReplicaSet":

            replica_set = owner.get("name")

    if not replica_set:
        return None

    rs_result = subprocess.run(
        [
            "kubectl",
            "get",
            "replicaset",
            replica_set,
            "-n",
            namespace,
            "-o",
            "json",
        ],
        capture_output=True,
        text=True,
    )

    if rs_result.returncode != 0:
        return None

    rs_data = json.loads(rs_result.stdout)

    rs_owners = rs_data.get(
        "metadata",
        {}
    ).get(
        "ownerReferences",
        []
    )

    for owner in rs_owners:

        if owner.get("kind") == "Deployment":

            return owner.get("name")

    return None


def main():

    print(
        "\n--- AI DevOps Self-Healing Agent ---\n"
    )

    # ==================================================
    # STEP 1: Detect Kubernetes failures
    # ==================================================

    failures = detect_kubernetes_failures()

    if "error" in failures:

        print(
            failures["error"]
        )

        return

    failure_list = failures.get(
        "failures",
        []
    )

    if not failure_list:

        print(
            "No Kubernetes failures detected."
        )

        return

    # ==================================================
    # Process each failure
    # ==================================================

    for failure in failure_list:

        print(
            "Failure detected:"
        )

        print(failure)

        namespace = failure["namespace"]

        pod = failure["pod"]

        # ==================================================
        # STEP 2: Collect pod logs
        # ==================================================

        print(
            "\n--- Collecting Pod Logs ---\n"
        )

        logs = get_pod_logs.invoke(
            {
                "namespace": namespace,
                "pod": pod,
            }
        )

        print(logs)

        # ==================================================
        # STEP 3: Collect pod details
        # ==================================================

        print(
            "\n--- Collecting Pod Details ---\n"
        )

        pod_details = get_pod_details.invoke(
            {
                "namespace": namespace,
                "pod": pod,
            }
        )

        print(pod_details)

        # ==================================================
        # STEP 4: AI diagnosis
        # ==================================================

        print(
            "\n--- AI Diagnosis ---\n"
        )

        diagnosis = diagnose_failure(
            failure,
            logs,
            pod_details,
        )

        print(diagnosis)

        # ==================================================
        # STEP 5: Find Deployment
        # ==================================================

        deployment = get_deployment_name(
            namespace,
            pod,
        )

        if not deployment:

            print(
                "\nCould not find the Deployment "
                "that owns this pod."
            )

            continue

        print(
            "\nDeployment found:"
        )

        print(deployment)

        # ==================================================
        # STEP 6: Check supported failure type
        # ==================================================

        if failure["reason"] != "CrashLoopBackOff":

            print(
                "\nAutomatic healing is not enabled "
                "for this failure type."
            )

            continue

        # ==================================================
        # STEP 7: Controlled self-healing
        # ==================================================

        print(
            "\n--- Self-Healing Action ---\n"
        )

        print(
            "CrashLoopBackOff detected."
        )

        print(
            "Executing the controlled healing action..."
        )

        healing_result = fix_test_deployment.invoke(
            {
                "namespace": namespace,
                "deployment": deployment,
            }
        )

        print(
            healing_result
        )

        # ==================================================
        # STEP 8: Health verification
        # ==================================================

        print(
            "\n--- Health Check ---\n"
        )

        health_result = check_deployment_health.invoke(
            {
                "namespace": namespace,
                "deployment": deployment,
            }
        )

        print(
            health_result
        )


if __name__ == "__main__":

    main()
