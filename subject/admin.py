from django.contrib import admin

from .models import Sector, UniversitySector
from .forms import SectorForm, UniversitySectorForm

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
	form = SectorForm
	list_display = ('id', 'name')

@admin.register(UniversitySector)
class UniversitySectorAdmin(admin.ModelAdmin):
	form = UniversitySectorForm
	list_display = ('id', 'university', 'sector')