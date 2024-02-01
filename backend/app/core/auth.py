import json
import logging
from fastapi import Depends, HTTPException, Header, Request, status
from fastapi.openapi.models import OAuthFlows, OAuthFlowImplicit
from fastapi.security import (HTTPAuthorizationCredentials, HTTPBearer,
                              OAuth2, OAuth2AuthorizationCodeBearer,
                              OAuth2PasswordBearer, OpenIdConnect, SecurityScopes)
from pydantic import BaseModel, Field, ValidationError
from typing_extensions import TypedDict
import urllib.parse
from jose import jwt
from typing import Dict, List, Optional, Type
from app.core.config import settings

logger = logging.getLogger('auth_logging')

class Auth0UnauthenticatedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        """Returns HTTP 401"""
        super().__init__(401, detail, **kwargs)

class Auth0UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        """Returns HTTP 403"""
        super().__init__(403, detail, **kwargs)

class HTTPAuth0Error(BaseModel):
    detail: str

unauthenticated_response: Dict = {401: {'model': HTTPAuth0Error}}
unauthorized_response:    Dict = {403: {'model': HTTPAuth0Error}}
security_responses:       Dict = {**unauthenticated_response, **unauthorized_response}


class Auth0User(BaseModel):
    id:                          str = Field(..., alias='sub')
    permissions: Optional[List[str]] = None
    email:             Optional[str] = Field(None, alias=f'{settings.AUTH0_RULE_NAMESPACE}/email')  # type: ignore [literal-required]


class Auth0HTTPBearer(HTTPBearer):
    async def __call__(self, request: Request):
        return await super().__call__(request)

class OAuth2ImplicitBearer(OAuth2):
    def __init__(self,
            authorizationUrl: str,
            scopes: Dict[str, str]={},
            scheme_name: Optional[str]=None,
            auto_error: bool=True):
        flows = OAuthFlows(implicit=OAuthFlowImplicit(authorizationUrl=authorizationUrl, scopes=scopes))
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        # Overwrite parent call to prevent useless overhead, the actual auth is done in Auth0.get_user
        # This scheme is just for Swagger UI
        return None


class JwksKeyDict(TypedDict):
    kid: str
    kty: str
    use: str
    n: str
    e: str

class JwksDict(TypedDict):
    keys: List[JwksKeyDict]


