from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Profile, Post, Like, Comment, FriendRequest, Message
from .forms import PostForm, CommentForm, ProfileForm
import json

def home(request):
    """Home page - shows all posts from all users"""
    posts = Post.objects.all().order_by('-post_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj,
    }
    return render(request, 'Social_media/home.html', context)

def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile for new user
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'Social_media/register.html', {'form': form})

def login_view(request):
    """User login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'Social_media/login.html', {'form': form})

@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile_view(request, username):
    """User profile view"""
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-post_date')
    
    # Check if current user has sent friend request
    friend_request = None
    if request.user != user:
        friend_request = FriendRequest.objects.filter(
            sender=request.user, 
            receiver=user
        ).first()
    
    context = {
        'profile_user': user,
        'posts': posts,
        'friend_request': friend_request,
    }
    return render(request, 'Social_media/profile.html', context)

@login_required
def edit_profile(request):
    """Edit user profile"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'Social_media/edit_profile.html', {'form': form})

@login_required
def create_post(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostForm()
    
    return render(request, 'Social_media/create.html', {'form': form})

@login_required
def like_post(request, post_id):
    """Like/unlike a post"""
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        # User already liked the post, so unlike it
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'like_count': post.like_count
    })

@login_required
def add_comment(request, post_id):
    """Add a comment to a post"""
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('home')
    else:
        form = CommentForm()
    
    return render(request, 'Social_media/add_comment.html', {'form': form, 'post': post})

@login_required
def send_friend_request(request, user_id):
    """Send a friend request"""
    receiver = get_object_or_404(User, id=user_id)
    
    if request.user == receiver:
        messages.error(request, 'You cannot send a friend request to yourself!')
        return redirect('profile', username=receiver.username)
    
    # Check if friend request already exists
    friend_request, created = FriendRequest.objects.get_or_create(
        sender=request.user,
        receiver=receiver,
        defaults={'status': 'pending'}
    )
    
    if created:
        messages.success(request, f'Friend request sent to {receiver.username}!')
    else:
        messages.info(request, f'Friend request already sent to {receiver.username}.')
    
    return redirect('profile', username=receiver.username)

@login_required
def accept_friend_request(request, request_id):
    """Accept a friend request"""
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    friend_request.status = 'accepted'
    friend_request.save()
    messages.success(request, f'Friend request from {friend_request.sender.username} accepted!')
    return redirect('friend_requests')

@login_required
def reject_friend_request(request, request_id):
    """Reject a friend request"""
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    friend_request.status = 'rejected'
    friend_request.save()
    messages.info(request, f'Friend request from {friend_request.sender.username} rejected.')
    return redirect('friend_requests')

@login_required
def friend_requests(request):
    """View friend requests"""
    received_requests = FriendRequest.objects.filter(receiver=request.user, status='pending')
    sent_requests = FriendRequest.objects.filter(sender=request.user, status='pending')
    
    context = {
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    }
    return render(request, 'Social_media/friend_requests.html', context)

@login_required
def messages_view(request):
    """View messages"""
    # Get all conversations for the current user
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).values('sender', 'receiver').distinct()
    
    # Get unique users the current user has messaged with
    users = set()
    for conv in conversations:
        if conv['sender'] == request.user.id:
            users.add(conv['receiver'])
        else:
            users.add(conv['sender'])
    
    context = {
        'users': User.objects.filter(id__in=users),
    }
    return render(request, 'Social_media/messages.html', context)

@login_required
def conversation_view(request, user_id):
    """View conversation with a specific user"""
    other_user = get_object_or_404(User, id=user_id)
    
    # Get all messages between the two users
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('sent_date')
    
    # Mark messages as seen
    Message.objects.filter(sender=other_user, receiver=request.user, message_seen=False).update(message_seen=True)
    
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                message=message_text
            )
            return redirect('conversation', user_id=user_id)
    
    context = {
        'other_user': other_user,
        'messages': messages,
    }
    return render(request, 'Social_media/conversation.html', context)

@login_required
def search_users(request):
    """Search for users"""
    query = request.GET.get('q', '')
    users = []
    
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)
    
    context = {
        'users': users,
        'query': query,
    }
    return render(request, 'Social_media/search.html', context)

@login_required
def update_post(request, post_id):
    """Update a post"""
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('home')
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'Social_media/update.html', context)

@login_required
def delete_post(request, post_id):
    """Delete a post"""
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == 'POST':
        if request.POST.get('confirm_delete'):
            post.delete()
            messages.success(request, 'Post deleted successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please confirm the deletion.')
    
    context = {
        'post': post,
    }
    return render(request, 'Social_media/delete.html', context)
