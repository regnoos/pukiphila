from django.contrib import admin

from soonger.users.admin import RoleInline
from . import models


class MembershipAdmin(admin.ModelAdmin):
    list_display = ['album', 'role', 'user']
    list_display_links = list_display
    list_filter = ['album', 'role']


class MembershipInline(admin.TabularInline):
    model = models.Membership
    extra = 0


class AlbumAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "created_date"]
    list_display_links = list_display
    inlines = [RoleInline, MembershipInline]

    def get_object(self, *args, **kwargs):
        self.obj = super().get_object(*args, **kwargs)
        return self.obj

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (db_field.name in ["default_points", "default_us_status", "default_task_status",
                              "default_priority", "default_severity",
                              "default_issue_status", "default_issue_type"]):
            if getattr(self, 'obj', None):
                kwargs["queryset"] = db_field.related.parent_model.objects.filter(album=self.obj)
            else:
                kwargs["queryset"] = db_field.related.parent_model.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if (db_field.name in ["watchers"]
                and getattr(self, 'obj', None)):
            kwargs["queryset"] = db_field.related.parent_model.objects.filter(memberships__album=self.obj)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(models.Album, AlbumAdmin)
admin.site.register(models.Membership, MembershipAdmin)
