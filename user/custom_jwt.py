from rest_framework_simplejwt.authentication import JWTAuthentication


class AuthorizeHeaderJWTAuthentication(JWTAuthentication):
    def get_authorization_header(self, request):
        return request.META.get("HTTP_AUTHORIZE", b"")
