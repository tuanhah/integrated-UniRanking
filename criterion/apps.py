from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CriterionConfig(AppConfig):
    name = 'criterion'
    verbose_name = _('Criterion')
    verbose_name_plural = _('Criterions')
    