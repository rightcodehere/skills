---
name: rc-kubernetes
description: Deploys, manages, and debugs Kubernetes in production — Deployments, Services, Gateway API, service mesh (Istio/Linkerd/Cilium), zero-trust networking (NetworkPolicy), pod security hardening (Pod Security Standards, non-root, read-only filesystem), autoscaling (HPA, PDB), and debugging. Use when users ask to write K8s manifests, deploy to a cluster, debug pods, configure ingress, set up autoscaling, or harden cluster security.
---

# Kubernetes

Production-grade Kubernetes: Deployments, Services, Gateway API, security hardening, and debugging.

## Before You Deploy to Kubernetes

Answer these questions:

- Does the app need horizontal scaling (3+ replicas)? → Kubernetes
- Is it a single-instance app with simple needs? → Docker Compose or VPS
- Is the team familiar with Kubernetes? → Proceed. If not, consider managed (EKS, GKE, AKS)
- Does the app need advanced networking? → Kubernetes + Gateway API
- Is the infrastructure budget tight? → Single-node k3s or Docker Compose for dev

## Deployment Types

| Type | Kind | Use Case |
| --- | --- | --- |
| Stateless | Deployment | Web APIs, workers |
| Stateful | StatefulSet | Databases, queues (use with caution) |
| Batch | Job/CronJob | Migrations, periodic tasks |
| Daemon | DaemonSet | Logging, monitoring agents |

When uncertain, start with a Deployment.

## Core Kubernetes Resources

- **Deployment**: Manages replicas of a stateless application with rolling updates
- **Service**: Exposes a Deployment internally (ClusterIP) or externally (LoadBalancer, NodePort)
- **ConfigMap**: Non-sensitive configuration data
- **Secret**: Sensitive data (use external provider like Vault)
- **PersistentVolume**: Cluster-level storage resource
- **PersistentVolumeClaim**: Pod's request for storage
- **Namespace**: Logical isolation of resources

## Gateway API (Replaces Legacy Ingress)

Gateway API is the modern, standardized approach to traffic routing:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: api-gateway
spec:
  gatewayClassName: istio
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
      hostname: api.example.com
      tls:
        mode: Terminate
        certificateRefs: [{name: api-tls}]
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api-route
spec:
  parentRefs: [{name: api-gateway}]
  hostnames: ["api.example.com"]
  rules:
    - matches:
        - path: {type: PathPrefix, value: /api}
      backendRefs:
        - name: api
          port: 80
```

Supports traffic splitting, header matching, and multi-tenancy.

## Zero-Trust Networking (NetworkPolicy)

Always start with a default-deny policy, then explicitly allow traffic:

```yaml
# Default deny all
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
---
# Allow traffic from gateway to api
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-ingress
spec:
  podSelector: {matchLabels: {app: api}}
  ingress:
    - from:
        - namespaceSelector: {matchLabels: {name: gateway-system}}
      ports: [{port: 3000}]
```

## Pod Security Hardening (NSA/CISA Guidelines)

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000
containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: [ALL]
      seccompProfile:
        type: RuntimeDefault
```

Every production pod must pass these 6 checks:
1. Run as non-root
2. Read-only root filesystem
3. Drop all capabilities
4. Disallow privilege escalation
5. Apply default seccomp profile
6. Run with restricted Pod Security Standard

## Service Mesh (When Needed)

| Tool | Best For | Complexity |
| --- | --- | --- |
| Istio | Full-featured mTLS + observability | High |
| Linkerd | Lightweight mTLS + low overhead | Medium |
| Cilium | eBPF-native, no sidecar | High (but powerful) |

Start without a service mesh. Add only if you need cross-service encryption and observability.

## Horizontal Pod Autoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: {type: Utilization, averageUtilization: 70}
    - type: Resource
      resource:
        name: memory
        target: {type: Utilization, averageUtilization: 80}
```

## Pod Disruption Budget (Ensures HA)

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels: {app: api}
```

Ensures at least 2 replicas remain available during planned maintenance.

## Resource Requests and Limits

Always set both:

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "256Mi"
```

- **Requests**: Reserved resources for scheduling
- **Limits**: Hard ceiling to prevent starving other pods

## Probes (Liveness and Readiness)

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /ready
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 5
```

- **Liveness**: Is the app alive? Restart if it fails.
- **Readiness**: Is the app ready to receive traffic? Remove from service if it fails.

## Production Hardening Checklist

- [ ] All containers run as non-root
- [ ] Pod Security Standard `restricted` applied to all namespaces
- [ ] NetworkPolicy `default-deny-all` with explicit allow rules
- [ ] Image pinned by digest, not tag
- [ ] Resource requests AND limits on every container
- [ ] Readiness AND liveness probes configured
- [ ] PodDisruptionBudget with `minAvailable: 1` or higher
- [ ] Secrets stored in external manager (Vault, Sealed Secrets)
- [ ] `automountServiceAccountToken: false` unless genuinely needed
- [ ] `allowPrivilegeEscalation: false`
- [ ] TLS enabled on ingress with cert-manager auto-renewal
- [ ] Audit logging enabled

## Common Debugging Commands

```bash
# Get pod status
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # Crashed container logs

# Port forward
kubectl port-forward svc/<service-name> 8080:80

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check service discovery
kubectl exec -it <pod> -- nslookup <service-name>
```

## Anti-Patterns

| Anti-Pattern | Fix |
| --- | --- |
| `image: myapp:latest` | `image: myapp@sha256:abc...` (pin by digest) |
| No resource limits | Set requests + limits |
| Running as root | `securityContext: {runAsNonRoot: true}` |
| Single replica | Always >= 2 for HA |
| No probes | Liveness + readiness mandatory |
| Hardcoded config | Use ConfigMap + Secret |
| No NetworkPolicy | Default-deny per namespace |
| Legacy Ingress | Migrate to Gateway API |

## Sources

- Kubernetes official documentation (kubernetes.io)
- Gateway API (gateway-api.sigs.k8s.io)
- NSA/CISA Kubernetes Hardening Guide
- OWASP Kubernetes Security
- Helm (helm.sh) and Kustomize (kustomize.io)
