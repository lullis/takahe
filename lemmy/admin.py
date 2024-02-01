from django.contrib import admin

from . import models


@admin.register(models.Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = ("domain", "local", "blocked", "public", "software")
    list_filter = ("local", "blocked")


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("id", "domain", "local")
    list_filter = ("local",)


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "domain", "local")
    list_filter = ("local",)
