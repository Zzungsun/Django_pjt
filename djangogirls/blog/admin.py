from django.contrib import admin
from .models import Post

#admin.site.register(모델명) 을 입력할 경우 admin페이지에서 수정 가능!
admin.site.register(Post)
