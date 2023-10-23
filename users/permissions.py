from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.exceptions import PermissionDenied
from users.models import ReportModel, UserAccount
class CanCreateReportPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user  
        
        if user.report_test:
            raise PermissionDenied("You have already created a report. You cannot create another one.")
        return True