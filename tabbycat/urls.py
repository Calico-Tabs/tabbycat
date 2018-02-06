from django.conf import settings
from django.urls import include, path
from django.contrib import admin, messages
from django.contrib.auth.views import logout as auth_logout
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django.views.generic.base import RedirectView
from django.views.i18n import JavaScriptCatalog

import tournaments.views

admin.autodiscover()

# ==============================================================================
# Base Patterns
# ==============================================================================

urlpatterns = [

    # Indices
    path('',
        tournaments.views.PublicSiteIndexView.as_view(),
        name='tabbycat-index'),
    path('start/',
        tournaments.views.BlankSiteStartView.as_view(),
        name='blank-site-start'),
    path('create/',
        tournaments.views.CreateTournamentView.as_view(),
        name='tournament-create'),
    path('load-demo/',
        tournaments.views.LoadDemoView.as_view(),
        name='load-demo'),

    # Top Level Pages
    path('donations/',
        tournaments.views.DonationsView.as_view(),
        name='donations'),
    path('style/',
        tournaments.views.StyleGuideView.as_view(),
        name='style-guide'),

    # Set language override
    path('i18n/',
        include('django.conf.urls.i18n')),

    # JS Translations Catalogue; includes all djangojs files in locale folders
    path('jsi18n/',
         JavaScriptCatalog.as_view(domain="djangojs", ),
         name='javascript-catalog'),

    # Admin area
    path('jet/',
        include('jet.urls', 'jet')),
    path('database/',
        admin.site.urls),

    # Accounts
    path('accounts/logout/',
        auth_logout,
        {'next_page': '/'},  # override to specify next_page
        name='logout'),
    path('accounts/',
        include('django.contrib.auth.urls')),

    # Favicon for old browsers that ignore <head> links and always load via root
    path('favicon\.ico',
        RedirectView.as_view(url='/static/favicon.ico')),

    # Tournament URLs
    path('<slug:tournament_slug>/',
        include('tournaments.urls')),

    # Draws Cross Tournament
    path('draw/',
        include('draw.urls_crosst')),
]

if settings.DEBUG and settings.ENABLE_DEBUG_TOOLBAR:  # Only serve debug toolbar when on DEBUG
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))


# ==============================================================================
# Logout/Login Confirmations
# ==============================================================================

# These messages don't always work properly with unit tests, so set fail_silently=True

@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    if kwargs.get('user'):
        messages.info(request,
            _("Later, %(username)s — you were logged out!") % {'username': kwargs['user'].username},
            fail_silently=True)
    else: # should never happen, but just in case
        messages.info(request, _("Later! You were logged out!"), fail_silently=True)


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    if kwargs.get('user'):
        messages.info(request,
            _("Hi, %(username)s — you just logged in!")  % {'username': kwargs['user'].username},
            fail_silently=True)
    else: # should never happen, but just in case
        messages.info(request, _("Welcome! You just logged in!"), fail_silently=True)


# ==============================================================================
# Redirect Method
# ==============================================================================

def redirect(view):
    from django.http import HttpResponseRedirect
    from django.urls import reverse

    def foo(request):
        return HttpResponseRedirect(reverse(view))

    return foo
