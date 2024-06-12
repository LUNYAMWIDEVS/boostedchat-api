from functools import wraps
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

def jwt_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        auth = JWTAuthentication()
        try:
            user, _ = auth.authenticate(request)
            if user is None:
                raise Exception("Invalid token")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(request, *args, **kwargs)
    return wrapped_view
