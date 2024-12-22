data "aws_region" "current" {}

resource "aws_cloudwatch_dashboard" "dash" {
  dashboard_name = "${local.prefix}-overview"
  dashboard_body = jsonencode({
    widgets = concat(
      local.s3_widgets,
      local.alb_widgets
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
}
