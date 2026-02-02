# EXPLAINER — Playto Community Feed

This document explains the key technical decisions made while building the **Playto Community Feed** backend, with a focus on data modeling, performance, and correctness.

---

## 🌳 The Tree — Nested Comments Design

### How comments are modeled

Nested comments are implemented using a **self-referencing foreign key** on the `Comment` model.

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE
    )
    content = models.TextField()
```
### Comment Hierarchy Rules

- A top-level comment has `parent = NULL`
- A reply points to another `Comment` as its parent
- This allows unlimited depth (Reddit-style threads)

---

### How the Tree Is Serialized Efficiently (No N+1)

All comments for a post are fetched in **a single database query**, then assembled into a tree **in memory**.

```python
comments = Comment.objects.select_related("author").filter(post=post)
```
An in-memory mapping (`{comment_id → node}`) is used to attach replies to their parent comments.

This avoids:
- Recursive database queries
- N+1 query problems for deeply nested threads

---

## 🧮 The Math — Leaderboard (Last 24 Hours)

### Why Karma Is Not Stored on the User Model

Storing “daily karma” as a field on the `User` model can lead to:
- Data inconsistency
- Race conditions
- Incorrect historical calculations

Instead, **all karma is derived from immutable transaction history**.

---

### Karma Rules

- Like on a **post** → `+5` karma  
- Like on a **comment** → `+1` karma  

Each like creates a `KarmaTransaction` record.

---

### Leaderboard Query (Last 24h)

```python
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum

since = now() - timedelta(hours=24)

leaderboard = (
    KarmaTransaction.objects
    .filter(created_at__gte=since)
    .values("user__username")
    .annotate(total_karma=Sum("points"))
    .order_by("-total_karma")[:5]
)
```
This ensures:
- Only last 24-hour activity is counted
- No cached or stale data
- Accurate real-time leaderboard results

---

## 🔒 Concurrency — Preventing Double Likes

### The Problem

Without safeguards, users could:
- Like the same post or comment multiple times
- Inflate karma via race conditions

---

### The Solution

Database-level **unique constraints** enforce correctness.

```python
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_post_like"),
            models.UniqueConstraint(fields=["user", "comment"], name="unique_comment_like"),
        ]
```
This guarantees:
- One like per user per object
- Safety even under concurrent requests

---

## 🤖 The AI Audit

### AI-Generated Issue

An AI-generated implementation attempted to:
- Store daily karma directly on the `User` model
- Update it during like events

This approach was flawed because:
- It breaks historical accuracy
- It introduces race conditions
- It makes “last 24 hours” calculations unreliable

---

### How It Was Fixed

The solution was redesigned to:
- Record karma as **immutable transactions**
- Compute aggregates dynamically using database queries

This approach is:
- Safer
- More scalable
- Easier to reason about and debug

---

## ✅ Final Notes

This project prioritizes:
- Correctness over shortcuts
- Database-level guarantees
- Clear, explainable architecture

All design choices were made with **performance, integrity, and clarity** in mind.
