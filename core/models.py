from django.db import models


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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.blood_group})"


class OfficeBearer(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"{self.name} ({self.position})"


class Initiative(models.Model):
    image_url = models.URLField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.title
