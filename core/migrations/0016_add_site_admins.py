from django.conf import settings
from django.db import migrations

# Two extra site-admin accounts (can sign in on the website's /login/ page and
# manage donor registrations, but have NO access to the Django admin portal).
# Passwords are stored as PBKDF2 hashes so the raw password never lives in the
# repo.
SITE_ADMINS = [
    (
        "siteadmin2",
        "pbkdf2_sha256$1000000$Cj19kPJ0c6zJsgwxnUOgCo$hcZU+fuUwn/IwwzqGy7yB8UFzpAe2pOjzkGhpuxs0F8=",
    ),
    (
        "siteadmin3",
        "pbkdf2_sha256$1000000$R6wi1aOFkWXK9xBepW07tn$OF39jL6BH8X3ne5ftCrEHD/ZEf2jok7K4QdcgWfg44I=",
    ),
]


def add_site_admins(apps, schema_editor):
    User = apps.get_model("auth", "User")
    for username, password in SITE_ADMINS:
        User.objects.update_or_create(
            username=username,
            defaults={
                "password": password,
                "is_staff": False,
                "is_superuser": False,
                "is_active": True,
            },
        )


def remove_site_admins(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username__in=[name for name, _ in SITE_ADMINS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0015_add_admin_users"),
    ]

    operations = [
        migrations.RunPython(add_site_admins, remove_site_admins),
    ]
