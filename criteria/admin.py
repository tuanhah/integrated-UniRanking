from django.contrib import admin

from .models import CriterionCategory, Criterion

admin.site.register(CriterionCategory)

@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
    list_display = ('id','name','description','category')

class ScoreAdmin(admin.ModelAdmin):
    pass