#------------- ASG Resources

resource "aws_launch_template" "tmpl" {

}

resource "aws_autoscaling_group" "site" {
  min_size          = 1
  max_size          = 2
  desired_capacity  = 1
  target_group_arns = [aws_lb_target_group.main.arn]

  launch_template {

  }
}
