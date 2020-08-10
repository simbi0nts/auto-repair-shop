
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from diag_api.logic.workflow import (CheckRepairShopWorkloadLogic,
                                     MakeAppointmentLogic,
                                     GetAvailableAppointmentTimeLogic)


class BaseApiView(APIView):
    permission_classes = (IsAuthenticated,)
    context_class = None

    def process_request(self, request):
        content = self.context_class.process(request)
        return Response(content)

    def get(self, request):
        return self.process_request(request)

    def post(self, request):
        return self.process_request(request)


class MakeAppointment(BaseApiView):
    context_class = MakeAppointmentLogic
    http_method_names = ['post']


class CheckRepairShopWorkload(BaseApiView):
    context_class = CheckRepairShopWorkloadLogic
    http_method_names = ['get']


class GetAvailableAppointmentTime(BaseApiView):
    context_class = GetAvailableAppointmentTimeLogic
    http_method_names = ['get']
