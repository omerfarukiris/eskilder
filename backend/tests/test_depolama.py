from ortak.depolama import storages_ayari


def test_ortam_yoksa_yerel_depolama():
    ayar = storages_ayari({})
    assert ayar["default"]["BACKEND"] == "django.core.files.storage.FileSystemStorage"


def test_s3_url_supabase_public_yolu():
    from storages.backends.s3 import S3Storage

    ayar = storages_ayari({
        "SUPABASE_S3_ENDPOINT": "https://abc.supabase.co/storage/v1/s3",
        "SUPABASE_S3_REGION": "eu-central-1",
        "SUPABASE_S3_ACCESS_KEY": "a",
        "SUPABASE_S3_SECRET_KEY": "b",
        "SUPABASE_PUBLIC_URL": "https://abc.supabase.co",
        "SUPABASE_BUCKET": "medya",
    })
    depo = S3Storage(**ayar["default"]["OPTIONS"])
    assert depo.url("a.jpg") == "https://abc.supabase.co/storage/v1/object/public/medya/a.jpg"
    assert ayar["default"]["OPTIONS"]["querystring_auth"] is False
