---
name: rc-terraform
description: Designs and manages infrastructure as code with Terraform — modules, remote state (S3 + DynamoDB), Stacks (deployments), test framework, preconditions/postconditions, moved/removed blocks, and CI/CD plan/apply separation. Use when users ask to write Terraform config, set up remote state, design modules, manage infrastructure state, or automate provisioning.
---

# Terraform

Production-grade infrastructure as code with Terraform 1.10+: Stacks, state management, testing, and CI/CD separation.

## Before You Write Terraform

Answer these questions:

- How many environments? (dev, staging, prod)
- Are you a solo developer or a team?
- Where will you store state? (S3 + DynamoDB, Google GCS, Terraform Cloud)
- How will you isolate environments? (directories, Stacks, workspaces—prefer directories)

## Project Structure by Scale

| Scale | Structure | State Strategy |
| --- | --- | --- |
| Personal | Single `main.tf` | Remote backend, optional workspaces |
| Team (2-5) | `envs/{dev,prod}/modules/` | Directory-per-environment, separate backends |
| Platform team | `infra/{networking,compute,data,iam}/` per repo | Per-component state, `terraform_remote_state` |

## Remote State Backend (S3 + DynamoDB)

```hcl
terraform {
  backend "s3" {
    bucket         = "tf-state-{account}-{region}"
    key            = "{env}/{component}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "tf-state-lock"
  }
  required_version = ">= 1.10"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}
```

State locking prevents concurrent applies that corrupt state.

## Module Design

One module = one domain. Single responsibility:

```
modules/
├ networking/
│   ├ main.tf
│   ├ variables.tf
│   └ outputs.tf
├ compute/
│   ├ main.tf
│   ├ variables.tf
│   └ outputs.tf
└ database/
    ├ main.tf
    ├ variables.tf
    └ outputs.tf

environments/
├ prod/
│   ├ backend.tf (key = "prod/compute/terraform.tfstate")
│   ├ main.tf
│   └ terraform.tfvars
└ dev/
    ├ backend.tf (key = "dev/compute/terraform.tfstate")
    ├ main.tf
    └ terraform.tfvars
```

## Preconditions and Postconditions

Validate assumptions and outcomes:

```hcl
resource "aws_db_instance" "main" {
  allocated_storage = 100
  engine            = "postgres"
  engine_version    = "16.3"

  lifecycle {
    precondition {
      condition     = var.allocated_storage >= 100
      error_message = "Database must have at least 100 GB"
    }
    postcondition {
      condition     = self.engine == "postgres"
      error_message = "Only PostgreSQL is supported"
    }
  }
}
```

## State Refactoring with `moved` Blocks

Instead of manual `terraform state mv`, use code-reviewed `moved` blocks:

```hcl
moved {
  from = aws_s3_bucket.old
  to   = module.storage.aws_s3_bucket.main
}

removed {
  from = aws_instance.legacy
  lifecycle {
    destroy = false  # Keep the resource alive, just remove from state
  }
}
```

## Terraform Stacks (2025+)

Deploy multiple configurations with shared state:

```hcl
stack "dev" {
  source = "./infrastructure"
  path   = "dev"
}

stack "prod" {
  source = "./infrastructure"
  path   = "prod"
}
```

## Testing Framework

```hcl
run "create_bucket" {
  command = apply
  variables {
    bucket_name = "test-bucket-${run_id}"
  }
  assert {
    condition     = aws_s3_bucket.main.bucket == "test-bucket-${run_id}"
    error_message = "Bucket name mismatch"
  }
}
```

Run: `terraform test`

## State Management Rules

| Rule | Why |
| --- | --- |
| Remote state always | Local is single-player |
| S3 + DynamoDB | Standard state storage + locking |
| Versioning on state bucket | Rollback bad apply |
| KMS encryption | State files contain secrets |
| Per-environment isolation | `destroy` in dev should never touch prod |
| Per-component state | Change in IAM should not re-evaluate RDS |
| Directory-per-environment | Workspaces share backend—too easy to select prod by accident |
| `moved` blocks over `state rm/mv` | Code-reviewed, reversible, self-documenting |

## Provider Pinning Strategy

```hcl
terraform {
  required_providers {
    aws        = { source = "hashicorp/aws", version = "~> 5.0" }
    kubernetes = { source = "hashicorp/kubernetes", version = ">= 2.20, < 3.0" }
  }
}
```

- `~> 5.0`: Allow minor updates (5.0 to 5.x)
- `>= 2.20, < 3.0`: Explicit range
- Never `latest`

## CI/CD Pipeline (GitHub Actions)

```yaml
name: Terraform
on: [pull_request, push]
jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform fmt -check
      - run: terraform validate
      - run: terraform plan -out=tfplan
      - uses: actions/upload-artifact@v4
        with: {name: tfplan, path: tfplan}

  apply:
    if: github.ref == 'refs/heads/main'
    needs: [plan]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - uses: actions/download-artifact@v4
        with: {name: tfplan}
      - run: terraform apply tfplan
```

## Pre-Apply Checklist

Before `terraform apply`:

- [ ] `terraform fmt -recursive` passes
- [ ] `terraform validate` passes
- [ ] `terraform plan` reviewed—no unexpected replacements
- [ ] Stateful resources (RDS, S3, disks) have `prevent_destroy = true`
- [ ] Remote backend configured with state locking
- [ ] Provider versions pinned (`~> X.Y` or exact)
- [ ] Preconditions/postconditions on critical resources
- [ ] `moved` blocks for renamed resources
- [ ] Sensitive outputs marked with `sensitive = true`
- [ ] Plan file reviewed by a second person for production changes
- [ ] `terraform apply` runs from CI/CD, not a developer laptop

## Emergency State Surgery

| Situation | Command |
| --- | --- |
| Remove resource from state (keep real) | `terraform state rm <address>` |
| Import existing resource | `terraform import <address> <id>` |
| Move resource (refactoring) | `terraform state mv <from> <to>` |
| Unlock stuck state | `terraform force-unlock <lock-id>` |
| Rollback corrupted state | Restore previous S3 version |
| List resources | `terraform state list` |
| Show resource details | `terraform state show <address>` |

## Anti-Patterns

| Anti-Pattern | Fix |
| --- | --- |
| Local state in team project | Remote state (S3 + DynamoDB) |
| One giant state file | Split by component |
| Workspaces for env isolation | Directory-per-environment |
| Manual `state mv` instead of `moved` blocks | Code-reviewed `moved` blocks |
| `latest` provider version | Pin `~> 5.0` |
| Running `apply` from laptop | CI/CD with saved plan |
| No locking | DynamoDB table for state lock |
| Secrets in state outputs | Mark `sensitive = true`, use external secrets manager |

## Sources

- Terraform documentation (developer.hashicorp.com/terraform)
- Terraform Stacks — HCP documentation
- Terraform Test Framework
- HashiCorp Learn: `moved` blocks
- AWS Well-Architected IaC patterns
