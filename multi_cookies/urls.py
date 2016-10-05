# coding: utf-8
from functools import update_wrapper

from django.conf.urls import patterns, include, url
from django.contrib.admin import site as admin_site

from multi_cookies.decorators import set_auth_cookie


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
)
