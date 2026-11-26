"""
Маршруты приложения habits.
URL routes of the habits app.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from habits.views import HabitViewSet, PublicHabitViewSet

# ============================================
# Роутер создаёт list/create/retrieve/update/destroy
# ============================================
# The router generates list/create/retrieve/update/destroy
# ============================================
router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")
router.register(r"public/habits", PublicHabitViewSet, basename="public-habit")

urlpatterns = [
    path("", include(router.urls)),
]
