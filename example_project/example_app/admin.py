from django.contrib import admin
from admin_inline_actions.mixins import (
    InlineActionsMixin, InlineActionsModelAdminMixin,
)
from django.shortcuts import redirect
from django.urls import reverse
from .models import (
    Article, Article1, Article2, Article3, Article4, Article5, Article6, Article7, Article8,
    Author, Author1, Author2, Author3, Author4, Author5, Author6, Author7, Author8,
)


class BaseAdminInline(
    InlineActionsMixin,
    admin.TabularInline,
):
    extra = 0
    model = Article1
    inline_actions = ('make_published',)

    def make_published(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()

    def make_published_permission(self, request, obj, parent_obj):
        if request.user.is_superuser:
            return False

    make_published.permissions = ('make_published_permission', 'example_app:can_change_article')


class AllFeaturesInline(
    InlineActionsMixin,
    admin.TabularInline,
):

    extra = 0
    model = Article2
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


class MultipleActionsInline(
    InlineActionsMixin,
    admin.TabularInline,
):

    extra = 0
    model = Article3
    inline_actions = ('make_published', 'make_published2')

    def make_published2(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()

    def make_published(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()


class InvalidPermissionsInline(
    InlineActionsMixin,
    admin.TabularInline,
):

    extra = 0
    model = Article4
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

    def make_published_permission(self, request, obj, parent_obj):
        if not request.user.is_superuser:
            return False

    def make_published_permission2(self, request, obj, parent_obj):
        if request.user.is_superuser:
            return False

    make_published.permissions = ()
    make_published2.permissions = 'make_published_permission'
    make_published3.permissions = ('make_published_permission2',)


class NoActionsInline(
    InlineActionsMixin,
    admin.TabularInline,
):
    extra = 0
    model = Article5


class NoMixinInline(admin.TabularInline):

    extra = 0
    model = Article6
    inline_actions = ('make_published',)

    def make_published(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()


class CustomResponseInline(
    InlineActionsMixin,
    admin.TabularInline,
):

    extra = 0
    model = Article7
    inline_actions = ('make_published',)

    def make_published(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()

        url = reverse('admin:example_app_author1_add')
        return redirect(url)


class WrongActionNameInline(
    InlineActionsMixin,
    admin.TabularInline,
):

    extra = 0
    model = Article8
    inline_actions = ('foo_bar',)

    def make_published(self, request, obj, parent_obj):
        obj.is_published = not obj.is_published
        obj.save()

        url = reverse('admin:example_app_author1_add')
        return redirect(url)


class BaseModelAdmin(
    InlineActionsModelAdminMixin,
    admin.ModelAdmin,
):
    inlines = (BaseAdminInline,)


class AllFeaturesModelAdmin(BaseModelAdmin):
    inlines = (AllFeaturesInline,)


class MultipleActionsModelAdmin(BaseModelAdmin):
    inlines = (MultipleActionsInline,)


class InvalidPermissionsModelAdmin(BaseModelAdmin):
    inlines = (InvalidPermissionsInline,)


class NoActionsModelAdmin(BaseModelAdmin):
    inlines = (NoActionsInline,)


class NoMixinModelAdmin(BaseModelAdmin):
    inlines = (NoMixinInline,)


class CustomResponseModelAdmin(BaseModelAdmin):
    inlines = (CustomResponseInline,)


class WrongActionNameModelAdmin(BaseModelAdmin):
    inlines = (WrongActionNameInline,)


admin.site.register(Author1, BaseModelAdmin)

admin.site.register(Author2, AllFeaturesModelAdmin)

admin.site.register(Author3, MultipleActionsModelAdmin)

admin.site.register(Author4, InvalidPermissionsModelAdmin)

admin.site.register(Author5, NoActionsModelAdmin)

admin.site.register(Author6, NoMixinModelAdmin)

admin.site.register(Author7, CustomResponseModelAdmin)

admin.site.register(Author8, WrongActionNameModelAdmin)
