from django.contrib import admin

# Register your models here.
from accounts.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_info', 'city', 'phone')

    def user_info(self, obj):
        return obj.position

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-phone')
        return queryset

    user_info.short_description = 'Информация'


admin.site.register(UserProfile, UserProfileAdmin)
