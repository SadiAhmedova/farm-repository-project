from django.shortcuts import render
from django.utils.functional import cached_property


class UserPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if request.user.id != obj.user_id:
            return render(request, 'main/404page.html')

        return super().dispatch(request, *args, **kwargs)


class RecentlyViewedMixin:
    def add_to_recently_viewed(self, product_id, product_type, product_name, product_photo):
        recently_viewed = self.request.session.get('recently_viewed', [])

        if hasattr(product_photo, 'url'):
            product_photo = product_photo.url
        elif isinstance(product_photo, str):
            pass
        else:
            product_photo = None

        product_entry = {'id': product_id, 'type': product_type, 'name': product_name, 'photo': product_photo}

        recently_viewed = [item for item in recently_viewed if item['id'] != product_id]

        recently_viewed.insert(0, product_entry)

        recently_viewed = recently_viewed[:3]

        self.request.session['recently_viewed'] = recently_viewed
        self.request.session.modified = True
    @cached_property
    def get_recently_viewed(self):
        return self.request.session.get('recently_viewed', [])

