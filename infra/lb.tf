resource "aws_lb" "entrypoint" {
  name                       = "${local.prefix}-lb"
  subnets                    = module.network.public_subnets
  internal                   = false
  load_balancer_type         = "application"
  security_groups            = [aws_security_group.lb.id]
  enable_deletion_protection = false
}

resource "aws_lb_listener" "frontend" {
  load_balancer_arn = aws_lb.entrypoint.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.arn
  }
}

resource "aws_lb_listener" "redirect" {
  // disabled until I have a certificate
  count             = 0
  load_balancer_arn = aws_lb.entrypoint.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "frontend_https" {
  // disabled until I have a certificate
  count             = 0
  load_balancer_arn = aws_lb.entrypoint.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = ""
  certificate_arn   = ""

  default_action {
    type             = "forward"
    target_group_arn = ""
  }
}

resource "aws_lb_target_group" "main" {
  vpc_id   = module.network.vpc_id
  port     = 8000
  protocol = "HTTP"
  tags = {
    Name = "${local.prefix}-tg"
  }
}

resource "aws_security_group" "lb" {
  name   = "${local.prefix}-lb-sg"
  vpc_id = module.network.vpc_id

  // allow connections on 80 and 443
  dynamic "ingress" {
    for_each = toset([80, 443])
    content {
      from_port   = ingress.key
      to_port     = ingress.key
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  // load balancer can only send traffic to the private subnets on port 80
  egress {
    cidr_blocks = module.network.private_subnet_objects[*].cidr_block
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
  }
}
