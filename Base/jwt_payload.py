from datetime import datetime, timedelta


def jwt_payload(username: str, permission_list: list):
    """
    Return JWT payload base

    Attributes:
        session_limit -- The survive time of this session (deprecated)
        username -- Username field
    """
    # RFC 7519
    payload = {
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1),
        "username": username,
        "permission": permission_list,
    }
    return payload
