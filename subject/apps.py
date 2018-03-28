from django.apps import AppConfig


class SubjectConfig(AppConfig):
    name = 'subject'

    def ready(self):
        import subject.signals
