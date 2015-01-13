from django.utils.translation import ugettext_lazy as _

from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Role, User
from .forms import UserChangeForm, UserCreationForm


#admin.site.unregister(Group)


class RoleAdmin(admin.ModelAdmin):
    list_display = ["name"]
    filter_horizontal = ('permissions',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.rel.to.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super().formfield_for_manytomany(
            db_field, request=request, **kwargs)


class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        (_('Personal info'), {'fields': ('full_name', 'email', 'bio', 'photo')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'gender', 'birthday', 'country', 'groups',)}
         ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'full_name')
    list_filter = ('is_superuser', 'is_active')
    search_fields = ('username', 'full_name', 'email')
    ordering = ('username',)
    filter_horizontal = ()


class RoleInline(admin.TabularInline):
    model = Role
    extra = 0


admin.site.register(User, UserAdmin)
# admin.site.register(Role, RoleAdmin)