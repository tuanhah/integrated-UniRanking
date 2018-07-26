from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
    

class UniversityConfig(AppConfig):
    name = 'university'
    verbose_name = _("University")
    verbose_name_plural = _("Universities")
    
    def ready(self):
        import university.signals
