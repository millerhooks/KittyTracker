from django.conf.urls import url, include
from rest_framework import routers
from kittytracker.tracker.views import CatViewSet, FeedingViewSet

router = routers.DefaultRouter()
router.register(r'cats', CatViewSet)
router.register(r'feedings', FeedingViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
