from rest_framework import HTTP_HEADER_ENCODING
from rest_framework_simplejwt.authentication import JWTAuthentication


class AuthorizeHeaderJWTAuthentication(JWTAuthentication):
    def get_header(self, request):
        header = request.META.get("HTTP_AUTHORIZE")

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header
