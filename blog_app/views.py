# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, PostCreationForm, CommentForm
from .models import User, Post, Category, Like, Comment, Notification, ChatMessage, ChatRoom
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import get_user_model




# Create your views here. 







# def index(request):
#     search_query = request.GET.get('search', '')
#     if search_query:
#         # Adjust the search to include the category name
#         posts = Post.objects.filter(
#             Q(title__icontains=search_query) |
#             Q(content__icontains=search_query) |
#             Q(author__username__icontains=search_query) |
#             Q(category__name__icontains=search_query)  # Search by category name
#         ).order_by('-created_at')
#     else:
#         posts = Post.objects.all().order_by('-created_at')
#         # posts = Post.objects.all().select_related('author').order_by('-created_at')

#     # Check likes and create comment forms for each post
#     for post in posts:
#         post.has_liked = request.user.is_authenticated and post.likes.filter(user=request.user).exists()
#         post.total_likes = post.likes.count()
#         post.comment_form = CommentForm()
        
#     for post in posts:
#         print("PROFILE IMGAE IS:", post.author.profile_image)


#     return render(request, 'blog_app/index.html', {'posts': posts})


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        # Filter posts based on the search query
        posts = Post.objects.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(category__name__icontains=search_query)
        ).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    # Paginate the posts (5 per page)
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page = request.GET.get('page')  # Get the current page number from the query parameter

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # If page is not an integer, display the first page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # If page is out of range, show the last page
        
        
    # Fetch the top 5 recent posts for the right sidebar
    recent_posts = Post.objects.order_by('-created_at')[:8]
    
     # Add the page number for each recent post
    recent_posts_with_pages = []
    for post in recent_posts:
        page_number = get_post_page(post)
        recent_posts_with_pages.append({'post': post, 'page': page_number})

    # Check likes and create comment forms for each post
    for post in posts:
        post.has_liked = request.user.is_authenticated and post.likes.filter(user=request.user).exists()
        post.total_likes = post.likes.count()
        post.comment_form = CommentForm()

    # Optional: Print profile image (for debugging)
    for post in posts:
        print("PROFILE IMAGE IS:", post.author.profile_image)

    # Pass the paginated posts to the template
    return render(request, 'blog_app/index.html', {'posts': posts, 'recent_posts': recent_posts_with_pages,})






def get_post_page(post, posts_per_page=5):
    all_posts = Post.objects.order_by('-created_at')
    post_index = list(all_posts).index(post)  # Find the index of the post in the full list
    page_number = (post_index // posts_per_page) + 1  # Calculate the page number
    return page_number



# def search_view(request):
#     search_query = request.GET.get('q', '').strip()  # Get the search term
#     posts = []
#     users = []

#     if search_query:
#         # Search for posts matching the query
#         posts = Post.objects.filter(
#             Q(title__icontains=search_query) |
#             Q(content__icontains=search_query) |
#             Q(category__name__icontains=search_query)
#         )

#         # Search for users matching the query
#         users = get_user_model().objects.filter(
#             Q(username__icontains=search_query)
#         )

#     return render(request, 'blog_app/search_results.html', {
#         'search_query': search_query,
#         'posts': posts,
#         'users': users,
#     })


def search_view(request):
    search_query = request.GET.get('q', '')  # Get the search term from the URL
    search_results = []

    if search_query:
        search_results = Post.objects.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) | 
            Q(category__name__icontains=search_query)
        )
    
    return render(request, 'blog_app/search_results.html', {
        'search_results': search_results,
        'search_query': search_query,
    })



# User Registration View

# User Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        # Check if passwords match
        if password != confirmation:
            messages.error(request, 'Passwords must match.')
            return render(request, 'blog_app/register.html', {
                'username': username,
                'email': email
            })

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'blog_app/register.html', {
                'username': username,
                'email': email
            })

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return render(request, 'blog_app/register.html', {
                'username': username,
                'email': email
            })

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Log the user in and redirect to profile page
        login(request, user)
        messages.success(request, 'Registration successful! Welcome to your profile.')
        return redirect('profile_update')  # Redirect to the profile page or any other page you want

    return render(request, 'blog_app/register.html')



# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirmation = request.POST['confirmation']

#         # Check if passwords match
#         if password != confirmation:
#             messages.error(request, 'Passwords must match.')
#             return render(request, 'blog_app/register.html')

