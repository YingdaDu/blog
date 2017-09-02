from rest_framework import generics
from django.db.models import Q
from rest_framework.views import APIView
from posts.models import Post
from .serializers import PostModelSerializer
from rest_framework.response import Response
from rest_framework import permissions
from .pagination import StandardResultsPagination


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self,  *args, **kwargs):
    	qs = Post.objects.all()
    	query = self.request.GET.get("q", None)
        isfollow = self.request.GET.get("f", None)
        if isfollow == "on":
            im_following = self.request.user.profile.get_following() # none
            qs1 = Post.objects.filter(user__in=im_following)
            qs2 = Post.objects.filter(user=self.request.user)
            qs = qs = (qs1 | qs2).distinct().order_by("-timestamp")

    	if query is not None:
            qs = qs.filter(
                    Q(title__icontains=query)|
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    )

        return qs


class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, slug, format=None):
        post_qs = Post.objects.filter(slug=slug)
        message = "Not allowed"
        if request.user.is_authenticated():
            is_liked = Post.objects.like_toggle(request.user, post_qs.first())
            like_count = post_qs.first().liked.all().count()
            print(like_count)
            return Response({'liked': is_liked, "like_count": like_count})
        return Response({"message": message}, status=400)
