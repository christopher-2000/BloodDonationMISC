from django.db import migrations

BEARER = {
    "name": "Jane Doe",
    "position": "Blood Coordinator",
    "phone": "432432-23423",
    "image_url": "",
    "order": 4,
}


def add_bearer(apps, schema_editor):
    OfficeBearer = apps.get_model("core", "OfficeBearer")
    OfficeBearer.objects.get_or_create(name=BEARER["name"], defaults=BEARER)


def remove_bearer(apps, schema_editor):
    OfficeBearer = apps.get_model("core", "OfficeBearer")
    OfficeBearer.objects.filter(name=BEARER["name"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_office_bearers"),
    ]

    operations = [
        migrations.RunPython(add_bearer, remove_bearer),
    ]
