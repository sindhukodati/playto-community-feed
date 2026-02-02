from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum
from core.models import KarmaTransaction

def get_leaderboard():
    last_24h = now() - timedelta(hours=24)

    return (
        KarmaTransaction.objects
        .filter(created_at__gte=last_24h)
        .values("user__username")
        .annotate(total_karma=Sum("points"))
        .order_by("-total_karma")[:5]
    )
