from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from . import views

route = DefaultRouter()


route.register("videoDetails", views.VideoDetailsAPIView, basename="video_details")
route.register("genre", views.GenreAPIView, basename="genre")
route.register("review", views.ReviewAPIView, basename="review")
route.register("purchased", views.PurchasedAPIView, basename="purchased")
route.register("deposit_history", views.DepositHistoryAPIView, basename="DepositHistory")
route.register("profile", views.ProfileAPIView, basename="profile")
route.register("members", views.MembersAPIView, basename="members")
route.register("message", views.MessageAPIView, basename="message")
route.register("notification", views.NotificationAPIView, basename="notification")
route.register("errors", views.ErrorsAPIView, basename="errors")
route.register("genretotal", views.GenreTotalAPIView, basename="genre_total")
route.register("dj", views.DjAPIView, basename="dj")
route.register("ceo", views.CeoAPIView, basename="ceo")
route.register("about_team", views.AboutTeamAPIView, basename="about_team")
route.register("dj_Total", views.DjTotalAPIView, basename="dj_total")

urlpatterns = [
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('deposit/', views.deposit, name='deposit'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('password_reset/request/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password_reset/reset/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("info/", views.UserInfoAPIView.as_view(), name="user-info"),
    path("", include(route.urls))
]
