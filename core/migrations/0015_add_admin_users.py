from django.conf import settings
from django.db import migrations

# Three extra staff/superuser accounts. Passwords are stored here as hashes
# (PBKDF2, Django's default) so the raw password never lives in the repo.
ADMINS = [
    (
        "admin3",
        "pbkdf2_sha256$1000000$TOsk49NueHtZ4i3hD6Uf4d$P/ftxdDWfhyVTd5n1N5gRb11iOqelowrn1kDdlkvQJE=",
    ),
    (
        "admin4",
        "pbkdf2_sha256$1000000$biTIAocxKOXo0ez9DDkTKP$ureUD6BbzvCxzP3HDBp1jGFFDXdazyi24ZV2BC3K31M=",
    ),
    (
        "admin5",
        "pbkdf2_sha256$1000000$jgVE25ah70GyuTAIeQM7dg$niu+hIUUQzdAUffqOcua7c15owFnw2vglyuxIHjuM0Q=",
    ),
]


def add_admins(apps, schema_editor):
    User = apps.get_model("auth", "User")
    for username, password in ADMINS:
        User.objects.update_or_create(
            username=username,
            defaults={
                "password": password,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )


def remove_admins(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username__in=[name for name, _ in ADMINS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0014_seed_site_content"),
    ]

    operations = [
        migrations.RunPython(add_admins, remove_admins),
    ]
