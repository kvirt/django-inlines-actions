import pytest

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.urls import reverse
from lxml.html import fragment_fromstring, fromstring

from example_app.models import Article, Author
from example_app import admin


def test_actions_base(
    admin_client,
    loaded_models,
    model_admin_url,
):
    changeview = admin_client.get(model_admin_url)

    assert 'Actions' in changeview.rendered_content

    assert 'Published Make' in changeview.rendered_content

    actions = fromstring(changeview.rendered_content).xpath('//td[@class="field-render_inline_actions"]//p/a')

    assert actions[0].get('class') == 'some_class'

    assert len(actions) == 3


def test_invalid_permissions(
    admin_client,
    loaded_models,
    model_admin_url,
    model_admin_instance,
):
    model_admin_instance.inlines = (admin.InvalidPermissionsInline,)

    with pytest.raises(ImproperlyConfigured):
        changeview = admin_client.get(model_admin_url)

        actions = fromstring(changeview.rendered_content).xpath('//td[@class="field-render_inline_actions"]//p/a')


def test_no_actions(
    admin_client,
    loaded_models,
    model_admin_url,
    model_admin_instance,
):
    model_admin_instance.inlines = (admin.NoActionsInline,)

    changeview = admin_client.get(model_admin_url)

    actions = fromstring(changeview.rendered_content).xpath('//td[@class="field-render_inline_actions"]//p/a')

    assert len(actions) == 0


def test_no_mixins(
    admin_client,
    loaded_models,
    model_admin_url,
    model_admin_instance,
):
    model_admin_instance.inlines = (admin.NoMixinInline,)

    changeview = admin_client.get(model_admin_url)

    actions = fromstring(changeview.rendered_content).xpath('//td[@class="field-render_inline_actions"]//p/a')

    assert len(actions) == 0


def test_permissions_failed(
    admin_client,
    loaded_models,
    model_admin_url,
    model_admin_instance,
):
    model_admin_instance.inlines = (admin.PermissionsFailedInline,)

    changeview = admin_client.get(model_admin_url)

    actions = fromstring(changeview.rendered_content).xpath('//td[@class="field-render_inline_actions"]//p/a')

    assert len(actions) == 0


def test_view(
    admin_client,
    loaded_models,
    action_url_factory
):
    article = loaded_models.article

    assert not article.is_published

    admin_client.get(action_url_factory('make_published'))

    article.refresh_from_db()
    assert article.is_published


def test_view_invalid_permissions(
    admin_client,
    loaded_models,
    model_admin_instance,
    action_url_factory
):

    with pytest.raises(ImproperlyConfigured):
        admin_client.get(action_url_factory(
            'make_published3',
            model_name='authorinvalid',
        ))


    response = admin_client.get(action_url_factory(
        'make_published',
        model_name='authorinvalid',
    ))
    assert response.status_code == 403


def test_view_custom_response(
    admin_client,
    loaded_models,
    action_url_factory,
):

    response = admin_client.get(action_url_factory('make_published2'))

    assert response.url == '/admin/example_app/author/'


def test_wrong_action_name(
    admin_client,
    loaded_models,
    model_admin_instance,
    model_admin_url,
):
    model_admin_instance.inlines = (admin.WrongActionNameInline,)

    with pytest.raises(AttributeError):
        changeview = admin_client.get(model_admin_url)
