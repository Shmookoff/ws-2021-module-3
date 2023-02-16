from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions

from user.models import Token


class BearerAuthentication(authentication.TokenAuthentication):
    keyword = "Bearer"
    model = Token

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related("user").get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))
        token.user.is_authenticated = True
        return (token.user, token)
