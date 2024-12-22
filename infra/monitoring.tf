data "aws_region" "current" {}

resource "aws_cloudwatch_dashboard" "dash" {
  dashboard_name = "${local.prefix}-overview"
  dashboard_body = jsonencode({
    widgets = concat(
      local.s3_widgets,
      local.alb_widgets,
      local.asg_widgets
    )
  })
}

locals {
  s3_widgets = [
    {
      type   = "metric"
      x      = 0
      y      = 0
      width  = 6
      height = 6
      properties = {
        metrics = [[
          "AWS/S3",
          "BucketSizeBytes",
          "BucketName",
          aws_s3_bucket.artefacts.bucket,
          "StorageType",
          "StandardStorage"
        ]]
        title  = "Artefact Bucket Size"
        period = 86400
        region = data.aws_region.current.name
        stat   = "Average"
      }
    },
    {
      type   = "metric"
      x      = 6
      y      = 0
      width  = 6
      height = 6
      properties = {
        metrics = [[
          "AWS/S3",
          "NumberOfObjects",
          "BucketName",
          aws_s3_bucket.artefacts.bucket,
          "StorageType",
          "AllStorageTypes"
        ]]
        title  = "Number of Objects in S3"
        period = 86400
        region = data.aws_region.current.name
        stat   = "Sum"
      }
    }
  ]

  alb_widgets = [
    {
      type   = "metric"
      x      = 0
      y      = 6
      width  = 6
      height = 6
      properties = {
        metrics = [[
          "AWS/ApplicationELB",
          "RequestCount",
          "LoadBalancer",
          aws_lb.entrypoint.id
        ]]
        title  = "LB Request Count"
        period = 60
        region = data.aws_region.current.name
        stat   = "Sum"
      }
    },
    {
      type   = "metric"
      x      = 6
      y      = 6
      width  = 6
      height = 6
      properties = {
        metrics = [[
          "AWS/ApplicationELB",
          "TargetResponseTime",
          "LoadBalancer",
          aws_lb.entrypoint.id
        ]]
        title  = "LB Response Time"
        period = 60
        region = data.aws_region.current.name
        stat   = "Average"
      }
    }
  ]

  asg_widgets = [
    {
      type   = "metric"
      x      = 0
      y      = 12
      width  = 6
      height = 6
      properties = {
        metrics = [[
          "AWS/AutoScaling",
          "GroupDesiredCapacity",
          "AutoScalingGroupName",
          aws_autoscaling_group.site.name
        ]]
        title  = "ASG Desired Capacity"
        period = 300
        region = data.aws_region.current.name
        stat   = "Average"
      }
    },
    {
      type   = "metric"
      x      = 6
      y      = 12
      width  = 6
      height = 6
      properties = {
        metrics = [[
          "AWS/EC2",
          "CPUUtilization",
          "AutoScalingGroupName",
          aws_autoscaling_group.site.name
        ]]
        title   = "ASG CPU Utilisation"
        period  = 300
        stacked = false
        stat    = "Average"
        view    = "timeSeries"
        region  = data.aws_region.current.name
      }
    }
  ]
}
