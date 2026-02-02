from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.db.models import Count

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .services.leaderboard import get_leaderboard


class FeedView(APIView):
    def get(self, request):
        posts = (
            Post.objects
            .select_related("author")
            .annotate(like_count=Count("like"))   # ✅ CORRECT
            .order_by("-created_at")
        )
        return Response(PostSerializer(posts, many=True).data)


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = (
            Post.objects
            .select_related("author")
            .annotate(like_count=Count("like"))   # ✅ CORRECT
            .order_by("-created_at")
        )
        return Response(PostSerializer(posts, many=True).data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


def build_comment_tree(comments):
    mapping = {}
    roots = []

    for c in comments:
        mapping[c.id] = {
            "id": c.id,
            "author": c.author.username,
            "content": c.content,
            "replies": []
        }

    for c in comments:
        if c.parent_id:
            mapping[c.parent_id]["replies"].append(mapping[c.id])
        else:
            roots.append(mapping[c.id])

    return roots


class LeaderboardView(APIView):
    def get(self, request):
        return Response(get_leaderboard())


@api_view(["GET"])
def home(request):
    return Response({
        "message": "Playto Community Feed API is running 🚀",
        "endpoints": {
            "feed": "/api/feed/",
            "posts": "/api/posts/",
            "leaderboard": "/api/leaderboard/"
        }
    })
