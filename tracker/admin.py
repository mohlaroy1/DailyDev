from django.contrib import admin
from .models import Technology, CodingSession 

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name", "category")
    list_filter = ("category",)



@admin.register(CodingSession)
class CodingSessionAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "date", "duration_minutes", "created_at",)
    list_filter = ("date", "technologies")
    search_fields = ("title", "description", "user__username",)
    filter_horizontal = ("technologies",)
    ordering = ("-date", "-created_at")
