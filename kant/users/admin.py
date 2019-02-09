from django.contrib import admin
from .models import UserProfile, DomesticNewsModel, DomesticNewsPhotoLink


app_name = "Пользователи"
# admin.site.register(UserProfile)
admin.site.register(DomesticNewsModel)
admin.site.register(DomesticNewsPhotoLink)


# class DomesticNewsPhotoInline(admin.StackedInline):
#     model = DomesticNewsPhotoLink
#     extra = 0
#
#
# @admin.register(DomesticNewsModel)
# class DomesticAdmin(admin.ModelAdmin):
#     exclude = ('name', 'description', 'content',)
#     inlines = [DomesticNewsPhotoInline, ]


admin.site.site_header = "Кант кызылча"
admin.site.site_title = "Каинды Кант"
admin.site.index_title = "Администрация сайта"