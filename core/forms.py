import re

from django import forms
from django.utils import timezone

from .models import Donor


class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = [
            "name",
            "age",
            "house_or_shop_name",
            "blood_group",
            "current_location",
            "phone",
            "last_donated",
        ]
        widgets = {
            "last_donated": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
            "name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "age": forms.NumberInput(
                attrs={"placeholder": "Enter your age", "min": 18, "max": 65}
            ),
            "house_or_shop_name": forms.TextInput(
                attrs={"placeholder": "House / shop name"}
            ),
            "current_location": forms.TextInput(
                attrs={
                    "placeholder": "Enter your current location (area, city)",
                    "data-location-autocomplete": "full",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "type": "tel",
                    "placeholder": "Enter your mobile number",
                    "data-phone": "1",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The model field's own min of 0 would otherwise override this.
        self.fields["age"].widget.attrs.update({"min": 18, "max": 65})
        # The date picker greys out future days.
        self.fields["last_donated"].widget.attrs["max"] = timezone.localdate().isoformat()

    def clean_last_donated(self):
        last_donated = self.cleaned_data["last_donated"]
        if last_donated and last_donated > timezone.localdate():
            raise forms.ValidationError("Last donated date can't be in the future.")
        return last_donated

    def clean_phone(self):
        """Accept a 10-digit number, optionally with a +country code.

        Returns the number in international form, e.g. +919876543210.
        A bare 10-digit number is assumed to be Indian (+91).
        """
        raw = self.cleaned_data["phone"].strip()
        digits = re.sub(r"\D", "", raw)
        error = forms.ValidationError("Enter a valid 10-digit mobile number.")

        if raw.startswith("+"):
            country_code_length = len(digits) - 10
            if not 1 <= country_code_length <= 3:
                raise error
            return "+" + digits

        if len(digits) != 10:
            raise error
        return "+91" + digits

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age < 18 or age > 65:
            raise forms.ValidationError("Donors must be between 18 and 65 years old.")
        return age
