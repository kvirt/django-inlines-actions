from django.db import models


class Author(models.Model):
    name = models.CharField(
        max_length=256,
    )

    class Meta:
        abstract = True


class Article(models.Model):
    title = models.CharField(
        max_length=256,
    )

    text = models.TextField()

    is_published = models.BooleanField(
        default=False,
    )

    class Meta:
        abstract = True


class Author1(Author):
    pass


class Article1(Article):
    author = models.ForeignKey(
        'example_app.Author1',
        on_delete=models.CASCADE
    )


class Author2(Author):
    pass


class Article2(Article):
    author = models.ForeignKey(
        'example_app.Author2',
        on_delete=models.CASCADE
    )


class Author3(Author):
    pass


class Article3(Article):
    author = models.ForeignKey(
        'example_app.Author3',
        on_delete=models.CASCADE
    )


class Author4(Author):
    pass


class Article4(Article):
    author = models.ForeignKey(
        'example_app.Author4',
        on_delete=models.CASCADE
    )


class Author5(Author):
    pass


class Article5(Article):
    author = models.ForeignKey(
        'example_app.Author5',
        on_delete=models.CASCADE
    )


class Author6(Author):
    pass


class Article6(Article):
    author = models.ForeignKey(
        'example_app.Author6',
        on_delete=models.CASCADE
    )


class Author7(Author):
    pass


class Article7(Article):
    author = models.ForeignKey(
        'example_app.Author7',
        on_delete=models.CASCADE
    )


class Author8(Author):
    pass


class Article8(Article):
    author = models.ForeignKey(
        'example_app.Author8',
        on_delete=models.CASCADE
    )
