from rest_framework.authtoken.models import Token

from rest_framework.exceptions import AuthenticationFailed
import json

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Check for token in headers (Authorization)
        authorization_header = request.headers.get('Authorization')
        token_key = None

        if authorization_header:
            auth_parts = authorization_header.split()
            if len(auth_parts) == 2 and auth_parts[0].lower() == 'bearer':
                token_key = auth_parts[1]

        # 2. If token not found in headers, check for token in cookies
        if not token_key:
            token_key = request.COOKIES.get('token')

        # 3. If token not found in cookies, check for token in query parameters
        if not token_key:
            token_key = request.GET.get('token')

        # 4. If token not found in query parameters, check for token in request body
        if not token_key and request.body:
            try:
                body_data = json.loads(request.body)
                token_key = body_data.get('token')
            except json.JSONDecodeError:
                pass

        # Authenticate user using the retrieved token key
        if token_key:
            try:
                token = Token.objects.get(key=token_key)
                request.user = token.user
            except Token.DoesNotExist:
                raise AuthenticationFailed('Invalid token')
        else:
            raise AuthenticationFailed('Token not provided')

        # Call the next middleware or view function
        response = self.get_response(request)

        return response
