def test_saglik_gizli_anahtar_olmadan_401(client, settings):
    settings.CRON_SECRET = "s3cr3t"
    assert client.get("/api/saglik/").status_code == 401


def test_saglik_yanlis_anahtar_401(client, settings):
    settings.CRON_SECRET = "s3cr3t"
    r = client.get("/api/saglik/", HTTP_AUTHORIZATION="Bearer yanlis")
    assert r.status_code == 401


def test_saglik_bos_cron_secret_her_zaman_401(client, settings):
    settings.CRON_SECRET = ""
    r = client.get("/api/saglik/", HTTP_AUTHORIZATION="Bearer ")
    assert r.status_code == 401


def test_saglik_dogru_anahtar_200(client, settings, db):
    settings.CRON_SECRET = "s3cr3t"
    r = client.get("/api/saglik/", HTTP_AUTHORIZATION="Bearer s3cr3t")
    assert r.status_code == 200 and r.json()["durum"] == "ok"
