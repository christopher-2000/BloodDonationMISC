from django.db import models
from django.templatetags.static import static


def image_url(path):
    """Resolve an image reference to a usable URL.

    Absolute URLs (e.g. Google Drive links) are returned unchanged; anything
    else is treated as a path inside the static folder.
    """
    if not path:
        return ""
    if path.startswith(("http://", "https://", "//", "/")):
        return path
    return static(path)



class Donor(models.Model):
    BLOOD_GROUPS = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("O+", "O+"), ("O-", "O-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
    ]

    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    house_or_shop_name = models.CharField(max_length=200)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    current_location = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    last_donated = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(
        default=True,
        verbose_name="Approved",
        help_text=(
            "Uncheck to reject this donor. Rejected donors are hidden from "
            "public search and stats."
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.blood_group})"


class OfficeBearer(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"{self.name} ({self.position})"


class Initiative(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.title

    @property
    def cover(self):
        """First image as a ready-to-use URL, used as the card thumbnail."""
        first = self.images.first()
        return image_url(first.image if first else "")


class InitiativeImage(models.Model):
    initiative = models.ForeignKey(
        Initiative, related_name="images", on_delete=models.CASCADE
    )
    # Path relative to the static folder, e.g. "images/MedicalCamp1.jpeg"
    image = models.CharField(max_length=300)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.image


class SiteContent(models.Model):
    """Editable page text, keyed so templates can look it up with a fallback."""

    key = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Stable identifier used inside templates, e.g. home_hero_title.",
    )
    label = models.CharField(
        max_length=150, help_text="Friendly name shown in the admin list."
    )
    value = models.TextField(blank=True)
    group = models.CharField(
        max_length=60,
        blank=True,
        help_text="Optional grouping, e.g. Home, About, Footer.",
    )
    is_html = models.BooleanField(
        default=False,
        help_text="Tick when the value contains safe HTML (e.g. a <span> in a heading).",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["group", "label"]
        verbose_name = "site text"
        verbose_name_plural = "site texts"

    def __str__(self):
        return self.label

