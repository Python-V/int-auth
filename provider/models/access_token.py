from django.apps import apps
from django.core.cache import cache
from django.db import models
from django.utils import timezone

from main.settings import auth_settings


class AccessToken(models.Model):
    """
    An AccessToken instance represents the actual access token to
    access user's resources, as in :rfc:`5`.
    Fields:
    * :attr:`user` The Django user representing resources" owner
    * :attr:`source_refresh_token` If from a refresh, the consumed RefeshToken
    * :attr:`token` Access token
    * :attr:`application` Application instance
    * :attr: `invalid` To check if this token can still be used or not
    * :attr:`expires` Date and time of token expiration, in DateTime format
    * :attr:`scope` Allowed scopes
    """

    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    source_refresh_token = models.OneToOneField(
        # unique=True implied by the OneToOneField
        auth_settings.REFRESH_TOKEN_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="refreshed_access_token",
    )
    token = models.CharField(
        max_length=255,
        unique=True,
    )
    id_token = models.OneToOneField(
        auth_settings.ID_TOKEN_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="access_token",
    )
    application = models.ForeignKey(
        auth_settings.APPLICATION_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    expires = models.DateTimeField()
    invalid = models.BooleanField(default=False)
    scope = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_valid(self, scopes=None):
        """
        Checks if the access token is valid.
        :param scopes: An iterable containing the scopes to check or None
        """
        return not self.is_expired() and self.allow_scopes(scopes)

    def allow_scopes(self, scopes):
        """
        Check if the token allows the provided scopes
        :param scopes: An iterable containing the scopes to check
        """
        if not scopes:
            return True

        provided_scopes = set(self.scope.split())
        resource_scopes = set(scopes)

        return resource_scopes.issubset(provided_scopes)

    def is_expired(self):
        """
        Check token expiration with timezone awareness
        """
        if not self.expires:
            return True

        return timezone.now() >= self.expires

    def revoke(self):
        """
        Convenience method to uniform tokens" interface, for now
        simply remove this token from the database in order to revoke it.
        """
        self.delete()

    def __str__(self):
        return self.token

    def delete(self):
        """
        Delete cache entry for the token
        """
        if self.token in cache:
            cache.delete(self.token)
        super(AccessToken, self).delete()


def get_access_token_model():
    """Return the AccessToken model that is active in this project."""
    return apps.get_model(auth_settings.ACCESS_TOKEN_MODEL)
