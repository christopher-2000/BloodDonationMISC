from django.db import migrations

# Seed the real Youth League initiatives. Image paths are relative to the
# static folder (core/static) and are served with {% static %} in templates.
INITIATIVES = [
    {
        "title": "Sahayavartha – A Small Act, A Greater Hope",
        "description": (
            "Sahayavartha is a charitable initiative led by MISC Youth League, "
            "Ernakulam, with the aim of supporting those in need. Through this "
            "initiative, old newspapers are collected from church members and sold "
            "to scrap dealers. The funds raised are distributed among underprivileged "
            "and financially struggling individuals and families.\n\n"
            "All church members are requested to bring their old newspapers to the "
            "church during the last week of every month and deposit them in the "
            "designated collection box.\n\n"
            "Through this simple initiative, we turn unused newspapers into meaningful "
            "support for those in need, promoting charity, compassion, and community "
            "responsibility. Together, even a small contribution can make a big "
            "difference in someone's life."
        ),
        "images": ["images/Sahayavartha.jpeg"],
    },
    {
        "title": "Excellence Awards",
        "description": (
            "The MISC Youth League Ernakulam annually organizes an appreciation "
            "programme to encourage and motivate students from our church community "
            "who have successfully completed their SSLC (10th) and Plus Two (12th) "
            "examinations. This initiative recognizes their academic achievements, "
            "celebrates their hard work and dedication, and inspires them to pursue "
            "higher education and achieve greater success in the future. Through this "
            "programme, the Youth League aims to support and motivate young minds to "
            "build a bright future."
        ),
        "images": ["images/Excellence Awards.jpeg"],
    },
    {
        "title": "Medical Camp",
        "description": (
            "Youth League annually organizes a free medical check-up camp at the "
            "church premises for church members and people from the local community "
            "and nearby areas. This initiative aims to promote health awareness, "
            "encourage preventive healthcare, and provide access to basic medical "
            "check-ups for everyone. Through this community service, the Youth League "
            "strives to care for the well-being of people and serve society with "
            "compassion."
        ),
        "images": [
            "images/MedicalCamp1.jpeg",
            "images/medicalCamp2.jpeg",
            "images/MedicalCamp3.jpeg",
        ],
    },
    {
        "title": "Carol Bells",
        "description": (
            "Carol Bells is the annual Christmas celebration organized by the MISC "
            "Youth League Ernakulam, spreading the joy and blessings of Christmas "
            "throughout the church community. The programme begins in the first week "
            "of December, with the carol team visiting the homes of church members "
            "until December 24th. Each visit includes prayers led by the priest and "
            "melodious Christmas carol songs performed by the choir team. The "
            "celebration concludes in December with a vibrant Christmas roadshow "
            "through the church locality, bringing people together in the spirit of "
            "love, peace, unity, and Christmas joy."
        ),
        "images": [
            "images/CarolBells1.jpeg",
            "images/carolBells2.jpeg",
            "images/CarolBells3.jpeg",
        ],
    },
    {
        "title": "Onam Celebration",
        "description": (
            "The Youth League organized a grand Onam celebration at our church on "
            "Atham day. Everyone dressed in traditional Kerala attire to embrace the "
            "spirit of Onam. The celebration included many fun games and exciting "
            "activities, including tug-of-war, making the event joyful, memorable, and "
            "a wonderful opportunity for everyone to come together."
        ),
        "images": ["images/Onam1.jpeg", "images/Onam2.jpeg"],
    },
]


def seed_initiatives(apps, schema_editor):
    Initiative = apps.get_model("core", "Initiative")
    InitiativeImage = apps.get_model("core", "InitiativeImage")

    Initiative.objects.all().delete()
    for item in INITIATIVES:
        initiative = Initiative.objects.create(
            title=item["title"], description=item["description"]
        )
        for order, path in enumerate(item["images"]):
            InitiativeImage.objects.create(
                initiative=initiative, image=path, order=order
            )


def unseed_initiatives(apps, schema_editor):
    Initiative = apps.get_model("core", "Initiative")
    Initiative.objects.filter(
        title__in=[item["title"] for item in INITIATIVES]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_remove_initiative_image_url_initiativeimage"),
    ]

    operations = [
        migrations.RunPython(seed_initiatives, unseed_initiatives),
    ]
