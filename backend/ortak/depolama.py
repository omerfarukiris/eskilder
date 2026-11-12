from urllib.parse import urlparse

YEREL = {"BACKEND": "django.core.files.storage.FileSystemStorage"}
STATIK = {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}


def storages_ayari(ortam) -> dict:
    """SUPABASE_S3_ENDPOINT tanımlıysa Supabase Storage (S3 uyumlu), değilse yerel dosya sistemi."""
    if not ortam.get("SUPABASE_S3_ENDPOINT"):
        return {"default": YEREL, "staticfiles": STATIK}
    host = urlparse(ortam["SUPABASE_PUBLIC_URL"]).netloc
    bucket = ortam["SUPABASE_BUCKET"]
    return {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "bucket_name": bucket,
                "endpoint_url": ortam["SUPABASE_S3_ENDPOINT"],
                "region_name": ortam.get("SUPABASE_S3_REGION", ""),
                "access_key": ortam["SUPABASE_S3_ACCESS_KEY"],
                "secret_key": ortam["SUPABASE_S3_SECRET_KEY"],
                "custom_domain": f"{host}/storage/v1/object/public/{bucket}",
                "url_protocol": "https:",
                "querystring_auth": False,
                "file_overwrite": False,
                "default_acl": None,
            },
        },
        "staticfiles": STATIK,
    }