#         # Check if the user already exists
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Username already taken.')
#             return render(request, 'blog_app/register.html')

#         if User.objects.filter(email=email).exists():
#             messages.error(request, 'Email is already in use.')
#             return render(request, 'blog_app/register.html')

#         # Create the user
#         user = User.objects.create_user(username=username, email=email, password=password)

#         # Log the user in and redirect to profile page
#         login(request, user)
#         messages.success(request, 'Registration successful! Welcome to your profile.')
#         return redirect('profile')  # Redirect to the profile page or any other page you want

#     return render(request, 'blog_app/register.html')


# User Login View
# User Login View
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('index')  # Redirect to the home page after login
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'blog_app/login.html')
    else:
        return render(request, 'blog_app/login.html')


# User Logout View
def logout_user(request):
    logout(request)  # Log the user out
    messages.success(request, "You have been logged out successfully.")  
    return redirect('login')  # Redirect to the login page after logout

# User Profile View (must be logged in to access)
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'blog_app/profile.html', {'form': form})


# View to create a new post


@login_required
def create_post(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST['category']
        
        # Use `.get()` to safely retrieve `media_type` (returns None if not present)
        media_type = request.POST.get('media_type')  

        # Get the selected category
        category = Category.objects.get(id=category_id)

        # Handle the uploaded image or video
        media_file = None
        if media_type == 'image':
            media_file = request.FILES.get('image')  # If image is selected
        elif media_type == 'video':
            media_file = request.FILES.get('video')  # If video is selected

        # Create the post
        post = Post(
            title=title,
            content=content,
            category=category,
            author=request.user,
            media_type=media_type,
            media_file=media_file,
        )
        post.save()

        # Prevent multiple submissions
        messages.success(request, "Your post has been created successfully!")
        return redirect('index')  # Redirect to another page after post creation (e.g., 'home')

    return render(request, 'blog_app/create_post.html', {
        'categories': categories
    })


# @login_required
# def create_post(request):
#     categories = Category.objects.all()

#     if request.method == 'POST':
#         title = request.POST['title']
#         content = request.POST['content']
#         category_id = request.POST['category']
#         media_type = request.POST['media_type']

#         # Get the selected category
#         category = Category.objects.get(id=category_id)

#         # Handle the uploaded image or video
#         media_file = None
#         if media_type == 'image':
#             media_file = request.FILES.get('image')  # If image is selected
#         elif media_type == 'video':
#             media_file = request.FILES.get('video')  # If video is selected

#         # Create the post
#         post = Post(
#             title=title,
#             content=content,
#             category=category,
#             author=request.user,
#             media_type=media_type,
#             media_file=media_file,
#         )
#         post.save()

#         # Prevent multiple submissions
#         messages.success(request, "Your post has been created successfully!")
#         return redirect('index')  # Redirect to another page after post creation (e.g., 'home')

#     return render(request, 'blog_app/create_post.html', {
#         'categories': categories
#     })


# @login_required
def update_post(request, post_id):
    # Get the post to update
    post = get_object_or_404(Post, id=post_id)
    
    # Get all categories to display in the dropdown
    categories = Category.objects.all()

    # Handle form submission if it's a POST request
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        media_type = request.POST.get('media_type')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        # Update the post object
        post.title = title
        post.content = content
        post.category_id = category_id
        post.media_type = media_type
        
        # If a new media file is uploaded, update the post's media file
        if media_type == 'image' and image:
            post.media_file = image
        elif media_type == 'video' and video:
            post.media_file = video
        
        post.save()

        # Flash a success message
        messages.success(request, 'Post updated successfully!')

        # Redirect to the post detail page
        return redirect('profile_update', user_id=request.user.id)

    # Pass the categories and the post to the template
    return render(request, 'blog_app/update_post.html', {'post': post, 'categories': categories})



# def update_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     categories = Category.objects.all()

#     if request.method == 'POST':
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         category_id = request.POST.get('category')
#         media_type = request.POST.get('media_type')
#         image = request.FILES.get('image')
#         video = request.FILES.get('video')

#         post.title = title
#         post.content = content
#         post.category_id = category_id
#         post.media_type = media_type

#         if media_type == 'image' and image:
#             post.media_file = image
#         elif media_type == 'video' and video:
#             post.media_file = video
        
#         post.save()

#         # Flash a success message if not using AJAX
#         messages.success(request, 'Post updated successfully!')

#         # Return a success response for AJAX requests
#         if request.is_ajax():
#             return JsonResponse({'success': True})

#         # If not AJAX, redirect to the post detail page
#         return redirect('post_detail', post_id=post.id)

#     return render(request, 'blog_app/update_post.html', {'post': post, 'categories': categories})













@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)  # Ensure the post belongs to the logged-in user
    
    # Delete all related comments and likes
    post.comments.all().delete()  # Delete all comments for this post
    post.likes.all().delete()     # Delete all likes for this post
    
    # Delete the post itself
    post.delete()

    messages.success(request, "Your post has been deleted successfully!")
    return redirect('index')  # Redirect to the home page or post list page



