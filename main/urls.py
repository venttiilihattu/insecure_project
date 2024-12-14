from django.urls import path
from .views import user_notes, signup, sensitive_view, search_posts, protected_page

urlpatterns = [
    path('notes/<int:user_id>/', user_notes, name='user_notes'),
    path('signup/', signup, name='signup'),
    path('sensitive/', sensitive_view, name='sensitive_view'),
    path('search/', search_posts, name='search_posts'),
    path('protected/', protected_page, name='protected_page'),
]
