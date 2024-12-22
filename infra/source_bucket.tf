#-------------- CREATE AND UPLOAD
data "archive_file" "source_code" {
  // create an archive of the repo's source code
  type        = "zip"
  source_dir  = "../."
  output_path = "${path.module}/app.zip"
  // exclude unneccessary files to make deployments leaner
  excludes = concat(
    split("\n", file("../.gitignore")),
    [
      ".git",
      "**/*.terraform",
      "**/*.pyc",
      "**/*.db",
      "**/*ignore",
      "**/*_cache",
      ".husky",
      ".github",
      ".envrc",
      "infra",
      "docs",
      "envs",
      "tests",
      "build-containers",
    ]
  )
}

resource "null_resource" "reupload_trigger" {
  triggers = {
    src_hash = "${data.archive_file.source_code.output_sha}"
  }
}

# Upload the archive to S3
resource "aws_s3_object" "app_archive" {
  bucket       = aws_s3_bucket.source_code.id
  key          = "app.zip"
  source       = data.archive_file.source_code.output_path
  content_type = "application/zip"

  lifecycle {
    replace_triggered_by = [null_resource.reupload_trigger]
  }
}

#-------------  CREATE S3 BUCKET FOR SOURCE CODE

resource "aws_s3_bucket" "source_code" {
  bucket_prefix = "${local.prefix}-source-"
  tags = {
    Name = "${local.prefix}-source"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.source_code.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}


