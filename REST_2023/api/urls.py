from django.urls import path

from REST_2023.api.views import EmployeesListApiView, DepartmentsListApiView, DemoApiView

urlpatterns = (
    path('employees/', EmployeesListApiView.as_view(), name='api get employees'),
    path('departments/', DepartmentsListApiView.as_view(), name='api get departments'),
    path('demo/', DemoApiView.as_view(), name='demo view'),
)
