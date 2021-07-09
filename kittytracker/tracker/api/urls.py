from django.conf.urls import url, include
from rest_framework import routers
from .views import MedicationViewSet, LitterViewSet, CatViewSet, \
    CareLogViewSet, FosterAlertViewSet, VetVisitViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'medications', MedicationViewSet)
router.register(r'litter', LitterViewSet)
router.register(r'cats', CatViewSet)
router.register(r'carelogs', CareLogViewSet)
router.register(r'fosteralerts', FosterAlertViewSet)
router.register(r'vetvisit', VetVisitViewSet)
router.register(r'users', UserViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
