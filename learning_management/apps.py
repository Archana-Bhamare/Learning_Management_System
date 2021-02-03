from django.apps import AppConfig


class LearnManagementConfig(AppConfig):
    name = 'learning_management'

    def ready(self):
        import learning_management.signals