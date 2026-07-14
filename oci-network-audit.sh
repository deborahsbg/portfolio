#!/bin/bash
# OCI Network Audit — lists all security lists and NSG rules
# Demonstrates OCI CLI proficiency

COMPARTMENT_ID=$1

echo "=== Security Lists ==="
oci network security-list list --compartment-id "$COMPARTMENT_ID" \
  --query 'data[*].{name:"display-name", rules:"ingress-security-rules"}' \
  --output table --auth instance_principal

echo "=== Network Security Groups ==="
oci network nsg list --compartment-id "$COMPARTMENT_ID" \
  --query 'data[*].{name:"display-name", rules:"security-rules"}' \
  --output table --auth instance_principal
