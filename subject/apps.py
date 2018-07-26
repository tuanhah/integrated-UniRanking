from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SubjectConfig(AppConfig):
    name = 'subject'
    verbose_name = _('Subject')
    verbose_name_plural = _('Subjects')
    
    def ready(self):
        import subject.signals
