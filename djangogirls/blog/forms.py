#장고 form 양식을 사용하기 위해 forms 호출
from django import forms
#Post 모델에 자료를 보내줄 것
from .models import Post
#Post에 대한 Form 클래스이므로 이름은 PostForm으로 설정
#forms.ModelForm을 괄호 사이에 집어 넣어야 form 구현 가능
class PostForm(forms.ModelForm):
    #PostForm 내부에 meta라는 이름으로 작성할 경우
    #타겟 모델은 model = 모델이름 형식으로
    #사용자에게 입력받을 부분은 fields = ('1번컬럼', '2번컬럼' ....)
    #형식으로 작성할 수 있다.
    class Meta:
        model = Post #Post모델을 타겟으로 설정 
        fields = ('title', 'text',) #Post 모델에서 title과 text 칼럼에 자료를 입력하겠다