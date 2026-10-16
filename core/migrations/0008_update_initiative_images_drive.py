from django.db import migrations

DRIVE_IMAGES = {
    "Sahayavartha – A Small Act, A Greater Hope": [
        "https://drive.google.com/uc?export=view&id=1ekGWrAf9iq5kLEGifAfVL_4owcomiu3W",
    ],
    "Excellence Awards": [
        "https://drive.google.com/uc?export=view&id=1drJslwdXoaI3f1m2zoimmqW_LzAvZyRQ",
    ],
    "Medical Camp": [
        "https://drive.google.com/uc?export=view&id=1ogl7asUKdMlb3YZ26Bwt-qilZzQlUPz6",
        "https://drive.google.com/uc?export=view&id=1SBDZkeRCSkx1Wm8WByK7o6CZ-SRd9_Xg",
        "https://drive.google.com/uc?export=view&id=1m7vH0uPIgoYzkzD8kzIBlvxxHAA8Fc_4",
    ],
    "Carol Bells": [
        "https://drive.google.com/uc?export=view&id=1qHz1WnvJPY4o-R7Q7-N-RPr6jMxVwrGs",
        "https://drive.google.com/uc?export=view&id=1lV70MjIM7OL45HrzHyv3JHikRfa_IWfy",
        "https://drive.google.com/uc?export=view&id=1Jf7toxVzPT2RvFFyFfWd4vygTfLOFEVP",
    ],
    "Onam Celebration": [
        "https://drive.google.com/uc?export=view&id=1NNorlK5g6n0qMRcaZQ3u71QQ_cRrb71C",
        "https://drive.google.com/uc?export=view&id=1isuW-4eq4xREowz9_naqspaP_dUkBWVP",
    ],
}


def apply_drive_images(apps, schema_editor):
    Initiative = apps.get_model("core", "Initiative")
    InitiativeImage = apps.get_model("core", "InitiativeImage")
    for title, urls in DRIVE_IMAGES.items():
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
        ("core", "0007_officebearer_phone"),
    ]

    operations = [
        migrations.RunPython(apply_drive_images, reverse),
    ]
