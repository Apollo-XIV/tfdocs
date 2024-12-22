resource "aws_s3_bucket_policy" "main" {
  bucket = aws_s3_bucket.source_code.id
  policy = data.aws_iam_policy_document.default.json
}


data "aws_iam_policy_document" "default" {
  statement {
    sid = "SourceCodeBucketPolicy"

    actions = [
      "s3:GetObject",
      "s3:ListBucket"
    ]

    resources = [
      "${aws_s3_bucket.source_code.arn}",  # Bucket ARN for ListBucket
      "${aws_s3_bucket.source_code.arn}/*" # Object ARNs for GetObject
    ]

    principals {
      type        = "AWS"
      identifiers = ["${aws_iam_role.web.arn}"]
    }
  }
}
#---------- ASG IAM MATERIALS
resource "aws_iam_role" "web" {
  name = "${local.prefix}-web-role"

  assume_role_policy = data.aws_iam_policy_document.instance_assume_role.json
}

data "aws_iam_policy_document" "instance_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_instance_profile" "web" {
  name = "${local.prefix}-web-profile"
  role = aws_iam_role.web.name
}
