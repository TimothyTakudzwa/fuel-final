from django.apps import AppConfig


class BuyerConfig(AppConfig):
    name = 'buyer'

    def ready(self):
        import buyer.signals
