from django.db.models import OuterRef, Prefetch, Subquery
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from ..models import Comment, Post
from ..serializers import CommentSerializer, PostSerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "currentPage": self.page.number,
                "totalPages": self.page.paginator.num_pages,
                "pageSize": self.page_size,
                "count": self.page.paginator.count,
                "results": data,
            }
        )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.none()
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def get_queryset(self):
        latest_comment_subquery = (
            Comment.objects.filter(post=OuterRef("pk"))
            .order_by("-created_at")
            .values("id")[:1]
        )

        queryset = Post.objects.annotate(
            latest_comment_id=Subquery(latest_comment_subquery)
        )

        queryset = queryset.prefetch_related(
            Prefetch(
                "comments",
                queryset=Comment.objects.filter(
                    id__in=queryset.values("latest_comment_id")
                ),
                to_attr="latest_comment_prefetched",
            )
        )

        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
