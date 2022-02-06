from rest_framework.routers import DefaultRouter

from .views import GlucoseLevelViewset

app_name = 'levels'

router = DefaultRouter()
router.register('levels', GlucoseLevelViewset, 'levels')

urlpatterns = router.urls
