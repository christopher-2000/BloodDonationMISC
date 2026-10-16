from django.db import migrations

# Final image set for the initiatives (imgbb direct links, verified by pixel
# match against the local originals in core/static/images).
INITIATIVE_IMAGES = {
    "Sahayavartha – A Small Act, A Greater Hope": [
        "https://i.ibb.co/NHQYXHS/Sahayavartha.jpg",
    ],
    "Excellence Awards": [
        "https://i.ibb.co/JR19cHgM/Excellence-Awards.jpg",
    ],
    "Medical Camp": [
        "https://i.ibb.co/Kcn12sQS/Medical-Camp1.jpg",
        "https://i.ibb.co/Q7SKrY7w/medical-Camp2.jpg",
        "https://i.ibb.co/bRMzDbgm/Medical-Camp3.jpg",
    ],
    "Carol Bells": [
        "https://i.ibb.co/SDD0FvJr/Carol-Bells1.jpg",
        "https://i.ibb.co/W4m0zWwV/carol-Bells2.jpg",
        "https://i.ibb.co/WNcg2t6Z/Carol-Bells3.jpg",
    ],
    "Onam Celebration": [
        "https://i.ibb.co/fGXgn3SF/Onam1.jpg",
        "https://i.ibb.co/pBxtmW6L/Onam2.jpg",
    ],
}


def apply_imgbb_images(apps, schema_editor):
    Initiative = apps.get_model("core", "Initiative")
    InitiativeImage = apps.get_model("core", "InitiativeImage")
    for title, urls in INITIATIVE_IMAGES.items():
        try:
            initiative = Initiative.objects.get(title=title)
        except Initiative.DoesNotExist:
            continue
        initiative.images.all().delete()
        for order, url in enumerate(urls):
            InitiativeImage.objects.create(
                initiative=initiative, image=url, order=order
            )


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_update_initiative_images_drive"),
    ]

    operations = [
        migrations.RunPython(apply_imgbb_images, reverse),
    ]
