# multi-domens-cookies

install:

  pip install -e git+https://github.com/raccoongang/multi-domens-cookies

add into settings vars for edx:

  AUTH_SESSION_COOKIE_DOMAIN = '.domain.com'

  ROOT_URLCONF = 'multi_cookies.[lms|cms]_urls'

  middleware_CLASSES = (
     ...,
     'multi_cookies.middleware.RemoteUserAuthMiddleware',
     ...,
   )
