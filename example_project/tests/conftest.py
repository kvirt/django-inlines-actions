import pytest
from django.apps import apps
from django.contrib import admin
from django.utils import timezone
from admin_inline_actions import InlineActionsMixin, InlineActionsModelAdminMixin

from example_app.models import Article, Author


@pytest.fixture
def author():
    for i in range(1, 9):
        author = apps.get_model(
            app_label='example_app',
            model_name='Author%(i)s' % {'i': i},
        )

        author = author.objects.create(
            name='Author',
        )

        article = apps.get_model(
            app_label='example_app',
            model_name='Article%(i)s' % {'i': i},
        )

        article.objects.create(
            author=author,
            text='Body lorem ipson dolor',
            title='Lorem ipson dolor',
        )

