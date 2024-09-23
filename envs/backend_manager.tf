variable "ENV" {
  description = "the name of the environment to load"
  default     = "dev"
}

module "backend" {
  source          = "Apollo-XIV/backend-manager/aws"
  version         = "0.0.27"
  prefix          = "tfdocs"
  force_destroy   = false
  enable_dynamodb = false

  output_dir = "../."

  environment_configs_dir = abspath("${path.root}")
  environments = [
    "dev",
    "staging"
  ]
  ENV = var.ENV

  variables = {
    name  = "string"
    apply = "bool"
  }

  approved_arns = [
    "arn:aws:iam::013948180024:user/desktop"
  ]
}
