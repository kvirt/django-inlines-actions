===========================
DJANGO ADMIN INLINE ACTIONS
===========================

Easy-to-use actions for Django admin inlines

.. image:: https://img.shields.io/github/workflow/status/kvirt/django-inlines-actions/GH
    :target: https://github.com/kvirt/django-inlines-actions/actions/runs/106638267

.. image:: https://img.shields.io/codecov/c/github/kvirt/django-inlines-actions
    :target: https://codecov.io/gh/kvirt/django-inlines-actions

.. image:: https://img.shields.io/pypi/v/django-inlines-actions
    :target: https://pypi.org/project/django-inlines-actions/


Installation
============

1. Install django_inlines_actions

    .. code-block:: shell

        pip install django_inlines_actions

2. Add ``inlines_actions`` to your ``INSTALLED_APPS``.

3. Add the ``InlineActionsModelAdminMixin`` to your ``ModelAdmin``.

4. Add the ``InlineActionsMixin`` to your ``TabularInline``.

5. Add ``inline_actions`` attribute to your ``TabularInline`` as a tuple of your actions.

    .. code-block:: python

        inline_actions = ('your_action_name', 'another_action_name',)

6. Every action **must have** following signature:

    .. code-block:: python

        def your_action_name(self, request, obj, parent_obj):


Usage
=====

    Action is basically a link to another url with corresponding view.
    It does not depends on form as some other solutions and not execute on **Enter** hit.
    Action should return ``None`` to return to the current changeform or a ``HttpResponse`` instance.
    If you want do disable ``Actions`` column set ``inline_actions`` to ``None``.

    .. code-block:: python

        inline_actions = ('change_title',)

        def change_title(self, request, obj, parent_obj):
            obj.title  = obj.title + ' | ' + parent_obj.name
            obj.save()


Features
========

Permissions
-------------

    Permissions are instance of list/tuple classes and can be either custom function or django built-in permission.

    .. code-block:: python

        def your_action_name(self, request, obj, parent_obj):
            pass
        your_action_name.permissions = ('permission_func_name', 'django_builtin_permission_name',)

    permissions function **must have** following signature:

    .. code-block:: python

        def permission_func_name(self, request, obj, parent_obj):

    Must return `False` to fail permission check otherwise permission will be passed.

    If ``permissions`` returns ``False`` action will no be rendered for user and action will raise ``PermissionDenied`` on execution.

Short Description
-------------------

    Short Description are either custom function or simple string.

    .. code-block:: python

        def your_action_name(self, request, obj, parent_obj):
            pass
        your_action_name.short_description = 'My Uniq Description'

    .. code-block:: python

        your_action_name.short_description = 'short_description_func_name'

    short_description function **must have** following signature:

    .. code-block:: python

        def short_description_func_name(self, request, obj, parent_obj):

Css Class
-----------

    Css Class are either custom function or simple string.

    .. code-block:: python

        def your_action_name(self, request, obj, parent_obj):
            pass
        your_action_name.css_class = 'my-css-class-name'

    .. code-block:: python

        your_action_name.css_class = 'css_class_func_name'

    css_class function **must have** following signature:

    .. code-block:: python

        def css_class_func_name(self, request, obj, parent_obj):


Example
=======

.. code-block:: python

    from django.contrib import admin
    from admin_inline_actions.admin import InlineActionsMixin
    from admin_inline_actions.admin import InlineActionsModelAdminMixin

    from .models import Article1, Author1


    class ArticleInline(
        InlineActionsMixin,
        admin.TabularInline,
    ):
        model = Article1
        inline_actions = ('make_published',)

        def make_published(self, request, obj, parent_obj):
            obj.is_published = not obj.is_published
            obj.save()

        def make_published_permission(self, request, obj, parent_obj):
            if not request.user.is_superuser:
                return False

        def make_published_short_description(self, request, obj, parent_obj):
            return 'Published Make'

        def make_published_css_class(self, request, obj, parent_obj):
            return 'some_class'

        make_published.permissions = ('make_published_permission', 'example_app:can_change_article')
        make_published.short_description = make_published_short_description
        make_published.css_class = make_published_css_class


    class AuthorAdmin(
        InlineActionsModelAdminMixin,
        admin.ModelAdmin,
    ):
        inlines = (ArticleInline,)


    admin.site.register(Author1, AuthorAdmin)


Tests
-----

::

    pip install requirements.txt
    tox
