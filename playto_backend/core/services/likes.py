from django.db import transaction
from core.models import Like, KarmaTransaction

@transaction.atomic
def like_post(user, post):
    Like.objects.create(user=user, post=post)
    KarmaTransaction.objects.create(user=post.author, points=5)

@transaction.atomic
def like_comment(user, comment):
    Like.objects.create(user=user, comment=comment)
    KarmaTransaction.objects.create(user=comment.author, points=1)
