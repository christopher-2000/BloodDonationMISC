from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Donor, Initiative, InitiativeImage, OfficeBearer, SiteContent


# Rows are matched on import_id_fields: an existing row with the same value is
# updated, otherwise a new row is created. Rows are validated against the model
# (e.g. blood group choices) and reported in the preview before anything saves.

class DonorResource(resources.ModelResource):
    class Meta:
        model = Donor
        fields = [
            "name", "age", "house_or_shop_name", "blood_group",
            "current_location", "phone", "last_donated", "is_approved",
        ]
        export_order = fields
        import_id_fields = ["phone"]
        clean_model_instances = True


class OfficeBearerResource(resources.ModelResource):
    class Meta:
        model = OfficeBearer
        fields = ["name", "position", "phone", "image_url", "order"]
        export_order = fields
        import_id_fields = ["name"]
        clean_model_instances = True


class InitiativeResource(resources.ModelResource):
    class Meta:
        model = Initiative
        fields = ["title", "description", "link"]
        export_order = fields
        import_id_fields = ["title"]
        clean_model_instances = True


class SiteContentResource(resources.ModelResource):
    class Meta:
        model = SiteContent
        fields = ["key", "label", "value", "group", "is_html"]
        export_order = fields
        import_id_fields = ["key"]
        clean_model_instances = True


MAX_INITIATIVE_IMAGES = 10


class InitiativeImageFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        kept = [
            form
            for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get("DELETE")
        ]
        if len(kept) > MAX_INITIATIVE_IMAGES:
            raise ValidationError(
                f"An initiative can have at most {MAX_INITIATIVE_IMAGES} images."
            )


class InitiativeImageInline(admin.TabularInline):
    model = InitiativeImage
    formset = InitiativeImageFormSet
    extra = 1
    max_num = MAX_INITIATIVE_IMAGES
    fields = ["image", "order"]
    ordering = ["order", "id"]


@admin.register(Donor)
class DonorAdmin(ImportExportModelAdmin):
    resource_classes = [DonorResource]
    list_display = ["name", "age", "blood_group", "current_location", "phone", "last_donated", "is_approved", "created_at"]
    list_editable = ["is_approved"]
    list_filter = ["is_approved", "blood_group", "current_location"]
    search_fields = ["name", "current_location", "phone"]


@admin.register(OfficeBearer)
class OfficeBearerAdmin(ImportExportModelAdmin):
    resource_classes = [OfficeBearerResource]
    list_display = ["name", "position", "phone", "order"]
    list_editable = ["order"]
    search_fields = ["name", "position", "phone"]


@admin.register(Initiative)
class InitiativeAdmin(ImportExportModelAdmin):
    resource_classes = [InitiativeResource]
    inlines = [InitiativeImageInline]
    list_display = ["title", "link", "created_at"]
    search_fields = ["title", "description"]


@admin.register(SiteContent)
class SiteContentAdmin(ImportExportModelAdmin):
    resource_classes = [SiteContentResource]
    list_display = ["label", "key", "group", "is_html", "updated_at"]
    list_filter = ["group", "is_html"]
    search_fields = ["label", "key", "value"]
    list_editable = ["is_html"]
    readonly_fields = ["updated_at"]
    fieldsets = (
        (
            None,
            {
                "fields": ("label", "key", "group", "is_html"),
                "description": (
                    "The key links this text to a spot on the site; change the "
                    "label freely but leave the key alone unless you also update "
                    "the template."
                ),
            },
        ),
        ("Content", {"fields": ("value",)}),
        ("Meta", {"fields": ("updated_at",), "classes": ("collapse",)}),
    )
