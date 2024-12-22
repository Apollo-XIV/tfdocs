locals {
  prefix = "tfdocs-${var.env}"
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_instance" "jumpbox" {
  // Used to ssh into autoscaling instances and troubleshoot
  count                       = var.bastion ? 1 : 0
  associate_public_ip_address = true
  subnet_id                   = module.network.public_subnets[0]
  user_data_replace_on_change = true

  launch_template {
    id      = aws_launch_template.tmpl.id
    version = aws_launch_template.tmpl.latest_version
  }

  lifecycle {
    replace_triggered_by = [
      aws_launch_template.tmpl
    ]
  }
}
