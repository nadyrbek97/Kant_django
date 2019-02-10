from django.contrib import admin
from .models import UserProfile, DomesticNewsModel, DomesticNewsPhotoLink
from django.contrib.auth.models import Group

# admin.site.register(UserProfile)
# admin.site.unregister(Group)
# admin.site.register(DomesticNewsModel)
# admin.site.register(DomesticNewsPhotoLink)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'city',)


class DomesticNewsPhotoInline(admin.StackedInline):
    model = DomesticNewsPhotoLink
    extra = 0


@admin.register(DomesticNewsModel)
class DomesticAdmin(admin.ModelAdmin):
    # exclude = ('name', 'description', 'content',)
    inlines = [DomesticNewsPhotoInline, ]


admin.site.site_header = "Кант кызылча"
admin.site.site_title = "Каинды Кант"
admin.site.index_title = "Администрация сайта"