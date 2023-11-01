from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from posts.models import Post
from posts.forms import CommentForm

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

class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()  
        comment_form = CommentForm()
        return render(request, "post_detail.html", {
            "post": post,
            "comments": comments,
            "comment_form": comment_form
        })

    def post(self, request, pk):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = get_object_or_404(Post, pk=pk)  
            comment.author = request.user  
            comment.save()
            return redirect('post_detail', pk=pk)
        else:
            post = get_object_or_404(Post, pk=pk)
            comments = post.comments.all()
            return render(request, "post_detail.html", {
                "post": post,
                "comments": comments,
                "comment_form": comment_form
            })
