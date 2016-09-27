import logging

from django.conf import settings

log = logging.getLogger(__name__)

class UserStandingMiddleware(object):
    """
    Checks a user's standing on request. Returns a 403 if the user's
    status is 'disabled'.
    """
    def process_response(self, request, response):
        log.info('{} !!!!'.format(dir(request)))
        if 'admin' in request.path:
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
        return response