class Auth0:
    def __init__(self, domain: str, api_audience: str, scopes: Dict[str, str]={},
            auto_error: bool=True, scope_auto_error: bool=True, email_auto_error: bool=False,
            auth0user_model: Type[Auth0User]=Auth0User):
        self.domain = domain
        self.audience = api_audience

        self.auto_error = auto_error
        self.scope_auto_error = scope_auto_error
        self.email_auto_error = email_auto_error

        self.auth0_user_model = auth0user_model

        self.algorithms = ['RS256']
        r = urllib.request.urlopen(f'https://{domain}/.well-known/jwks.json')
        self.jwks: JwksDict = json.loads(r.read())

        authorization_url_qs = urllib.parse.urlencode({'audience': api_audience})
        authorization_url = f'https://{domain}/authorize?{authorization_url_qs}'
        self.implicit_scheme = OAuth2ImplicitBearer(
            authorizationUrl=authorization_url,
            scopes=scopes,
            scheme_name='Auth0ImplicitBearer')
        self.password_scheme = OAuth2PasswordBearer(tokenUrl=f'https://{domain}/oauth/token', scopes=scopes)
        self.authcode_scheme = OAuth2AuthorizationCodeBearer(
            authorizationUrl=authorization_url,
            tokenUrl=f'https://{domain}/oauth/token',
            scopes=scopes)
        self.oidc_scheme = OpenIdConnect(openIdConnectUrl=f'https://{domain}/.well-known/openid-configuration')
        
    async def validate_api_key(self, api_key: str) -> Optional[Auth0User]:
        # Implement your API key validation logic here
        # This is a placeholder implementation
        if api_key == "valid_api_key":
            # Simulate fetching an Auth0User associated with this API key
            return Auth0User(sub="api_key_user_id", email="api_user@example.com")
        return None
    
    
    # TODO: Implement this method to fetch user details from Auth0
    # async def verify_api_key(self, api_key: str, db: Session) -> Optional[Auth0User]:
    #     # Check if the API key exists and is valid
    #     api_key_entry = db.query(ApiKey).filter(ApiKey.key == api_key).first()
    #     if not api_key_entry:
    #         return None
        
    #     # Use the user_id from the API key entry to fetch user details from Auth0
    #     user_id = api_key_entry.user_id
    #     url = f"https://{settings.AUTH0_DOMAIN}/api/v2/users/{user_id}"
    #     headers = {
    #         "Authorization": f"Bearer {settings.AUTH0_MANAGEMENT_API_TOKEN}"
    #     }
        
    #     response = requests.get(url, headers=headers)
    #     if response.status_code == 200:
    #         user_info = response.json()
    #         # Map the Auth0 response to your Auth0User model fields
    #         return Auth0User(sub=user_info["user_id"], email=user_info["email"])
    #     else:
    #         # Log or handle the error appropriately
    #         logger.error(f"Failed to fetch user from Auth0: {response.text}")
    #         return None

    async def get_user(self, security_scopes: SecurityScopes, creds: Optional[HTTPAuthorizationCredentials] = Depends(Auth0HTTPBearer(auto_error=False)), api_key: str = Header(None)):
        if api_key:
            user = await self.validate_api_key(api_key)
            if user:
                return user
            # If API Key validation fails and auto_error is True, raise an error
            if self.auto_error:
                raise HTTPException(status_code=403, detail="Invalid API Key")

        """
        Verify the Authorization: Bearer token and return the user.
        If there is any problem and auto_error = True then raise Auth0UnauthenticatedException or Auth0UnauthorizedException,
        otherwise return None.

        Not to be called directly, but to be placed within a Depends() or Security() wrapper.
        Example: def path_op_func(user: Auth0User = Security(auth.get_user)).
        """
        if creds is None:
            if self.auto_error:
                # See HTTPBearer from FastAPI:
                # latest - https://github.com/tiangolo/fastapi/blob/master/fastapi/security/http.py
                # 0.65.1 - https://github.com/tiangolo/fastapi/blob/aece74982d7c9c1acac98e2c872c4cb885677fc7/fastapi/security/http.py
                raise HTTPException(403, detail='Missing bearer token')  # must be 403 until solving https://github.com/tiangolo/fastapi/pull/2120
            else:
                return None

        token = creds.credentials
        payload: Dict = {}
        try:
            unverified_header = jwt.get_unverified_header(token)
            if 'kid' not in unverified_header:
                msg = 'Malformed token header'
                if self.auto_error:
                    raise Auth0UnauthenticatedException(detail=msg)
                else:
                    logger.warning(msg)
                    return None
                
            rsa_key = {}
            for key in self.jwks['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }
                    break
            if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=self.algorithms,
                    audience=self.audience,
                    issuer=f'https://{self.domain}/'
                )
            else:
                msg = 'Invalid kid header (wrong tenant or rotated public key)'
                if self.auto_error:
                    raise Auth0UnauthenticatedException(detail=msg)
                else:
                    logger.warning(msg)
                    return None

        except jwt.ExpiredSignatureError:
            msg = 'Expired token'
            if self.auto_error:
                raise Auth0UnauthenticatedException(detail=msg)
            else:
                logger.warning(msg)
                return None

        except jwt.JWTClaimsError:
            msg = 'Invalid token claims (wrong issuer or audience)'
            if self.auto_error:
                raise Auth0UnauthenticatedException(detail=msg)
            else:
                logger.warning(msg)
                return None

        except jwt.JWTError:
            msg = 'Malformed token'
            if self.auto_error:
                raise Auth0UnauthenticatedException(detail=msg)
            else:
                logger.warning(msg)
                return None

        except Auth0UnauthenticatedException:
            raise

        except Exception as e:
            # This is an unlikely case but handle it just to be safe (maybe the token is specially crafted to bug our code)
            logger.error(f'Handled exception decoding token: "{e}"', exc_info=True)
            if self.auto_error:
                raise Auth0UnauthenticatedException(detail='Error decoding token')
            else:
                return None

        if self.scope_auto_error:
            token_scope_str: str = payload.get('scope', '')

            if isinstance(token_scope_str, str):
                token_scopes = token_scope_str.split()

                for scope in security_scopes.scopes:
                    if scope not in token_scopes:
                        raise Auth0UnauthorizedException(detail=f'Missing "{scope}" scope',
                            headers={'WWW-Authenticate': f'Bearer scope="{security_scopes.scope_str}"'})
            else:
                # This is an unlikely case but handle it just to be safe (perhaps auth0 will change the scope format)
                raise Auth0UnauthorizedException(detail='Token "scope" field must be a string')

        try:
            user = self.auth0_user_model(**payload)

            if self.email_auto_error and not user.email:
                raise Auth0UnauthorizedException(detail=f'Missing email claim (check auth0 rule "Add email to access token")')

            return user

        except ValidationError as e:
            logger.error(f'Handled exception parsing Auth0User: "{e}"', exc_info=True)
            if self.auto_error:
                raise Auth0UnauthorizedException(detail='Error parsing Auth0User')
            else:
                return None
            
            
auth = Auth0(domain=settings.AUTH0_DOMAIN, api_audience=settings.AUTH0_API_IDENTIFIER)

