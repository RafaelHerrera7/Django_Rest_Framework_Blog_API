from rest_framework import permissions
from django.conf import settings


class HasValidAPIKey(permissions.BasePermission):
    '''
    Custom permissions to check if a valid API key it provided in the request
    '''
    
    def has_permission(self, request, view):
        api_key = str(request.headers.get('API-Key'))
        return api_key in getattr(settings, 'VALID_API_KEYS', [])