@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
            # Create notification for post author (if the commenter isn't the author)
            if request.user != post.author:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    post=post,
                    notification_type='comment',
                    text=f"{request.user.username} commented on your post '{post.title}'"
                )
            
            return JsonResponse({
                'status': 'success',
                'comment_id': comment.id,
                'user': comment.user.username,
                'comment_text': comment.comment_text,
                'created_at': comment.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

    return JsonResponse({'status': 'error'}, status=400)



@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return JsonResponse({'status': 'success', 'comment_id': comment_id})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            comment.comment_text = comment_text
            comment.save()
            return JsonResponse({
                'status': 'success',
                'comment_id': comment_id,
                'comment_text': comment.comment_text
            })
    return JsonResponse({'status': 'error'})





@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        # Unlike the post
        like.delete()
        liked = False
    else:
        liked = True
        # Create notification for post author (if the liker isn't the author)
        if request.user != post.author:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                post=post,
                notification_type='like',
                text=f"{request.user.username} liked your post '{post.title}'"
            )

    return JsonResponse({
        'status': 'success',
        'liked': liked,
        'total_likes': post.likes.count()
    })
    
    
    
# Add this new view to display notifications
@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    
    # Mark all notifications as read
    unread_notifications = user_notifications.filter(is_read=False)
    unread_notifications.update(is_read=True)
    
    return render(request, 'blog_app/notifications.html', {
        'notifications': user_notifications
    })

# Optional: Add this view to get unread notification count
@login_required
def get_notification_count(request):
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'count': count})



@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Get all comments related to the post

    # Handle the comment form submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog_app/post_detail.html', {'post': post, 'comments': comments, 'form': form})



@login_required
def profile_update(request,  user_id=None):
    if user_id:
        profile_user = get_object_or_404(User, id=user_id)
    else:
        profile_user = request.user

    unread_notifications_count = Notification.objects.filter(recipient=request.user, is_read=False).count()

    # Fetch the user's posts and comments
    user_posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    user_comments = Comment.objects.filter(user=profile_user)

    # Process likes for each post
    for post in user_posts:
        post.has_liked = post.likes.filter(user=request.user).exists()
        post.total_likes = post.likes.count()
        post.comment_form = CommentForm()
    

    # Handle form submission for logged-in user's profile update
    form = None
    if profile_user == request.user:
        if request.method == 'POST':
            form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Your profile has been updated!")
                return redirect('profile_update', user_id=request.user.id)
        else:
            form = UserUpdateForm(instance=request.user)

    # Add a context variable to control button visibility
    is_own_profile = profile_user == request.user

    return render(request, 'blog_app/profile_update.html', {
        'form': form,
        'profile_user': profile_user,
        'user_posts': user_posts,
        'user_comments': user_comments,
        'unread_notifications_count': unread_notifications_count,
        'is_own_profile': is_own_profile  # Pass the context variable
    })




from django.db.models import Max

from django.utils import timezone
import datetime

@login_required
def chat_inbox(request):
    chat_rooms = ChatRoom.objects.filter(participants=request.user)

    # Add unread messages count and latest message to each chat room
    chat_rooms_with_unread = []
    for chat_room in chat_rooms:
        # Fetch the last message in the chat room (most recent)
        last_message = ChatMessage.objects.filter(room=chat_room).order_by('-created_at').first()
        
        # Count unread messages excluding the ones sent by the current user
        unread_count = ChatMessage.objects.filter(
            room=chat_room,
            is_read=False
        ).exclude(sender=request.user).count()

        chat_rooms_with_unread.append({
            "chat_room": chat_room,
            "unread_count": unread_count,
            "last_message": last_message  # Add the last message
        })

    # Make sure datetime.datetime.min is timezone-aware
    min_datetime = timezone.make_aware(datetime.datetime.min, timezone.get_current_timezone())

    # Sort the chat rooms by the timestamp of the latest message, but handle None values
    chat_rooms_with_unread.sort(
        key=lambda x: x['last_message'].created_at if x['last_message'] else min_datetime, 
        reverse=True
    )

    return render(request, 'blog_app/chat_inbox.html', {
        'chat_rooms_with_unread': chat_rooms_with_unread,
    })





