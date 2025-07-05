from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profiles
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    
    # Posts
    path('create-post/', views.create_post, name='create_post'),
    path('update-post/<int:post_id>/', views.update_post, name='update_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('add-comment/<int:post_id>/', views.add_comment, name='add_comment'),
    
    # Friend Requests
    path('send-friend-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject-friend-request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('friend-requests/', views.friend_requests, name='friend_requests'),
    
    # Messaging
    path('messages/', views.messages_view, name='messages'),
    path('conversation/<int:user_id>/', views.conversation_view, name='conversation'),
    
    # Search
    path('search/', views.search_users, name='search'),
] 