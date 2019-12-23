from django.dispatch import Signal


email_confirmed = Signal(providing_args=["email_address"])
