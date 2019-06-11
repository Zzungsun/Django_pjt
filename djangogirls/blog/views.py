from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse
from .models import Post
from django.utils import timezone
from .forms import PostForm

#쉘에서 사용 가능한 명령어 => 뷰에서도 사용가능
# Create your views here.
def post_list(request):
    #HttpResponse는 print() 구문처럼 내부에 적은 문자열을 화면에 출력한다.
    #단, HttpResponse는 콘솔창에 출력하지 않고, 웹 페이지에 출력해준다.
    #return HttpResponse('post_list 준비중')
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    #render함수는 바로 템플릿 파일을 지정해서 사용할 수있다.
    return render(request, 'blog/post_list.html',{'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

def post_new(request):
    #요청 방식이 POST인지 검증한다.
    if request.method == "POST" :
        #PostForm 양식을 받아오되 POST 방식으로 전달된 데이터를 채워넣는다.
        #이렇게 되면 title, text, created_date 세 개의 컬럼에 자료가 채워진다
        #단, 아직 author, published_date 컬럼에는 자료가 채워지지 않음
        form = PostForm(request.POST)
        #들어온 자료가 올바른 자료인지 is_valid() 함수로 검사한다.
        #자료가 올바른(폼을 통해 전달된 자료)라면 is_vaild()는 True값을 갖는다
        if form.is_valid():
            #나머지 2개 컬럼에 대해서도 자료를 모두 저장하기 위해서
            #먼저 현재 들어와 있는 3개 자료에 대해서 임시저장을 한다.
            #commit=False로 save() 함수를 실행하면 임시저장 상태.
            post = form.save(commit=False)
            #author 컬럼에는 요청한 유저를 집어넣는다.
            post.author = request.user
            #published_date 컬럼에는 현재 시간을 집어넣는다.
            post.published_date = timezone.now()
            #모자란 2개 컬럼을 다 채웠기 때문에 DB에 완전 저장
            post.save()
            #자료 입력이 끝났다면 올린 글을 확인할 수 있도록 상세페이지로 이동.
            #redirect 함수는 별도로 호출해야함.(django.shortcuts에서 import)
            #redirect의 'post_detail'은 urls.py의 post_detail의 url패턴임
            return redirect('post_detail', pk=post.pk)
    else:
        #form 양식을 작성할 경우에는 forms.py 내부의 자료를 form 이라는 변수에 저장 받는다.
        #유효한 자료가 검증되지 않는다면 form을 다시 비운다.
        form = PostForm()
        #저장한 form을 render 함수를 이용해 템플릿으로 보내준다.
    return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        #instance는 미리 적혀있던 정보를 폼에 저장
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else :
        #post 방식이 아닌 get 방식인 경우 수정결과 반영이 아닌 수정 창만 보여줌
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})
        

# back-end / front-end // -> full-stack