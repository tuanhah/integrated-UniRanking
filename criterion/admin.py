from django.contrib import admin

from .models import CriterionCategory, Criterion

@admin.register(CriterionCategory)
class CriterionCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'university_only')

@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category', 'university_only')
