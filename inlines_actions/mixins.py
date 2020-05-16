from django.core.exceptions import ImproperlyConfigured
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .views import InlineActionView


class InlineActionsMixin:

    inline_actions = None

    def __init__(self, parent_model, admin_site):
        super().__init__(parent_model, admin_site)

        self.request = None

    class Media:
        css = {
            'all': ('inlines_actions/css/styles.css',),
        }

    def get_inline_actions(self, request, parent_obj):
        if self.inline_actions is None:
            return self.inline_actions

        for action in self.inline_actions:
            getattr(self, action)

        return self.inline_actions

    def check_inline_permissions(self, request, permissions, obj, parent_obj):
        if not permissions:
            return True

        if isinstance(permissions, (list, tuple)):
            for permission in permissions:

                is_attr = getattr(self, permission, None)

                if is_attr is not None:
                    ret = is_attr(request, obj, parent_obj)
                else:
                    ret = request.user.has_perm(permission)

                if ret == False:
                    return ret
        else:
            raise ImproperlyConfigured(_('Permissions must be instance of list or tuple'))

        return True

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)

        self.parent_obj = obj

        if not self.get_inline_actions(request, obj):
            return fields

        fields = ('render_inline_actions',) + fields

        return fields

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)

        if not self.get_inline_actions(request, obj):
            return fields

        return fields

    def render_inline_actions(self, obj=None):
        if not (obj and obj.pk):
            return ''

        buttons = []

        for action_name in self.inline_actions:
            action_func = getattr(self, action_name)

            if getattr(action_func, 'permissions', None) is not None:
                if not self.check_inline_permissions(self.request, action_func.permissions, obj, self.parent_obj):
                    continue

            if getattr(action_func, 'css_class', None) is not None:
                css_attr = action_func.css_class
                css_class = getattr(self, css_attr.__name__)(self.request, obj, self.parent_obj) if callable(css_attr) else css_attr  # noqa
            else:
                css_class = 'inline-action'

            if getattr(action_func, 'short_description', None) is not None:
                descr_attr = action_func.short_description
                short_description =  getattr(self, descr_attr.__name__)(self.request, obj, self.parent_obj) if callable(descr_attr) else descr_attr  # noqa
            else:
                short_description = ' '.join(action_func.__name__.title().split('_'))

            url = reverse(
                'admin:%(app_label)s_%(parent_model)s_%(action_name)s' % {
                    'app_label': self.parent_model._meta.app_label,
                    'parent_model': self.parent_model._meta.model_name,
                    'action_name': action_name,
                },
                kwargs={
                    'parent_pk': self.parent_obj.pk,
                    'model_name': self.model._meta.model_name,
                    'pk': obj.pk,
                    'action': action_name,
                },
            )

            buttons.append(
                '<a href="%(url)s" class="%(css_class)s">%(short_description)s</a>' % {
                    'url': url,
                    'css_class': css_class,
                    'short_description': short_description,
                }
            )

        if not buttons:
            return ''

        buttons = ''.join(buttons)

        return mark_safe(buttons)
    render_inline_actions.short_description = _('Actions')


class InlineActionsModelAdminMixin:

    def __init__(self, parent_model, admin_site):
        super().__init__(parent_model, admin_site)

        self.urls_registred = False
        self.inline_instances = []

    def get_urls(self):
        urls = super().get_urls()
        return self._get_inline_action_urls() + urls

    def get_inline_instances(self, request, obj=None):
        instances = super().get_inline_instances(request, obj=obj)

        for instance in instances:
            if not isinstance(instance, InlineActionsMixin):
                continue

            if not instance.inline_actions:
                continue

            if not self.urls_registred:
                self.inline_instances.append(instance)
            else:
                instance.request = request

        self.urls_registred = True

        return instances

    def _get_inline_action_urls(self):
        self.get_inline_instances(request=None, obj=None)

        urls = []

        for instance in self.inline_instances:
            for action in instance.inline_actions:
                urls.append(
                    path(
                        '<parent_pk>/<model_name>/<pk>/<action>',
                        self.admin_site.admin_view(InlineActionView.as_view(instance=instance)),
                        name='%(app_label)s_%(model_name)s_%(action)s' % {
                            'app_label': self.model._meta.app_label,
                            'model_name': self.model._meta.model_name,
                            'action': action,
                        },
                    ),
                )

        return urls
