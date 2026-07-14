# Performance & Scale

## Current Stack (Always Free)
- **Compute**: A1.Flex 4 OCPU / 24GB RAM
- **Storage**: 200GB block + 20GB object
- **Network**: 10 Mbps LB, 10 TB egress/month
- **Databases**: 4 engines, all within free tier

## Capacity Headroom
| Resource | Used | Free Tier Limit | Headroom |
|----------|------|-----------------|----------|
| OCPU | ~1.5 (avg) | 4 | 62% |
| RAM | ~12GB | 24GB | 50% |
| Block Storage | ~80GB | 200GB | 60% |
| Object Storage | ~5GB | 20GB | 75% |
| NoSQL Reads | ~15K/mo | 133M/mo | 99.9% |

## Scaling Strategy
1. **Vertical**: Upgrade A1.Flex shape (up to 64 OCPU)
2. **Horizontal**: Migrate to OKE (Kubernetes)
3. **Database**: Move to managed services (OCI Database, MySQL HeatWave)
