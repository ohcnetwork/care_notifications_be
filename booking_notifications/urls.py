"""No HTTP endpoints — this plug is purely signal- and celery-driven.

Care's ``config/urls.py`` unconditionally does ``include(f"{plug}.urls")`` for
every entry in ``PLUGIN_APPS``, so we must expose this module even with an
empty pattern list, otherwise app boot fails with ``ModuleNotFoundError``.
"""

urlpatterns: list = []
