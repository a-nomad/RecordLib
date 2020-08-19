"""
Views for the basic user interface of the webapp; logging in and getting the frontend app.
"""
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response


class FrontendView(LoginRequiredMixin, TemplateView):
    """
    Serve the fronend app. 
    """

    login_url = "/api/accounts/login/"
    template_name = "backend/index.html"

    def get(self, request):
        """ GET the frontend app."""
        current_user = request.user
        return render(
            request, "backend/index.html", context={"username": current_user.username}
        )


# noinspection PyMethodMayBeStatic
class LoginSuccessView(APIView):
    """ 
    Confirm that login was successful.
    """

    def get(self, request):
        """Login was successful. Tell the client."""
        content = {"username": request.user.username}
        return Response(content)


# noinspection PyMethodMayBeStatic
class LoginFailureView(APIView):
    """
    Login failed.
    """

    def get(self, request):
        """Login failed."""
        return Response({"errors": "login failed."})

