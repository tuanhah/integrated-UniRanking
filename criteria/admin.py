from django.contrib import admin
from .models import CategoryCriterion, Criterion

admin.site.register(CategoryCriterion)

@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
    list_display = ('id','name','description','category')