from functools import wraps
from sanic.log import logger
from sanic.response import json
import jwt
from Base import message
from Query import Permission


def permission(code):
    """check user permission

    must be warp before all decorator

    Args:
        code: permission code
    """

    def decorator(f):
        # @debug
        @wraps(f)
        async def permission_decorator(request, *args, **kwargs):

            config = request.app.config
            try:
                # token = request.args['token']
                auth_header = request.headers['Authorization']
            except KeyError as e:
                logger.debug(e)
                return json(message('invalid session'))

            if auth_header.startswith('Bearer'):
                bearer = auth_header.split(' ', 1)
                token = bearer[1]

            payload = None
            try:
                payload = jwt.decode(
                    token, config.JWT['jwtSecret'],
                    algorithms=config.JWT['algorithm']
                )
            except jwt.ExpiredSignatureError as e:
                logger.info(e)
                return json(message('session_expired'), 401)
            except jwt.PyJWTError as e:
                logger.warning(e)
                return json(message('invalid_session'), 401)

            query = Permission()

            is_authorized = query.check_permission(payload['username'], code)

            if is_authorized:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json(message('no_permission'), 403)

        return permission_decorator

    return decorator
