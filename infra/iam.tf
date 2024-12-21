resource "aws_s3_bucket_policy" "main" {
  bucket = aws_s3_bucket.artefacts.id
  policy = data.aws_iam_policy_document.default.json
}


data "aws_iam_policy_document" "default" {
  statement {
    sid = "ArtefactBucketPolicy"

    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]

    resources = [
      "${aws_s3_bucket.artefacts.arn}",
      "${aws_s3_bucket.artefacts.arn}/app.zip"
    ]

    principals {
      type = "AWS"
      identifiers = [
        # Replace this with the instance profile ARN
        # "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/YourInstanceRoleName"
        aws_iam_role.web.arn
      ]
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
  name = "YourInstanceProfile"
  role = aws_iam_role.web.name
}
