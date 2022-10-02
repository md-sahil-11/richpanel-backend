
from django.contrib.auth import authenticate
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.AllowAny,),
    )
    def login(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            return Response({"success": False, "err": "Invalid password or email!"})
        data = UserSerializer(user).data
        token, _ = Token.objects.get_or_create(user=user)
        result = {**data}
        result['token'] = token.key
        return Response({"success": True, "data": result})
   
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def logout(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response({"success": True})
    
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.AllowAny,),
    )
    def register(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        name = request.data.get("name")

        user = User.objects.create(
            email=email,
            name=name,
        )
        user.set_password(password)
        user.save()
        if not user:
            return Response({"success": False, "err": "Invalid password or email!"})
        data = UserSerializer(user).data
        token, _ = Token.objects.get_or_create(user=user)
        # import pdb; pdb.set_trace()
        result = {**data}
        result['token'] = token.key
        return Response({"success": True, "data": result})