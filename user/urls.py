from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

import user.views.user_view as uvu

router = DefaultRouter(trailing_slash=False)
app_router = routers.DefaultRouter()

app_router.register('organisation', uvu.EmployerViewSet, 'organisation')
app_router.register('individual', uvu.EmployeeViewSet, 'individual')
app_router.register('wallet', uvu.WalletViewSet, 'wallet')


urlpatterns = [
    path('', include(app_router.urls)),
]
