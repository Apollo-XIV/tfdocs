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

data "aws_ami" "ubuntu_latest" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  owners = ["099720109477"] # Canonical's account ID for EU regions
}

resource "aws_launch_template" "tmpl" {
  name_prefix   = "${local.prefix}-lt"
  instance_type = "t2.micro"
  image_id      = data.aws_ami.ubuntu_latest.id

  update_default_version = true
  user_data              = data.cloudinit_config.base.rendered

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

  network_interfaces {
    security_groups = [
      aws_security_group.site.id
    ]
    associate_public_ip_address = false
  }
}


data "cloudinit_config" "base" {
  gzip          = false
  base64_encode = true

  part {
    content_type = "text/cloud-config"
    content = yamlencode({
      packages = [
        "awscli",
        "unzip"
      ]
    })
  }

  part {
    content_type = "text/x-shellscript"
    content      = <<-EOF
      #!/usr/bin/bash
      
      useradd -m -s /bin/bash webuser
      # install nix
      curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix \
      | sh -s -- \
      install \
      --no-confirm

      # source the init daemon for nix
      . /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh

      mkdir -p /var/www/tfdocs
      aws s3 cp s3://${aws_s3_bucket.source_code.bucket}/${aws_s3_object.app_archive.key} .
      unzip -d /var/www/tfdocs app.zip
      chown -R webuser:webuser /var/www/tfdocs

      cd /var/www/tfdocs
      nix develop .#web
      # Start the webserver on :8000
      sudo -u webuser nohup gunicorn -w 4 web:app &
    EOF
  }
}


resource "aws_autoscaling_group" "site" {
  name                = "${local.prefix}-asg"
  min_size            = 0
  max_size            = 2
  desired_capacity    = var.node_count
  target_group_arns   = [aws_lb_target_group.main.arn]
  vpc_zone_identifier = module.network.private_subnets

  launch_template {
    id      = aws_launch_template.tmpl.id
    version = aws_launch_template.tmpl.latest_version // always use the latest available version
  }

  instance_refresh {
    strategy = "Rolling"
  }

}

resource "aws_security_group" "site" {
  name   = "${local.prefix}-site-sg"
  vpc_id = module.network.vpc_id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 1024
    to_port   = 65535
    protocol  = "tcp"
    security_groups = [
      aws_security_group.lb.id
    ]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
