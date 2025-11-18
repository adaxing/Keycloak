from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakOpenID
from config.keycloak_config import settings
from fastapi import Security, HTTPException, status, Depends
from schemas import userPayload

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.token_url
)

keycloak_openid = KeycloakOpenID(
    server_url=settings.server_url,
    realm_name=settings.realm,
    client_id=settings.client_id,
    client_secret_key=settings.client_secret,
    verify=True
)
# print(keycloak_openid.public_key())
# public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkDTSlgd+VWplL27YzB+/mG5tPJzzhFbNxDUPHliQqZ9D/0u82e+cL4YPXcQdIXD9heDhBppWJjE/fryvquzFECmdFenMumqXBfPwrQy1TQrs2J4+bMGHyLFP2UGOtX3vsboOZyxEv6LHrXfFangQIURwXfMyRNUCmnTRDLx9sr8Y+NY1qZmLOX5sAl8meeSFgJbwzdzGlghwOIHEsZaTDGAHQLnNm8o2/lLwJ5mpN05ZF/15UVP7SEt0qU6ys7D2T2PJ6+FqjZD94gCkAKHWX1wJFz7slSeAKT9mh3qPi6I5WuKwqbij5RHTBZox17H0xQH8zIsqG3pYsP0wb//b/wIDAQAB"
async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        + f'{keycloak_openid.public_key()}'
        + "\n-----END PUBLIC KEY-----"
    )
    
    
async def get_payload(token: str = Security(oauth2_scheme)) -> dict:
    try: 
        return keycloak_openid.decode_token(
            token,
            # key=public_key,
            # options={"verify_signature": True, "verify_aud": False, "exp": True}
        )
    except Exception as e:
        print(e)
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail=str(e),
        #     headers={'www-Authenticate': 'Bearer'}
        # )
        
async def get_user_info(payload: dict = Depends(get_payload)) -> userPayload:
    try:
        return userPayload(
            id=payload.get('sub'),
            username=payload.get('preferred_username'),
            email=payload.get('email'),
            # first_name=payload.get('given_name'),
            # last_name=payload.get('family_name'),
            realm_roles=payload.get('realm_access', {}).get('roles', []),
            client_roles=payload.get('realm_access', {}).get('roles', [])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={'www-Authenticate': 'Bearer'}
        )