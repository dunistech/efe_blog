# blog_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create_post/', views.create_post, name='create_post'), 
     path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('search/', views.search_view, name='search_view'),
    path('profile/update/<int:user_id>/', views.profile_update, name='profile_update'),
    path('profile/update/', views.profile_update, name='profile_update'),

    
    
    path('notifications/', views.notifications, name='notifications'),
    
        # Add to urls.py
    path('chat/', views.chat_inbox, name='chat_inbox'),
    path('chat/start/<int:recipient_id>/', views.start_chat, name='start_chat'),
    path('chat/room/<int:room_id>/', views.chat_room, name='chat_room'),
    path('chat/unread/', views.get_unread_messages_count, name='get_unread_messages_count'),

    path('users/', views.user_list, name='user_list'),

    
    path('chat/fetch_new_messages/<int:room_id>/', views.fetch_new_messages, name='fetch_new_messages'),
    
    path('chat/fetch_unread_counts/', views.fetch_unread_counts, name='fetch_unread_counts'),
    
    path('post/update/<int:post_id>/', views.update_post, name='update_post'),

    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),





]