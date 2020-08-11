# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from api.views.workflow import (CheckRepairShopWorkload,
                                GetAvailableAppointmentTime,
                                MakeAppointment)

admin.autodiscover()


urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('make_appointment/', MakeAppointment.as_view(), name='make_appointment'),
    path('check_workload/', CheckRepairShopWorkload.as_view(), name='check_workload'),
    path('get_available_appointment_time/', GetAvailableAppointmentTime.as_view(), name='get_available_appointment_time'),
]
