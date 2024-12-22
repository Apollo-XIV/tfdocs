variable "ENV" {
  description = "the name of the environment to load"
  default     = "dev"
}

module "backend" {
  source          = "Apollo-XIV/backend-manager/aws"
  version         = "0.0.30"
  prefix          = "tfdocs"
  force_destroy   = false
  enable_dynamodb = false

  output_dir = "../infra"

  environment_configs_dir = abspath(path.root)
  environments = [
    "dev",
    "staging"
  ]
  ENV = var.ENV

  variables = {
    name       = "string"
    apply      = "bool"
    bastion    = "bool"
    node_count = "number"
  }

  approved_arns = [
    "arn:aws:iam::013948180024:user/desktop",
    "arn:aws:iam::013948180024:user/github"
  ]
}

output "backend" {
  value = module.backend.bucket
}
