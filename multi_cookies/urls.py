# coding: utf-8
from functools import update_wrapper

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.admin import site as admin_site
from django.contrib.auth.views import logout

from multi_cookies.decorators import set_auth_cookie, external_redirect

from student.views import LogoutView, login_user, signin_user, register_user
from student_account.views import login_and_registration_form
from auth_exchange.views import LoginWithAccessTokenView
import contentstore.views
import external_auth.views
import django_cas.views


def wrap_admin(view, cacheable=False):
    def wrapper(*args, **kwargs):
        return admin_site.admin_view(view, cacheable)(*args, **kwargs)
    wrapper.admin_site = admin_site
    return update_wrapper(wrapper, view)


urlpatterns = patterns(
    '',
    #  админка
    url(r'^admin/login/$', set_auth_cookie(admin_site.login), name='admin:login'),
    url(r'^admin/logout/$', set_auth_cookie(wrap_admin(admin_site.logout)), name='logout'),
    # cms
    url(r'^signup$', set_auth_cookie(contentstore.views.signup), name='signup'),
    url(r'^signin$', set_auth_cookie(contentstore.views.login_page), name='login'),
    # lms
    url(r'^login_ajax$', set_auth_cookie(login_user), name="login"),
    url(r'^logout$', external_redirect(set_auth_cookie(LogoutView.as_view())),
        name='logout'),
)

if settings.FEATURES.get('AUTH_USE_CAS'):
    urlpatterns += (
        url(r'^cas-auth/login/$',
            set_auth_cookie(external_auth.views.cas_login),
            name="cas-login"),
        url(r'^cas-auth/logout/$',
            external_redirect(set_auth_cookie(django_cas.views.logout)),
            {'next_page': '/'}, name="cas-logout"),
    )

if settings.FEATURES["ENABLE_COMBINED_LOGIN_REGISTRATION"]:
    # Backwards compatibility with old URL structure, but serve the new views
    urlpatterns += (
        url(r'^login$', set_auth_cookie(login_and_registration_form),
            {'initial_mode': 'login'}, name="signin_user"),
        url(r'^register$', set_auth_cookie(login_and_registration_form),
            {'initial_mode': 'register'}, name="register_user"),
    )
else:
    # Serve the old views
    urlpatterns += (
        url(r'^login$', set_auth_cookie(signin_user), name="signin_user"),
        url(r'^register$', set_auth_cookie(register_user), name="register_user"),
    )

if settings.FEATURES.get('ENABLE_OAUTH2_PROVIDER'):
    urlpatterns += (
        url(
            r'^oauth2/login/$',
            set_auth_cookie(LoginWithAccessTokenView.as_view()),
            name="login_with_access_token"
        ),
    )
