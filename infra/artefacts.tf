resource "aws_s3_bucket" "artefacts" {
  bucket = "${local.prefix}-artefacts"
}

resource "aws_s3_bucket_ownership_controls" "artefacts" {
  bucket = aws_s3_bucket.artefacts.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "artefacts" {
  bucket = aws_s3_bucket.artefacts.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "artefacts" {
  depends_on = [
    aws_s3_bucket_ownership_controls.artefacts,
    aws_s3_bucket_public_access_block.artefacts,
  ]

  bucket = aws_s3_bucket.artefacts.id
  acl    = "public-read"
}
