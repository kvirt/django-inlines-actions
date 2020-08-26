from collections import namedtuple

import pytest
from django.apps import apps
from django.contrib.admin import site
from django.urls import reverse

from example_app.admin import BaseAdminInline
from example_app.models import Article, Author, AuthorInvalid


@pytest.fixture
def loaded_models():
    author = Author.objects.create(
        name='Author',
    )

    author_invalid = AuthorInvalid.objects.create(
        name='Author',
    )

    article = Article.objects.create(
        author=author,
        author_invalid=author_invalid,
        text='Body lorem ipson dolor',
        title='Lorem ipson dolor',
    )

    Models = namedtuple('Models', ['author', 'article', 'author_invalid'])

    return Models(
        author=author,
        article=article,
        author_invalid=author_invalid,
    )


@pytest.fixture
def model_admin_instance():
    model_admin_instance = site._registry[Author]

    yield model_admin_instance

    model_admin_instance.inlines = BaseAdminInline


@pytest.fixture
def model_admin_url():
     return reverse('admin:example_app_author_change', args=(1,))


@pytest.fixture
def action_url_factory():

    def _action_url_factory(action_name, model_name='author'):
        return reverse(
            f'admin:example_app_{model_name}_{action_name}',
            kwargs={
                'parent_pk': 1,
                'model_name': 'article',
                'pk': 1,
                'action': action_name,
            },
        )

    return _action_url_factory
