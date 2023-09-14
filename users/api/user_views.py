import math, base64, pandas as pd, openai, environ, json
from django.db import DatabaseError
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.forms import EmailField
from django.contrib.auth import authenticate, login
from django.middleware import csrf
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework import (
    exceptions as rest_exceptions,
    
    decorators as rest_decorators,
    permissions as rest_permissions,
    status as rest_status,
)
from rest_framework.response import Response
from rest_framework_simplejwt import (
    tokens,
    views as jwt_views,
    serializers as jwt_serializers,
    exceptions as jwt_exceptions,
)
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from asgiref.sync import sync_to_async
from users import models

# from app.helpers.async_user_helpers import *
from users.helpers.sync_user_helpers import *
from users.serializers import user_serializers

# Create your views here.
env = environ.Env()
environ.Env.read_env()


def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {"refresh_token": str(refresh), "access_token": str(refresh.access_token)}


@swagger_auto_schema(method="POST", request_body=user_serializers.LoginSerializer)
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def loginView(request):
    serializer = user_serializers.LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]
    user = authenticate(email=email, password=password)
    if user is not None:
        tokens = get_user_tokens(user)
        res = Response()
        res.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=tokens["access_token"],
            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        res.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
            value=tokens["refresh_token"],
            expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        res.data = tokens

        res["X-CSRFToken"] = csrf.get_token(request)

        return res
    raise rest_exceptions.AuthenticationFailed("Username or Password is incorrect!")


@swagger_auto_schema(
    method="POST", request_body=user_serializers.RegistrationSerializer
)
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def registerView(request):
    print(request.data)
    serializer = user_serializers.RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    if user is not None:
        return Response("Registered!")
    # return response.Response("Registered!")
    return rest_exceptions.AuthenticationFailed("Invalid credentials!")


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def logoutView(request):
    try:
        refreshToken = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        token = tokens.RefreshToken(refreshToken)
        token.blacklist()

        res = Response()
        res.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        res.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        res.delete_cookie("X-CSRFToken")
        res.delete_cookie("csrftoken")
        res["X-CSRFToken"] = None

        return res
    except:
        raise rest_exceptions.ParseError("Invalid token")


class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh")
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            raise jwt_exceptions.InvalidToken(
                "No valid token found in cookie 'refresh'"
            )


class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                value=response.data["refresh"],
                expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )

            del response.data["refresh"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")

        return super().finalize_response(request, response, *args, **kwargs)


@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def user(request):
    try:
        user = models.UserAccount.objects.get(id=request.user.id)
    except models.UserAccount.DoesNotExist:
        return Response(status_code=404)

    serializer = user_serializers.UserAccountSerializer(user)
    return Response(serializer.data)


class UserInfoPost(APIView):
    @swagger_auto_schema(
        request_body=user_serializers.ReportSerializer, #TODO: create report serializer and use it
        operation_description="POST user_info email",
    )
    def post(self, request):
        serializer = user_serializers.UserInfoSerializer(request.data)
        email = serializer.data.get("email")
        user_info = serializer.data.get("user_info")

        try:
            user = UserAccount.objects.get(email=email)
        except UserAccount.DoesNotExist:
            return Response(status=rest_status.HTTP_404_NOT_FOUND)
        except DatabaseError as db_error:
            return Response(status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

        # formatted_user_info = json.dumps(user_info)
        user.user_info = user_info
        user.save()

        return Response(status=rest_status.HTTP_200_OK)


# class UserScoreAPIView(APIView):
#     def get(self, request, username):
#         user = (
#             models.UserAccount.objects.filter(email=username)
#             .only("email", "user_info")
#             .first()
#         )
#         tehsil_score = get_education_score(user)
#         experience_score = 1
#         skills_score = 1
#         language_score = 1
#         programming_skills_score = 1
#         sports_score = 1

#         for stage in user.user_info:
#             if stage["name"] == "is-tecrubesi-substage":
#                 experience_score = get_experience_score(stage)

#             if stage["name"] == "xususi-bacariqlar-substage":
#                 skills_score = get_skills_score(stage)

#             if stage["name"] == "dil-bilikleri-substage":
#                 language_score = get_language_score(stage)

#             if stage["name"] == "proqram-bilikleri-substage":
#                 programming_skills_score = get_programming_skills_score(stage)

#             if stage["name"] == "idman-substage":
#                 sports_score = get_sport_skills_score(stage)
        
#         return Response(
#             {
#                 "user_info": user.user_info,
#                 "special_skills_weight": skills_score,
#                 "language_score": language_score,
#                 "experience_score": experience_score,
#                 "tehsil_score": tehsil_score,
#                 "programming_skills_score": programming_skills_score,
#                 "sports_score": sports_score,
#             }
#         )


# class UserScoreAPIView(AsyncAPIView):

#     async def get(self, request, username):
#         user = await sync_to_async(models.UserAccount.objects.filter(username=username).only("username", "user_info").first)()
#         tehsil_score = await get_education_score(user)
#         skills_score = await get_skills_score(user)
#         language_score = await get_language_score(user)
#         experience_score = await get_experience_score(user)
#         return response.Response({"special_skills_weight":skills_score, "language_score":language_score,
#                                    "tehsil_score":tehsil_score, "experience_score":experience_score})




class UserFilesAPIView(APIView):
    # parser_classes = (MultiPartParser,)
    
    def post(self, request, *args, **kwargs):
        serializer = user_serializers.UserVerificationFileUploadSerializer(data=request.data, many=True)
        
        if serializer.is_valid():
            uploaded_data = serializer.validated_data
            print(uploaded_data)
        #     try:
        #         user = UserAccount.objects.get(email='tami@mail.ru')  # Retrieve the user
        #     except UserAccount.DoesNotExist:
        #         return Response({'message': 'User not found'})

        #     for data in uploaded_data:
        #         category = data['category']
        #         uploaded_files = data['files']

        #         for uploaded_file in uploaded_files:
        #             models.UserVerificationFile.objects.create(user=user, category=category, file=uploaded_file)

        #     return Response({'message': 'Files uploaded successfully'})
        # else:
        #     return Response(serializer.errors)
        return Response({'message': 'Files uploaded successfully'})

