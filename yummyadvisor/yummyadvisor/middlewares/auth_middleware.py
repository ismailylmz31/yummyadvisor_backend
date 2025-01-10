import json
from urllib.request import urlopen
from jose import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class Auth0JSONWebTokenAuthentication:
    def __init__(self):
        self.auth0_domain = settings.AUTH0_DOMAIN
        self.api_identifier = settings.API_IDENTIFIER
        self.issuer = f"https://{self.auth0_domain}/"

    def decode_jwt(self, token):
        header = jwt.get_unverified_header(token)
        rsa_key = {}
        if "kid" not in header:
            raise AuthenticationFailed("Authorization malformed.")

        try:
            # JWKS URL
            url = f"https://{self.auth0_domain}/.well-known/jwks.json"
            jwks = json.loads(urlopen(url).read())
            for key in jwks["keys"]:
                if key["kid"] == header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"],
                    }
            if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=self.api_identifier,
                    issuer=self.issuer,
                )
                return payload
        except Exception:
            raise AuthenticationFailed("Unable to verify token.")
