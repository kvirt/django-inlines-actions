from django.contrib import admin
from inlines_actions.mixins import (
    InlineActionsMixin, InlineActionsModelAdminMixin,
)
from django.shortcuts import redirect
from django.urls import reverse
from .models import Article, Author, AuthorInvalid

class AdminInlineMixin(
    InlineActionsMixin,
    admin.TabularInline,
):

    extra = 0
    model = Article


class BaseAdminInline(AdminInlineMixin):

    inline_actions = ('make_published', 'make_published2', 'make_published3')

    def make_published3(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()

    def make_published2(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()

        url = reverse('admin:example_app_author_changelist')
        return redirect(url)

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


class InvalidPermissionsInline(AdminInlineMixin):

    inline_actions = ('make_published', 'make_published2', 'make_published3')

    def make_published3(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()

    def make_published2(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()

    def make_published(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()

    def make_published_permission2(self, request, obj, parent_obj):
        if request.user.is_superuser:
            return False

    make_published.permissions = ('make_published_permission2', 'example_app:can_change_article')
    make_published2.permissions = ()
    make_published3.permissions = 'make_published_permission'


class NoActionsInline(
    InlineActionsMixin,
    admin.TabularInline,
):
    extra = 0
    model = Article


class NoMixinInline(admin.TabularInline):

    extra = 0
    model = Article
    inline_actions = ('make_published',)

    def make_published(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()


class WrongActionNameInline(AdminInlineMixin):

    def make_published(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()

    inline_actions = ('foo_bar',)


class PermissionsFailedInline(AdminInlineMixin):

    inline_actions = ('make_published',)

    def make_published(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()

    def make_published_permission(self, request, obj, parent_obj):
        if request.user.is_superuser:
            return False

    make_published.permissions = ('make_published_permission',)


class BaseModelAdmin(
    InlineActionsModelAdminMixin,
    admin.ModelAdmin,
):
    inlines = (BaseAdminInline,)


class InvalidModelAdmin(
    InlineActionsModelAdminMixin,
    admin.ModelAdmin,
):
    inlines = (InvalidPermissionsInline,)


admin.site.register(Author, BaseModelAdmin)

admin.site.register(AuthorInvalid, InvalidModelAdmin)
