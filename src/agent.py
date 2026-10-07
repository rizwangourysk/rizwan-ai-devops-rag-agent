from langchain_ollama import ChatOllama

from k8s_tools import get_pods
from docker_tools import get_docker_containers


llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0,
)


question = input("Enter your DevOps question: ")


# Ask the LLM which tool is required
decision = llm.invoke(
    f"""
You are an AI DevOps assistant.

User question:
{question}

Choose exactly ONE option:

GET_PODS
GET_DOCKER_CONTAINERS
NO_TOOL

Rules:

- If the question asks about Kubernetes pods or Kubernetes cluster information,
  respond only with GET_PODS.

- If the question asks about Docker containers or Docker information,
  respond only with GET_DOCKER_CONTAINERS.

- Otherwise respond only with NO_TOOL.
"""
)


tool_decision = decision.content.strip()

print("\n--- AI Decision ---\n")
print(tool_decision)


# Kubernetes tool
if "GET_PODS" in tool_decision:

    result = get_pods.invoke({})

    print("\n--- Kubernetes Tool Result ---\n")
    print(result)

    final_response = llm.invoke(
        f"""
You are an AI DevOps assistant.

User question:
{question}

Current Kubernetes information:
{result}

Answer the user's question using the real Kubernetes information.

Give a simple and clear answer.
"""
    )

    print("\n--- AI DevOps Agent Answer ---\n")
    print(final_response.content)


# Docker tool
elif "GET_DOCKER_CONTAINERS" in tool_decision:

    result = get_docker_containers.invoke({})

    print("\n--- Docker Tool Result ---\n")
    print(result)

    final_response = llm.invoke(
        f"""
You are an AI DevOps assistant.

User question:
{question}

Current Docker information:
{result}

Answer the user's question using the real Docker information.

Give a simple and clear answer.
"""
    )

    print("\n--- AI DevOps Agent Answer ---\n")
    print(final_response.content)


# No tool required
else:

    final_response = llm.invoke(
        f"""
You are an AI DevOps assistant.

User question:
{question}

Answer the question clearly and simply.
"""
    )

    print("\n--- AI DevOps Agent Answer ---\n")
    print(final_response.content)
