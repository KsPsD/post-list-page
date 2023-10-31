from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View


def post_list(request):
    return render(request, "post_list.html")


from posts.forms import PostForm


class PostCreateView(View):
    def get(self, request):
        form = PostForm()
        return render(request, "post_create.html", {"form": form})

    # NOTE: 인증 관련 기능 구현하지 말라는 제한이 있어서 로그인을 아예 구현안함. 그래서 무조건 슈퍼유저로 작성됨.
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            superuser = User.objects.filter(is_superuser=True).first()
            if superuser:
                post.author = superuser
            else:
                assert False, "Superuser가 없습니다. createsuperuser 명령어를 실행해주세요."
            post.save()
            return redirect("post_list")
        else:
            return render(request, "post_create.html", {"form": form})
