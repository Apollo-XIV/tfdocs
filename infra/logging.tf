
module "log_bucket" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket = "${local.prefix}-logs"
  acl    = "log-delivery-write"

  control_object_ownership       = true
  object_ownership               = "ObjectWriter"
  attach_elb_log_delivery_policy = true
}
