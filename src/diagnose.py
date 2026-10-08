from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0,
)


def diagnose_failure(failure, logs="", pod_details=""):

    prompt = f"""
You are an AI Kubernetes troubleshooting assistant.

A Kubernetes failure was detected.

FAILURE INFORMATION
-------------------

Namespace:
{failure["namespace"]}

Pod:
{failure["pod"]}

Container:
{failure["container"]}

Failure reason:
{failure["reason"]}


POD LOGS
--------

{logs}


POD DETAILS
-----------

{pod_details}


TASK
----

Analyze the actual Kubernetes evidence.

Explain:

1. What is the exact problem?
2. What is the root cause?
3. What evidence proves the root cause?
4. What should a DevOps engineer do to fix it?
5. Is restarting the deployment enough to fix the problem?

Do not guess when the evidence already shows the root cause.

Give a simple and practical DevOps answer.
"""

    response = llm.invoke(prompt)

    return response.content


if __name__ == "__main__":

    test_failure = {
        "namespace": "default",
        "pod": "self-healing-demo-85d6f4466-r7vkr",
        "container": "app",
        "reason": "CrashLoopBackOff",
    }

    logs = ""

    pod_details = """
Command:
  /bin/sh
  -c

Args:
  exit 1

State:
  Waiting
  Reason: CrashLoopBackOff

Last State:
  Terminated
  Reason: Error
  Exit Code: 1

Restart Count:
  5

Events:
  Container image nginx:1.27 was pulled.
  Container was created.
  Container was started.
  Back-off restarting failed container.
"""

    print("\n--- AI Kubernetes Diagnosis ---\n")

    diagnosis = diagnose_failure(
        test_failure,
        logs,
        pod_details,
    )

    print(diagnosis)
