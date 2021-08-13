from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db.models.deletion import CASCADE

# Create your models here.
class Blog(models.Model):
    latitude = models.FloatField(default=0.0) #위도
    longitude = models.FloatField(default=0.0) #경도
    hashtag = models.TextField(max_length=20) #해시태그는 하나만 적을 수 있도록 하는 게 편할듯
    weather = models.TextField() #4개로 구분 - cloudy, sunny, rainy, snowy
    images = models.ImageField(upload_to ="images", blank = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )#작성자 여기 수정
    created_at = models.DateTimeField(auto_now_add=True) #작성시각
    #pub_date = models.DateTimeField('data published')
    body = models.TextField(max_length=200) #글 본문
    likes = models.ManyToManyField(User, through='Like', through_fields=('blog', 'user'), related_name='likes')
    
    def delete(request, self, *args, **kwargs):
        self.images.delete()
    
    def __str__(self):
        return str(self.latitude) + ", " + str(self.longitude) #일단 위도, 경도 표시하도록 해놓음 ->편의에 따라 바꿔도 ㄱㅊ

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True) # 현 계정의 사용자를 가져올 수 있음.
    nickname = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile/',blank=True)          # 값을 채워넣지 않아도 되는 속성.

class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    body = models.TextField(max_length=200)
    date = models.DateTimeField(default=timezone.now)

class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
