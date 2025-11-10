from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from starlette.requests import Request
from ..schemas.tokenScheamas import TokenData
from ..app import AppException
from ..configurations import jwtConf as secure



secure_cfg = secure.JwtConfig(conf=secure.Configure(default="./config.json"))



# Configuration
SECRET_KEY =secure_cfg.custom_config['secret_key']
ALGORITHM = secure_cfg.custom_config['algorithm']
ACCESS_TOKEN_EXPIRE_MINUTES = secure_cfg.custom_config['access_token_expire_minutes']
REFRESH_TOKEN_EXPIRE_DAYS = secure_cfg.custom_config['refresh_token_expire_days']




def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """Crée un token d'accès JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Crée un token de rafraîchissement"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    """Décode et valide un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id: int = payload.get("sub")
        username: str = payload.get("username")
        email: str = payload.get("email")
        roles: list = payload.get("roles", [])
        
        if user_id is None:
            raise AppException(
                "Token invalide",
                status_code=401,
                details={"reason": "missing_user_id"}
            )
        
        return TokenData(
            user_id=user_id,
            username=username,
            email=email,
            roles=roles
        )
    
    except JWTError as e:
        raise AppException(
            "Token invalide ou expiré",
            status_code=401,
            details={"reason": str(e)}
        )


def extract_token_from_header(authorization: str) -> str:
    """Extrait le token du header Authorization"""
    if not authorization:
        raise AppException(
            "Authorization header manquant",
            status_code=401,
            details={"reason": "missing_authorization_header"}
        )
    
    parts = authorization.split()
    
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise AppException(
            "Format du header Authorization invalide",
            status_code=401,
            details={"reason": "invalid_authorization_format"}
        )
    
    return parts[1]


async def get_current_user(request: Request) -> TokenData:
    """
    Dépendance pour obtenir l'utilisateur courant à partir du token JWT
    Usage: @app.route("/protected", methods=["GET"])
           async def protected_route(user: User = Depends(get_current_user)):
    """
    authorization = request.headers.get("authorization")
    token = extract_token_from_header(authorization)
    token_data = decode_token(token)
    return token_data
