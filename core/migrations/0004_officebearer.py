from django.db import migrations, models


def add_default_bearers(apps, schema_editor):
    OfficeBearer = apps.get_model("core", "OfficeBearer")
    for order, (name, position) in enumerate(
        [
            ("Abin Thomas", "President"),
            ("Jithin Mathew", "Secretary"),
            ("Anna Mariya", "Treasurer"),
            ("Rohit Varghese", "Joint Secretary"),
        ]
    ):
        OfficeBearer.objects.create(name=name, position=position, order=order)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_initiative"),
    ]

    operations = [
        migrations.CreateModel(
            name="OfficeBearer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("position", models.CharField(max_length=100)),
                ("image_url", models.URLField(blank=True, max_length=500)),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["order", "created_at"],
            },
        ),
        migrations.RunPython(add_default_bearers, migrations.RunPython.noop),
    ]
