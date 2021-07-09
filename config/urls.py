from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views import defaults as default_views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from graphene_django.views import GraphQLView

from kittytracker.schema import schema

# from django.contrib.auth.decorators import login_required
# from kittytracker.tracker.views import PrivateGraphQLView

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),
    url(r'^graphql', GraphQLView.as_view(graphiql=True, schema=schema)),

    url(r'^api/v1/', include('kittytracker.tracker.api.urls', namespace='tracker_api')),
    url(r'^tracker/', include('kittytracker.tracker.urls', namespace='tracker_crud')),

    # User management
    url(r'^users/', include('kittytracker.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here
    url(r'^api/v1/auth/obtain_token/', obtain_jwt_token),
    url(r'^api/v1/auth/refresh_token/', refresh_jwt_token),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

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
