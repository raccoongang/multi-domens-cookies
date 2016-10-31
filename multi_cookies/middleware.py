from django.conf import settings

import logging
log = logging.getLogger(__name__)


class RemoteUserAuthMiddleware(object):

    def process_response(self, request, response):
        if 'admin' not in request.path:
            user = request.user
            is_auth = user.is_authenticated()

            response.set_cookie('authenticated', str(int(is_auth)),
                                domain=settings.AUTH_SESSION_COOKIE_DOMAIN,
                                secure=settings.SESSION_COOKIE_SECURE or None,
                                max_age=settings.SESSION_COOKIE_AGE)
            response.set_cookie('authenticated_user',
                                is_auth and user.username or 'Anonymous',
                                domain=settings.AUTH_SESSION_COOKIE_DOMAIN,
                                secure=settings.SESSION_COOKIE_SECURE or None,
                                max_age=settings.SESSION_COOKIE_AGE)
            response.set_cookie('authenticated_email',
                                is_auth and user.email or '',
                                domain=settings.AUTH_SESSION_COOKIE_DOMAIN,
                                secure=settings.SESSION_COOKIE_SECURE or None,
                                max_age=settings.SESSION_COOKIE_AGE)
        return response
