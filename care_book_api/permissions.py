from rest_framework.permissions import BasePermission

class IsParent(BasePermission):
	message = "You must be a parent of the home!"

	def has_object_permission(self, request, view, obj):
		if (obj.user == request.user):
			return True
		else:
			return False