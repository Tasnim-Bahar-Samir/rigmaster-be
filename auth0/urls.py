from django.urls import path, include

# auth
urlpatterns = [  
    path('', include('dj_rest_auth.urls')),
    # path('login1/', views.CustomLoginView.as_view()),
]