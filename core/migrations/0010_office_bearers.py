from django.db import migrations

# Real office bearers with their photos (imgbb direct links).
BEARERS = [
    {
        "name": "Fr Schariah Cheeran",
        "position": "President",
        "image_url": "https://i.ibb.co/tTL00x7J/Father.jpg",
        "order": 0,
    },
    {
        "name": "Aenosh Santhosh",
        "position": "Secretary",
        "image_url": "https://i.ibb.co/fd3Y4s56/Aenosh.jpg",
        "order": 1,
    },
    {
        "name": "Aleena Joby",
        "position": "Joint Trustees",
        "image_url": "https://i.ibb.co/j9qRSXSC/Anna.jpg",
        "order": 2,
    },
    {
        "name": "Estina Subin",
        "position": "Joint Trustees",
        "image_url": "https://i.ibb.co/fzP35KtJ/Estina.jpg",
        "order": 3,
    },
]


def seed_bearers(apps, schema_editor):
    OfficeBearer = apps.get_model("core", "OfficeBearer")
    OfficeBearer.objects.all().delete()
    for item in BEARERS:
        OfficeBearer.objects.create(**item)


def unseed_bearers(apps, schema_editor):
    OfficeBearer = apps.get_model("core", "OfficeBearer")
    OfficeBearer.objects.filter(
        name__in=[item["name"] for item in BEARERS]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_initiative_images_imgbb"),
    ]

    operations = [
        migrations.RunPython(seed_bearers, unseed_bearers),
    ]
