# Kubernetes Troubleshooting Guide

## Pod Pending

A Pod in Pending state means Kubernetes has accepted the Pod but cannot schedule it onto a node.

Common causes:
- Not enough CPU or memory
- Node selector does not match
- Taints and tolerations are not configured correctly
- PersistentVolumeClaim is not available

Useful commands:

kubectl get pods -A
kubectl describe pod <pod-name>
kubectl get nodes
kubectl describe nodes

## CrashLoopBackOff

CrashLoopBackOff means a container starts and then repeatedly crashes.

Common causes:
- Application error
- Missing environment variable
- Database connection failure
- Incorrect configuration
- Application listening on the wrong port

Useful commands:

kubectl get pods -A
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
kubectl describe pod <pod-name>

## ImagePullBackOff

ImagePullBackOff means Kubernetes cannot pull the container image.

Common causes:
- Image name is incorrect
- Image tag does not exist
- Container registry authentication failure
- Private registry access problem

Useful commands:

kubectl get pods -A
kubectl describe pod <pod-name>

## Service Troubleshooting

If a Kubernetes Service cannot reach the application, check:

- Service selector
- Pod labels
- Service port
- Target port
- Pod readiness

Useful commands:

kubectl get services
kubectl describe service <service-name>
kubectl get pods --show-labels
kubectl get endpoints <service-name>

## Deployment Troubleshooting

Useful commands:

kubectl get deployments
kubectl describe deployment <deployment-name>
kubectl rollout status deployment/<deployment-name>
kubectl rollout history deployment/<deployment-name>

To rollback a deployment:

kubectl rollout undo deployment/<deployment-name>
