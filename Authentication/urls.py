from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views_dir.Task1 import UserSignUpView, home
from .views_dir.Task2 import complete_sign_up
from .views_dir.Task3 import key_exchange, receive_session_key_from_client, send_projects
from .views_dir.Task4 import send_marks
from .views_dir.Task5 import send_csr, verify_csr, handshake_with_dc


urlpatterns = [
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    path('api/sign-up/', UserSignUpView.as_view(), name='api_signup'),
    path('api/home/', home, name='home'),
    path('api/complete_sign_up/', complete_sign_up, name='complete_sign_up'),
    path('api/key_exchange/', key_exchange, name='key_exchange'),
    path('api/send_session_key_to_server/', receive_session_key_from_client, name='send_session_key_to_server'),
    path('api/send_projects/', send_projects, name='send_projects'),
    path('api/send_marks/', send_marks, name='send_marks'),
    path('api/send_csr/', send_csr, name='send_csr'),
    path('api/verify_csr/', verify_csr, name='verify_csr'),
    path('api/handshake_with_dc/', handshake_with_dc, name='handshake_with_dc'),
]
