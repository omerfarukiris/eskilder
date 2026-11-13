import importlib
import os
from unittest import mock


def test_joker_alan_adi_csrf_kaynagi():
    with mock.patch.dict(os.environ, {"ALLOWED_HOSTS": ".vercel.app,eskilder.org.tr"}):
        import config.settings as ayar

        importlib.reload(ayar)
        assert ayar.CSRF_TRUSTED_ORIGINS == ["https://*.vercel.app", "https://eskilder.org.tr"]
    importlib.reload(ayar)


def test_postgres_secenekleri_yalniz_postgreste():
    with mock.patch.dict(os.environ, {"DATABASE_URL": "sqlite:////tmp/x.db"}):
        import config.settings as ayar

        importlib.reload(ayar)
        assert "prepare_threshold" not in ayar.DATABASES["default"].get("OPTIONS", {})
    with mock.patch.dict(os.environ, {"DATABASE_URL": "postgresql://u:p@h:6543/postgres"}):
        importlib.reload(ayar)
        assert ayar.DATABASES["default"]["OPTIONS"]["prepare_threshold"] is None
        assert ayar.DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] is True
    importlib.reload(ayar)
