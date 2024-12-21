import boto3

s3 = boto3.client('s3')

bucket_name = "tfdocs-dev-release-bucket"
bucket_url = f"https://{bucket_name}.s3.amazonaws.com"


def list_available_releases() -> list[str]:
    """Lists all available releases in the artefact storage bucket"""
    all_folders = s3.list_objects_v2(
        Bucket=bucket_name,
    )
    # sort them
    return all_folders


def get_download_link(version_number) -> str:
    return f"{bucket_url}/{version_number}/tfdocs.AppImage"
