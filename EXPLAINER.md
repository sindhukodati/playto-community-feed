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
