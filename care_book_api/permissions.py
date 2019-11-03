from rest_framework.permissions import BasePermission

from .models import Home, Child

class IsHomeParent(BasePermission):
	message = "You must be a parent of the home!"

	def has_permission(self, request, view):
		home = Home.objects.get(id=view.kwargs['home_id'])
		if home.parents.filter(username=request.user): 
			return True
		else:
			return False


class IsChildParent(BasePermission):
	message = "You must be a parent of the child!"

	def has_permission(self, request, view):
		child = Child.objects.get(id=view.kwargs['child_id'])
		if child.home.parents.filter(username=request.user): 
			return True
		else:
			return False