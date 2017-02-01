from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

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


class RedirectToPortal(object):
    portal_host = settings.FEATURES.get('PORTAL_HOST', 'example.com')
    portal_url = '{}://{}'.format(settings.FEATURES.get('PORTAL_SCHEME', 'http'), portal_host)
    
    def process_request(self, request):
        cms_host = getattr(settings, 'CMS_BASE', None)
        if not request.user.is_authenticated() and cms_host and request.META['HTTP_HOST'] != cms_host:
            register_url = reverse('register_user')
            registration_complete_url = reverse('registration-complete')
            login_url = reverse('signin_user')

            is_register = (
                request.META['PATH_INFO'] in (register_url, registration_complete_url)
                or request.META['PATH_INFO'].startswith('/activate')
            )
            is_internal_url = (
                request.META['PATH_INFO'].startswith('/user_api')
                or request.META['PATH_INFO'].startswith(settings.STATIC_URL)
            )
            is_oauth2_login = (
                request.META['PATH_INFO'] == login_url 
#                and (
#                    'oauth2' in request.META['RAW_URI'] 
#                    and self.portal_host in request.META['RAW_URI']
#                   or request.META['HTTP_REFERER'].startswith(self.portal_url)
#                )
            )
            is_oauht2_urls = (
                request.META['PATH_INFO'].startswith('/oauth2') 
                or request.META['PATH_INFO'].startswith('/auth') 
                or request.META['PATH_INFO'].startswith('/login_oauth_token')
            )

            if is_register or is_internal_url or is_oauth2_login or is_oauht2_urls:
                return None

            return redirect(self.portal_url)
