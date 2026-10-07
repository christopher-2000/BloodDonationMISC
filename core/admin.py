from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Donor, Initiative, OfficeBearer


# Rows are matched on import_id_fields: an existing row with the same value is
# updated, otherwise a new row is created. Rows are validated against the model
# (e.g. blood group choices) and reported in the preview before anything saves.

class DonorResource(resources.ModelResource):
    class Meta:
        model = Donor
        fields = [
            "name", "age", "house_or_shop_name", "blood_group",
            "current_location", "phone", "last_donated",
        ]
        export_order = fields
        import_id_fields = ["phone"]
        clean_model_instances = True


class OfficeBearerResource(resources.ModelResource):
    class Meta:
        model = OfficeBearer
        fields = ["name", "position", "image_url", "order"]
        export_order = fields
        import_id_fields = ["name"]
        clean_model_instances = True


class InitiativeResource(resources.ModelResource):
    class Meta:
        model = Initiative
        fields = ["title", "description", "image_url", "link"]
        export_order = fields
        import_id_fields = ["title"]
        clean_model_instances = True


@admin.register(Donor)
class DonorAdmin(ImportExportModelAdmin):
    resource_classes = [DonorResource]
    list_display = ["name", "age", "blood_group", "current_location", "phone", "last_donated", "created_at"]
    list_filter = ["blood_group", "current_location"]
    search_fields = ["name", "current_location", "phone"]


@admin.register(OfficeBearer)
class OfficeBearerAdmin(ImportExportModelAdmin):
    resource_classes = [OfficeBearerResource]
    list_display = ["name", "position", "order"]
    list_editable = ["order"]
    search_fields = ["name", "position"]


@admin.register(Initiative)
class InitiativeAdmin(ImportExportModelAdmin):
    resource_classes = [InitiativeResource]
    list_display = ["title", "link", "created_at"]
    search_fields = ["title", "description"]
