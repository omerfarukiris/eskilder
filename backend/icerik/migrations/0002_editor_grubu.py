from django.contrib.auth.management import create_permissions
from django.db import migrations

ICERIK_MODELLERI = ["siteayarlari", "etkirakami", "duyuru", "duyurufotografi", "etkinlik", "etkinlikfotografi",
                    "destekci", "yonetimkuruluuyesi", "dokuman"]


def grup_olustur(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    grup, _ = Group.objects.get_or_create(name="Editör")
    izinler = Permission.objects.filter(content_type__app_label="icerik", content_type__model__in=ICERIK_MODELLERI)
    izinler = izinler | Permission.objects.filter(content_type__app_label="iletisim", content_type__model="iletisimmesaji")
    grup.permissions.set(izinler)


def grup_sil(apps, schema_editor):
    apps.get_model("auth", "Group").objects.filter(name="Editör").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("icerik", "0001_baslangic"),
        ("iletisim", "0001_baslangic"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]
    operations = [migrations.RunPython(grup_olustur, grup_sil)]