@login_required
def start_chat(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    existing_room = ChatRoom.objects.filter(participants=request.user).filter(participants=recipient).first()

    if existing_room:
        return redirect('chat_room', room_id=existing_room.id)

    chat_room = ChatRoom.objects.create()
    chat_room.participants.add(request.user, recipient)
    return redirect('chat_room', room_id=chat_room.id)




@login_required
def chat_room(request, room_id):
    # Fetch the chat room and ensure the user is a participant
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in chat_room.participants.all():
        return redirect('chat_inbox')

    if request.method == 'POST':
        # Handle new message creation
        content = request.POST.get('content')
        if content:
            ChatMessage.objects.create(
                room=chat_room,
                sender=request.user,
                content=content
            )
        return JsonResponse({'success': True})  # Respond dynamically if using JavaScript

    # Mark all messages as read for the current user in this chat room
    ChatMessage.objects.filter(room=chat_room, is_read=False).exclude(sender=request.user).update(is_read=True)

    # Fetch messages and the other participant
    chat_messages = chat_room.messages.order_by('created_at')  # Ensures messages are ordered correctly
    other_participant = chat_room.participants.exclude(id=request.user.id).first()

    return render(request, 'blog_app/chat_room.html', {
        'chat_room': chat_room,
        'chat_messages': chat_messages,
        'other_participant': other_participant
    })




# @login_required
# def get_unread_messages_count(request):
#     count = ChatMessage.objects.filter(
#         room__participants=request.user
#     ).exclude(sender=request.user).filter(is_read=False).count()
#     return JsonResponse({'count': count})

@login_required
def get_unread_messages_count(request):
    # Count unread messages
    count = ChatMessage.objects.filter(
        room__participants=request.user
    ).exclude(sender=request.user).filter(is_read=False).count()
    
    # You can also send the count in the context so that it can be rendered in the template
    return JsonResponse({'count': count})




@login_required
def user_list(request):
    search_query = request.GET.get('search', '')
    
    # Fetch users excluding the current user
    users = get_user_model().objects.exclude(id=request.user.id)
    
    # If a search query is provided, filter users by name (username)
    if search_query:
        users = users.filter(Q(username__icontains=search_query))
    
    return render(request, 'blog_app/user_list.html', {'users': users})





from django.utils.timezone import now
from django.http import JsonResponse
import json

# Functionn To dynamic fetching of the General Notification New messages To the JAVASCRIPT 
@login_required
def fetch_new_messages(request, room_id):
    if request.method == "GET":
        chat_room = get_object_or_404(ChatRoom, id=room_id)
        if request.user not in chat_room.participants.all():
            return JsonResponse({'error': 'Unauthorized access'}, status=403)

        last_check = request.GET.get('last_check')
        if last_check:
            last_check = json.loads(last_check)

        # Fetch messages created after the last_check timestamp
        new_messages = ChatMessage.objects.filter(
            room=chat_room,
            created_at__gte=last_check,
        ).exclude(sender=request.user)

        message_data = [
            {
                "sender": message.sender.username,
                "content": message.content,
                "created_at": message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for message in new_messages
        ]

        return JsonResponse({'new_messages': message_data})
    
    
    
   
#    Function To Fetch Unread Message Counts Per User To the JAVASCRIPT 
@login_required
def fetch_unread_counts(request):
    chat_rooms = ChatRoom.objects.filter(participants=request.user)
    counts = []
    for chat_room in chat_rooms:
        unread_count = ChatMessage.objects.filter(
            room=chat_room,
            is_read=False
        ).exclude(sender=request.user).count()
        counts.append({
            "chat_room_id": chat_room.id,
            "unread_count": unread_count,
        })
    return JsonResponse({'counts': counts})

    
