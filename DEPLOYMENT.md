# Deployment

## Quadlet Architecture
Each service is a `.container` file in `~/.config/containers/systemd/`.
All managed by systemd with declared dependencies.

## Disaster Recovery
Full stack rebuild from git in under 15 minutes.
All data persists in Podman volumes.
