#------------- ASG Resources

locals {
  nixos_ami = "ami-0e7d1823ac80520e6"
}

data "aws_ami" "nixos" {
  owners      = ["427812963091"]
  most_recent = true

  filter {
    name   = "name"
    values = ["nixos/24.11*"]
  }
  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

resource "aws_launch_template" "tmpl" {
  name_prefix   = "${local.prefix}-lt"
  instance_type = "t2.micro"
  image_id      = data.aws_ami.nixos.id
  user_data = base64encode(<<-EOF
    useradd -m -s /bin/bash webuser
    # Temporarily install awscliv2
    nix-shell -p awscli2

    mkdir -p /var/www/tfdocs
    aws s3 cp s3://${aws_s3_bucket.artefacts.bucket}/${aws_s3_object.app_archive.key} /var/www/tfdocs
    chown -R webuser:webuser /var/www/tfdocs

    cd /var/www/tfdocs
    nix develop
    # Start the webserver
    sudo -u webuser nohup python3 -m web &
  EOF
  )

  metadata_options {
    http_tokens   = "required" # This ensures that IMDSv2 is required
    http_endpoint = "enabled"  # This keeps the metadata endpoint enabled
  }

  monitoring {
    enabled = true
  }

  iam_instance_profile {
    arn = aws_iam_instance_profile.web.arn // profile with iam permissions to artefact bucket
  }
}

resource "aws_autoscaling_group" "site" {
  min_size            = 1
  max_size            = 2
  desired_capacity    = 1
  target_group_arns   = [aws_lb_target_group.main.arn]
  vpc_zone_identifier = module.network.private_subnets

  launch_template {
    id      = aws_launch_template.tmpl.id
    version = aws_launch_template.tmpl.latest_version // always use the latest available version
  }
}
