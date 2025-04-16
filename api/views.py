from rest_framework import viewsets, filters
from rest_framework.filters import SearchFilter
from django.template.loader import render_to_string
from .serializers import *
from multimedia.models import *
from multimedia.serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from members.serializers import *
import logging, base64, requests
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from .filter import *
from django.views.decorators.vary import vary_on_cookie
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from .custom_permision import *
from django.utils.decorators import method_decorator
from .pagination import *
from django_filters.rest_framework import DjangoFilterBackend
class VideoDetailsAPIView(viewsets.ModelViewSet):
    serializer_class = VideoUploadSerializer
    queryset = VideoUpload.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = VideoUploadFilter
    pagination_class = CustomPagination
    ordering_fields = ['title', 'price', 'date_uploaded', 'popular']
    @method_decorator(cache_page(60 * 60, key_prefix="videosupload"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
       
        return super().get_queryset()

    # permission_classes = [AuthorizedAccess]

class GenreAPIView(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    @method_decorator(cache_page(60 * 60, key_prefix="genre"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
       
        return super().get_queryset()
    # permission_classes = [AuthorizedAccess]
class GenreTotalAPIView(viewsets.ModelViewSet):
    serializer_class = GenreTotalSerializer
    queryset = Genre.objects.all()
    permission_classes = [AuthorizedAccess]
    @method_decorator(cache_page(60 * 60, key_prefix="genre"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
       
        return super().get_queryset()
class MessageAPIView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    # permission_classes = [AuthorizedAccess]

class PurchasedAPIView(viewsets.ModelViewSet):
    serializer_class = PurchasedSerializer
    queryset = Purchased.objects.all()
    filterset_class = PurchaseFilter
    # permission_classes = [AuthorizedAccess]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['purchase_time']
class DepositHistoryAPIView(viewsets.ModelViewSet):
    # permission_classes = [AuthorizedAccess]
    serializer_class = DepositHistorySerializer
    # http_method_names = ["get", "head", "option"]
    queryset = DepositHistory.objects.all()
    filterset_class = DepositFilter
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['time']
class ReviewAPIView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    # permission_classes = [AuthorizedAccess]
    @method_decorator(cache_page(60 * 60, key_prefix="review"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
       
        return super().get_queryset()

class ProfileAPIView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    # permission_classes = [AuthorizedAccess]
    @method_decorator(cache_page(60 * 60, key_prefix="profile"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
       
        return super().get_queryset()
        return super().get_queryset()
class ErrorsAPIView(viewsets.ModelViewSet):
    serializer_class = ErrosSerializer
    queryset = Error.objects.all()
    permission_classes = [AuthorizedAccess]
class UserRegistrationAPIView(GenericAPIView):
    # permission_classes = [AuthorizedAccess]
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {
            "refresh": str(token),
            'access': str(token.access_token)
        }
        return Response(data, status=status.HTTP_201_CREATED)
class UserLoginAPIView(GenericAPIView):
    # permission_classes = [AuthorizedAccess]
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data

        serializer = MembersSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {
            "refresh": str(token),
            'access': str(token.access_token)
        }
        return Response(data, status=status.HTTP_200_OK)
logger = logging.getLogger(__name__)
class UserLogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logger.debug(request.data)
        try: 
            refresh_token = request.data
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Logout Error: {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserInfoAPIView(RetrieveAPIView):
    serializer_class = MembersSerializer
    def get_object(self):
        return self.request.user
class MembersAPIView(viewsets.ModelViewSet):
    # permission_classes = [AuthorizedAccess]
    serializer_class = MembersSerializer
    queryset = Member.objects.all()
    @method_decorator(cache_page(60 * 60, key_prefix="members"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
       
        return super().get_queryset()

class NotificationAPIView(viewsets.ModelViewSet):
    # permission_classes = [AuthorizedAccess]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = 'date_notified'
    @method_decorator(cache_page(60 * 60, key_prefix="notifications"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
       
        return super().get_queryset()

@api_view(['POST'])
def deposit(request):
        permission_classes = [AuthorizedAccess]
        if request.method == "POST":
            username = request.data["username"]
            Amount = int(request.data["amount"])
            number = str(request.data["phone_number"])
            phoneNumber = "254" + number[1:]
            # Your API username and password
            api_username = "7v1lCadGn6V2AstOB8LD"
            api_password = "CHKjuI9dQdRWgMXAof7ip4rMIkopntZrT3G0zgRc"
            # Concatenating username and password with colon
            credentials = f'{api_username}:{api_password}'
            # Base64 encode the credentials
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            # Creating the Basic Auth token
            basic_auth_token = f'Basic {encoded_credentials}'
            # Output the token
            # print(basic_auth_token)
            url = 'https://backend.payhero.co.ke/api/v2/payments'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': basic_auth_token
            }
            logger.info("sending data")
            data = {
                "amount": Amount,
                "phone_number": phoneNumber,
                "channel_id": 1786,
                "provider": "m-pesa",
                "external_reference": "INV-009",
                "callback_url":"https://smooth-vast-thrush.ngrok-free.app/stk/"
            }
            response = requests.post(url, json=data, headers=headers).json()
            if response["success"]:
                payments = Paying.objects.filter(phone_number = phoneNumber)
                if payments.exists():
                    for paiz in payments:
                        paiz.delete()
                print(username)
                Paying.objects.get_or_create(
                    username = username,
                    phone_number = phoneNumber
                )
            # print(response)
            return Response(response, status=200)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = [AuthorizedAccess]
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = Member.objects.get(email=serializer.validated_data['email'])
            # Create JWT token
            token = AccessToken.for_user(user)
            plain_text =" password_reset_email.txt"
            html_content = render_to_string('password_reset_email.html', {"token":token})
            # Send email
            subject = 'Password Reset Request'
            send_mail(
                subject,
                message=plain_text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                html_message=html_content,
                fail_silently=False,
            )
            return Response({"message": "Reset link sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AuthorizedAccess]
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
