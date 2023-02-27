from abc import ABC

from django.views import generic as view
from rest_framework import generics as rest_views
from rest_framework import serializers
from rest_framework import views as rest_base_views
from rest_framework.response import Response

from REST_2023.api.models import Employee, Department


class ShortEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name')


class DepartmentSerializer(serializers.ModelSerializer):
    employee_set = ShortEmployeeSerializer(many=True)

    class Meta:
        model = Department
        fields = '__all__'


class ShortDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    department = ShortDepartmentSerializer()

    class Meta:
        model = Employee
        fields = '__all__'


# class DemoSerializer(serializers.Serializer, ABC):
#     # def update(self, instance, validated_data):
#     #     pass
#     #
#     # def create(self, validated_data):
#     #     pass
#
#     key = serializers.CharField()
#     value = serializers.IntegerField()


# Server-side rendering(the result is HTML)
class EmployeesListView(view.ListView):
    model = Employee
    template_name = ''


class DepartmentsListApiView(rest_views.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


# JSON serialization(parse models into JSON)
# class EmployeesListApiView(rest_views.ListCreateAPIView):
class EmployeesListApiView(rest_views.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        department_id = self.request.query_params.get('department')
        queryset = self.queryset
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset


class DemoSerializer(serializers.Serializer):
    employees = ShortEmployeeSerializer(many=True)
    employees_count = serializers.IntegerField()
    departments = ShortDepartmentSerializer(many=True)
    first_department = serializers.CharField()


class DemoApiView(rest_base_views.APIView):
    def get(self, request):
        employees = Employee.objects.all()
        departments = Department.objects.all()
        body = {
            'employees': employees,
            'employees_count': employees.count(),
            'departments': departments,
            'first_department': departments.first()
        }

        serializer = DemoSerializer(body)

        return Response(serializer.data)

