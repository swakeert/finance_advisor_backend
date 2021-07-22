"""finance_advisor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from finance_advisor.advisees.urls import advisee_router
from finance_advisor.advisors.urls import advisor_router
from finance_advisor.cash_flows.urls import advisee_cash_flow_router
from finance_advisor.core.urls import core_router
from finance_advisor.core.views import TokenObtainPairWithUserInfoView
from finance_advisor.goals.urls import goal_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/login/", TokenObtainPairWithUserInfoView.as_view()),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view()),
    path("api/v1/advisees/", include(advisee_router.urls)),
    path("api/v1/advisees/<int:advisee_id>/goals/", include(goal_router.urls)),
    path("api/v1/advisees/<int:advisee_id>/", include(advisee_cash_flow_router.urls)),
    path("api/v1/advisors/", include(advisor_router.urls)),
    path("api/v1/core/", include(core_router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
