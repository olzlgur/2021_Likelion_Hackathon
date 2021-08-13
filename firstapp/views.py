from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Blog, Profile
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from .models import Blog, Comment
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm, ProfileForm
from .models import Profile

# Create your views here.

def loading(request):
    return render(request, 'blog/loading.html')

def main(request):
    blogs = Blog.objects.all()
    person = get_object_or_404(get_user_model(), username=request.user)
    return render(request, 'blog/main.html', {'blogs':blogs, 'person':person})

def signup(request):
    return render(request, 'blog/signup.html')

def siteMain(request):
    return render(request, 'siteMain.html')

def detail(request, id):
    blog = get_object_or_404(Blog, pk = id)
    person = get_object_or_404(get_user_model(), username=request.user)
    comments = Comment.objects.filter(post = id)
    if request.method == "POST":
            comment = Comment()
            comment.writer=  request.user
            comment.post = blog
            comment.body = request.POST['body']
            comment.date = timezone.now()
            comment.save()
    
    if blog.likes.filter(id=request.user.id):
        message="취소"
    else:
        message="좋아요"

    return render(request, 'blog/detail.html', {'blog' :blog, 'comments' : comments, 'person':person, "message" : message})

def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    return render(request, 'blog/profile.html', {'person':person}) 

def modify(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
            return redirect('profile', user.username)
        return redirect('profile', request.user)
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        # 새롭게 추가하는 것이 아니라 수정하는 것이기 때문에
        # 기존의 정보를 가져오기 위해 instance를 지정해야 한다.
        profile, create = Profile.objects.get_or_create(user=request.user)
        # Profile 모델은 User 모델과 1:1 매칭이 되어있지만
        # User 모델에 새로운 인스턴스가 생성된다고 해서 그에 매칭되는 Profile 인스턴스가 생성되는 것은 아니기 때문에
        # 매칭되는 Profile 인스턴스가 있다면 그것을 가져오고, 아니면 새로 생성하도록 한다.
        profile_form = ProfileForm(instance=profile)
        return render(request, 'blog/modify.html', {
            'user_change_form': user_change_form,
            'profile_form': profile_form
        })

def test(request):
    return render(request, 'blog/test.html')

def credit(request):
    person = get_object_or_404(get_user_model(), username=request.user)
    return render(request, 'blog/credit.html', {'person':person})

def main_map(request):
    blogss = Blog.objects.all()
    personss = Profile.objects.all()
    personsss = get_object_or_404(get_user_model(), username=request.user)
    context = {
        'blogss': blogss,
        'personss': personss,
        'personsss': personsss
    }
    return render(request, 'blog/map.html', context)

def login(request):
    return render(request, 'blog/login.html')

def new(request):
    return render(request, 'blog/new.html')

def post(request):
    person = get_object_or_404(get_user_model(), username=request.user)
    return render(request, 'blog/post.html', {'person':person})

def create(request):
    post_blog = Blog()
    post_blog.body = request.POST['body']
    post_blog.hashtag = request.POST['hashtag']
    post_blog.created_at = timezone.now()
    post_blog.images = request.FILES['images']
    post_blog.author = request.user #여기도 수정
    post_blog.weather = request.POST.getlist('weather[]')
    post_blog.save()
    return redirect('main')
# if request.method == 'POST':
        

def search(request):
    blog_list = Blog.objects.all()
    person = get_object_or_404(get_user_model(), username=request.user)
    search_key = request.GET.get('search_key') # 검색어 가져오기
    if search_key: # 만약 검색어가 존재하면
        blog_list = blog_list.filter(hashtag__icontains=search_key) # 해당 검색어를 포함한 queryset 가져오기
    return render(request, 'blog/search.html', {'blog_list':blog_list, 'person':person})



def edit(request, id):
    edit_blog = Blog.objects.get(id= id)
    return render(request, 'blog/edit.html', {'blog':edit_blog})


def update(request, id):
    update_blog = Blog.objects.get(id= id)
    update_blog.body = request.POST['body']
    update_blog.hashtag = request.POST['hashtag']
    update_blog.weather = request.POST.getlist('weather[]')
    update_blog.author = request.user
    update_blog.created_at = timezone.now()
    update_blog.save()
    return redirect('detail', update_blog.id)


def delete(request, id):
    delete_blog = Blog.objects.get(id= id)
    delete_blog.delete()
    return redirect('main')    

def post_like(request, id):
    blog = get_object_or_404(Blog, pk=id)
    user = request.user

    if blog.likes.filter(id=user.id):
        blog.likes.remove(user)
    else: 
        blog.likes.add(user)

    return redirect('/detail/'+str(id))

