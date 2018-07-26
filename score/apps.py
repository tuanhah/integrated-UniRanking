from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ScoreConfig(AppConfig):
    name = 'score'
    verbose_name = _('Score')
    