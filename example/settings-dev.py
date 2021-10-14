from settings import *  # noqa

INSTALLED_APPS += [
    "livereload",
]

MIDDLEWARE += [
    "livereload.middleware.LiveReloadScript",
]
