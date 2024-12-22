import boto3

s3 = boto3.client("s3")

bucket_name = "tfdocs-dev-artefacts"
bucket_url = f"https://{bucket_name}.s3.amazonaws.com"


def list_available_releases() -> list[str]:
    """Lists all available releases in the artefact storage bucket"""
    all_objs = s3.list_objects_v2(
        Bucket=bucket_name,
    )["Contents"]

    filtered = [
        object["Key"].split("/")[0] for object in all_objs if "/" in object["Key"]
    ]

    # sort them
    return filtered


def get_download_link(version_number) -> str:
    return f"{bucket_url}/{version_number}/tfdocs.AppImage"
