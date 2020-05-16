from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.generic import View
from django.urls import reverse


class InlineActionView(View):

    instance = None

    def get(self, request, **kwargs):
        app_label, parent_model_name = request.path.split('/')[2:4]

        model = apps.get_model(
            app_label=app_label,
            model_name=kwargs['model_name'],
        )
        obj = model.objects.get(pk=self.kwargs['pk'])

        parent_model = apps.get_model(
            app_label=app_label,
            model_name=parent_model_name,
        )
        parent_obj = parent_model.objects.get(pk=self.kwargs['parent_pk'])

        action_func = getattr(self.instance, kwargs['action'])

        if getattr(action_func, 'permissions', None) is not None:
            if not self.instance.check_inline_permissions(request, action_func.permissions, obj, parent_obj):
                raise PermissionDenied

        ret = action_func(request, obj, parent_obj)

        if ret is not None:
            return ret

        back_url = reverse(
            'admin:%(app_label)s_%(parent_model_name)s_change' % {
                'app_label': app_label,
                'parent_model_name': parent_model_name,
            },
            kwargs={'object_id': kwargs['parent_pk']},
        )

        return redirect(back_url)
