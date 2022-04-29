from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import *


User = get_user_model()


admin.site.site_title = "Murojaatlari Boti Admin Paneli"
admin.site.site_header = "Murojaatlari Boti Admin Paneli"


class PhotoStackedInline(admin.StackedInline):
    model = Photo
    readonly_fields = ['get_url']
    fields = ['get_url']
    extra = 0
    can_delete = False

    def get_url(self, obj):
        return format_html("<img src='{}' style='width: 100px; height: 100px;'/>".format(obj.url))
    get_url.allow_tags = True
    get_url.short_description = "Rasm"

    def has_add_permission(self, request, obj):
        return False


class AppealAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'comment']
    fields = ['id', 'get_fullname', 'phone', 'get_phone', 'comment', 'get_google_maps_button']
    readonly_fields = ['id', 'get_fullname', 'phone', 'comment', 'get_google_maps_button', 'get_phone']
    inlines = [PhotoStackedInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(is_submitted=True)
        return queryset
    

    def get_fullname(self, obj):
        try:
            return "{} {}".format(obj.profile.first_name, obj.profile.last_name)
        except:
            return "-"
    get_fullname.allow_tags = True
    get_fullname.short_description = "To'liq ismi"


    def get_phone(self, obj):
        return format_html("<a href='tel:{}' class='btn btn-success btn-sm'><i class='fas fa-phone'></i> Qo'ng'iroq qilish</a>".format(obj.phone))
    get_phone.allow_tags = True
    get_phone.short_description = "Aloqa"


    def get_google_maps_button(self, obj):
        return format_html("<a href='{}' target='_blank' class='btn btn-danger btn-sm'><i class='fas fa-location-crosshairs'></i> Joylashuv</a>".format(obj.google_maps_url))
    get_google_maps_button.allow_tags = True
    get_google_maps_button.short_description = "Havolalar"


    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        return True


admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Appeal, AppealAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)