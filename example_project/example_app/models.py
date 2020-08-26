from django.db import models


class Author(models.Model):

    name = models.CharField(
        max_length=256,
    )


class Article(models.Model):

    author = models.ForeignKey(
        'example_app.Author',
        on_delete=models.CASCADE,
        null=True,
    )

    author_invalid = models.ForeignKey(
        'example_app.AuthorInvalid',
        on_delete=models.CASCADE,
        null=True,
    )

    title = models.CharField(
        max_length=256,
    )

    text = models.TextField()

    is_published = models.BooleanField(
        default=False,
    )


class AuthorInvalid(models.Model):

    name = models.CharField(
        max_length=256,
    )

