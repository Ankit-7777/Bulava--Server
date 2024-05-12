from django.utils.deprecation import MiddlewareMixin
from .models import BlacklistedToken
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

class TokenBlacklistMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = self.get_token_from_request(request)
        if token:
            if self.token_is_blacklisted(token):
                return Response({'detail': 'Invalid token'}, status=HTTP_401_UNAUTHORIZED)

    def get_token_from_request(self, request):
        # Extract token from Authorization header or query parameter
        auth_header = request.headers.get('Authorization')
        if auth_header:
            return auth_header.split()[1] if 'Bearer' in auth_header else None
        return None

    def token_is_blacklisted(self, token):
        return BlacklistedToken.objects.filter(token=token).exists()
