from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views import defaults as default_views
from socialmedia import urls as socialmedia_urls
from socialmedia.basecore import views as core_views
from socialmedia.activities import views as activities_views
from socialmedia.authentication import views as socialmedia_auth_views
from socialmedia.search import views as search_views

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^yourbox/', core_views.your_box, name='fbox'),
    url(r'^contact/', core_views.contact, name='contact_us'),
    url(r'^signup/$', socialmedia_auth_views.signup, name='signup'),
    url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/picture/$', core_views.picture, name='picture'),
    url(r'^settings/upload_picture/$', core_views.upload_picture,
      name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', core_views.save_uploaded_picture,
      name='save_uploaded_picture'),

    url(r'^settings/upload_bg_picture/$', core_views.upload_bg_picture,
      name='upload_bg_picture'),
    url(r'^settings/save_uploaded_bg_picture/$', core_views.save_uploaded_bg_picture,
      name='save_uploaded_bg_picture'),

    url(r'^settings/password/$', core_views.password, name='password'),
    url(r'^network/$', core_views.network, name='network'),
    url(r'^feeds/', include('socialmedia.feeds.urls')),
    url(r'^questions/', include('socialmedia.questions.urls')),
    url(r'^articles/', include('socialmedia.articles.urls')),
    url(r'^messages/', include('socialmedia.messenger.urls'), name='messages'),
    url(r'^notifications/$', activities_views.notifications,
        name='notifications'),
    url(r'^notifications/last/$', activities_views.last_notifications,
        name='last_notifications'),
    url(r'^notifications/check/$', activities_views.check_notifications,
        name='check_notifications'),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^(?P<username>[^/]+)/$', core_views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns


if 'cms' in settings.INSTALLED_APPS:
    from django.contrib.sitemaps.views import sitemap
    from cms.sitemaps import CMSSitemap
    urlpatterns += [
        url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'cmspages': CMSSitemap}}),
        url(r'^', include('cms.urls')),
    ]
else:
    urlpatterns += [
        url(r'^$', TemplateView.as_view(template_name='index.html')),
    ]

if 'imprint' in settings.INSTALLED_APPS:
    from imprint.views import AboutView
    urlpatterns += [
        url(r'^about/$', AboutView.as_view(), name='about'),
    ]

