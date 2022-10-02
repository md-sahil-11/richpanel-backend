from rest_framework.routers import DefaultRouter

from . import views

app_name = "subscription"

router = DefaultRouter(trailing_slash=False)

router.register("history", views.SubscriptionHistoryViewSet, basename="history")
router.register("plans", views.PlanViewSet, basename="plans")

urlpatterns = router.urls
