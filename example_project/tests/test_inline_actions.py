import pytest

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.urls import reverse
from lxml.html import fragment_fromstring, fromstring


def test_actions_available(admin_client, author):
    url = reverse('admin:example_app_author1_change', args=(1,))
    changeview = admin_client.get(url)

    assert 'Actions' in changeview.rendered_content


def test_actions_attributes(admin_client, author):
    url = reverse('admin:example_app_author2_change', args=(1,))
    changeview = admin_client.get(url)

    assert 'Published Make' in changeview.rendered_content

    actions = fromstring(changeview.rendered_content).xpath('//td[@class="field-render_inline_actions"]//p/a')

    assert actions[0].get('class') == 'some_class'


def test_multiple_actions(admin_client, author):
    url = reverse('admin:example_app_author3_change', args=(1,))
    changeview = admin_client.get(url)

    actions = fromstring(changeview.rendered_content).xpath('//td[@class="field-render_inline_actions"]//p/a')

    assert len(actions) == 2


def test_invalid_permissions(admin_client, author):
    url = reverse('admin:example_app_author4_change', args=(1,))

    with pytest.raises(ImproperlyConfigured):
        changeview = admin_client.get(url)

        actions = fromstring(changeview.rendered_content).xpath('//td[@class="field-render_inline_actions"]//p/a')


def test_no_actions(admin_client, author):
    url = reverse('admin:example_app_author5_change', args=(1,))
    changeview = admin_client.get(url)

    actions = fromstring(changeview.rendered_content).xpath('//td[@class="field-render_inline_actions"]//p/a')

    assert len(actions) == 0


def test_no_mixins(admin_client, author):
    url = reverse('admin:example_app_author5_change', args=(1,))
    changeview = admin_client.get(url)

    actions = fromstring(changeview.rendered_content).xpath('//td[@class="field-render_inline_actions"]//p/a')

    assert len(actions) == 0


def test_permissions_failed(admin_client, author):
    url = reverse('admin:example_app_author9_change', args=(1,))
    changeview = admin_client.get(url)

    actions = fromstring(changeview.rendered_content).xpath('//td[@class="field-render_inline_actions"]//p/a')

    assert len(actions) == 0


def test_view(admin_client, author):
    from example_app.models import Article2
    article = Article2.objects.first()

    assert not article.is_published

    url = reverse(
        'admin:example_app_author2_make_published',
        kwargs={
            'parent_pk': 1,
            'model_name': 'article2',
            'pk': 1,
            'action': 'make_published',
        },
    )
    admin_client.get(url)

    article.refresh_from_db()
    assert article.is_published


def test_view_invalid_permissions(admin_client, author):
    url = reverse(
        'admin:example_app_author4_make_published3',
        kwargs={
            'parent_pk': 1,
            'model_name': 'article4',
            'pk': 1,
            'action': 'make_published3',
        },
    )

    with pytest.raises(ImproperlyConfigured):
        response = admin_client.get(url)

    url = reverse(
        'admin:example_app_author4_make_published',
        kwargs={
            'parent_pk': 1,
            'model_name': 'article4',
            'pk': 1,
            'action': 'make_published',
        },
    )

    response = admin_client.get(url)
    assert response.status_code == 403


def test_view_custom_response(admin_client, author):
    url = reverse(
        'admin:example_app_author7_make_published',
        kwargs={
            'parent_pk': 1,
            'model_name': 'article7',
            'pk': 1,
            'action': 'make_published',
        },
    )

    response = admin_client.get(url)

    assert response.url == '/admin/example_app/author1/add/'


def test_wrong_action_name(admin_client, author):
    url = reverse('admin:example_app_author8_change', args=(1,))

    with pytest.raises(AttributeError):
        changeview = admin_client.get(url)
