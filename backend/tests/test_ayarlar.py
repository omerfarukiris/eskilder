import importlib
import os
from unittest import mock


def test_joker_alan_adi_csrf_kaynagi():
    with mock.patch.dict(os.environ, {"ALLOWED_HOSTS": ".vercel.app,eskilder.org.tr"}):
        import config.settings as ayar

        importlib.reload(ayar)
        assert ayar.CSRF_TRUSTED_ORIGINS == ["https://*.vercel.app", "https://eskilder.org.tr"]
    importlib.reload(ayar)
