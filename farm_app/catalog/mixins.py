from django.shortcuts import render


class UserPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if request.user.id != obj.user_id:
            return render(request, 'main/404page.html')

        return super().dispatch(request, *args, **kwargs)
