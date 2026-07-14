# Architecture

## Network Topology
Internet → OCI Load Balancer (TLS 1.3, Let's Encrypt auto-renew)
  → Public Subnet (10.0.0.0/24)
    → Private Subnet (10.0.1.0/24)
      → Compute A1.Flex (4 OCPU, 24GB RAM, Oracle Linux 9)
        → Podman Quadlets (12 services, systemd-managed)

## Service Mesh
All services on single bridge network with internal DNS.
Only the API Gateway is published to the host.
Secrets via OCI Vault → podman secret → container environment.
Zero .env files. Zero hardcoded passwords.
