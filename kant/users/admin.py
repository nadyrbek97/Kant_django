from django.contrib import admin
from .models import UserProfile, DomesticNewsModel, DomesticNewsPhotoLink


admin.site.register(UserProfile)
admin.site.register(DomesticNewsModel)
admin.site.register(DomesticNewsPhotoLink)

admin.site.site_header = "Кант кызылча"
admin.site.site_title = "Каинды Кант"
admin.site.index_title = "Администрация сайта"