from itertools import chain

from django.contrib.auth import get_user_model
from django.conf.urls.static import static
from django.shortcuts import redirect, render
from django.urls import reverse, resolve
from django.views import generic as views

from farm_app.accounts.models import FarmerUser
from farm_app.catalog.forms import *
from farm_app.catalog.mixins import UserPermissionMixin
from farm_app.catalog.models import *

from farm_app.catalog.mixins import RecentlyViewedMixin

UserModel = get_user_model()


class IndexView(views.ListView, RecentlyViewedMixin):
    template_name = 'main/home.html'


    def get_queryset(self):
        veg_fruit = VegetableAndFruit.objects.all()
        nuts = Nut.objects.all()
        animal_products = AnimalProduct.objects.all()
        dairies = DairyProduct.objects.all()
        return list(chain(veg_fruit, nuts, animal_products, dairies))

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            current_page = resolve(self.request.path_info).url_name
            count_all_products = FarmerUser.objects.all().count() + DairyProduct.objects.all().count() + Nut.objects.all().count() + AnimalProduct.objects.all().count()

            context['count_all_products'] = count_all_products
            context['users'] = FarmerUser.objects.all()
            context['veg_fruit'] = VegetableAndFruit.objects.all()
            context['dairies'] = DairyProduct.objects.all()
            context['nuts'] = Nut.objects.all()
            context['animal_products'] = AnimalProduct.objects.all()
            context['current_page'] = current_page
            context['recently_viewed'] = self.get_recently_viewed

            return context

def aboutPage(request):
    return render(request, 'main/about-us.html')


class VegetableCreateView(views.CreateView):
    template_name = 'catalog/create-vegetable-page.html'
    model = VegetableAndFruit
    form_class = VegetableCreationForm

    def get_success_url(self):
        return reverse('details vegetable', kwargs={
            'pk': self.object.pk,
        })

    def form_valid(self, form):
        print(self.request.FILES)
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.pk
        self.object.save()
        return super().form_valid(form)


class VegetableEditView(views.UpdateView, UserPermissionMixin):
    model = VegetableAndFruit
    template_name = 'catalog/edit-vegetable-page.html'
    form_class = VegetableCreationForm
    context_object_name = 'plant'

    def form_valid(self, form):
        print(self.request.FILES)
        instance = form.save(commit=False)

        photo = self.request.FILES.get('photo')
        if photo:
            instance.photo = photo
        instance.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('details vegetable', kwargs={
            'pk': self.object.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class VegetableDetailsView(views.DetailView, RecentlyViewedMixin):
    model = VegetableAndFruit
    context_object_name = 'plant'
    template_name = 'catalog/details-vegetable-page.html'
    model_name = object.__class__.__name__

    def get_profile(self):
        profile = FarmerUser.objects.all().get(id=self.object.user_id)
        return profile

    def get_photo(self):
        if self.object.photo:
            return self.object.photo.url
        return static('images/fruit-and-veg.jpg')

    def get_context_data(self, **kwargs):
        self.add_to_recently_viewed(self.object.id, 'VegetableAndFruit', self.object.__str__(), self.get_photo())

        context = super().get_context_data(**kwargs)
        context.update({
            'recently_viewed': self.get_recently_viewed,
            'photo': self.get_photo(),
            'model_name': self.model_name,
            'profile': self.get_profile,
        })

        return context


class VegetableDeleteView(views.DeleteView):
    model = VegetableAndFruit
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_model'] = 'VegetableAndFruit'
        return context

    def get_success_url(self):
        return reverse('profile details', kwargs={
            'pk': self.request.user.id
        })


class NutCreateView(views.CreateView):
    template_name = 'catalog/create-nut-page.html'
    model = Nut
    form_class = NutCreationForm


    def get_success_url(self):
        return reverse('details nut', kwargs={
            'pk': self.object.pk,
        })

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.pk
        self.object.save()
        return super().form_valid(form)


class NutEditView(views.UpdateView, UserPermissionMixin):
    model = Nut
    template_name = 'catalog/edit-nut-page.html'
    form_class = NutCreationForm
    context_object_name = 'nut'

    def get_success_url(self):
        return reverse('details nut', kwargs={
            'pk': self.object.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NutDetailsView(views.DetailView, RecentlyViewedMixin):
    model = Nut
    context_object_name = 'nut'
    template_name = 'catalog/details-nut-page.html'
    model_name = object.__class__.__name__

    def get_profile(self):
        profile = FarmerUser.objects.all().get(id=self.object.user_id)
        return profile

    def get_photo(self):
        if self.object.photo:
            return self.object.photo.url
        return static('images/nuts-and-dry-fruits.jpg')

    def get_context_data(self, **kwargs):
        self.add_to_recently_viewed(self.object.id, 'Nut', self.object.__str__(), self.get_photo())

        context = super().get_context_data(**kwargs)
        context.update({
            'recently_viewed': self.get_recently_viewed,
            'photo': self.get_photo(),
            'model_name': self.model_name,
            'profile': self.get_profile,
        })

        return context


class NutDeleteView(views.DeleteView):
    model = Nut
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_model'] = 'Nut'
        return context

    def get_success_url(self):
        return reverse('profile details', kwargs={
            'pk': self.request.user.id
        })


class DairyCreateView(views.FormView):
    template_name = 'catalog/create-dairy-page.html'
    model = DairyProduct
    form_class = DairyCreationForm

    def get_success_url(self):
        return reverse('details dairy', kwargs={
            'pk': self.object.pk,
        })

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.pk
        self.object.save()
        return super().form_valid(form)


class DairyEditView(views.UpdateView, UserPermissionMixin):
    model = DairyProduct
    template_name = 'catalog/edit-dairy-page.html'
    form_class = DairyCreationForm
    context_object_name = 'dairy'

    def get_success_url(self):
        return reverse('details dairy', kwargs={
            'pk': self.object.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DairyDetailsView(views.DetailView, RecentlyViewedMixin):
    model = DairyProduct
    context_object_name = 'dairy'
    template_name = 'catalog/details-dairy-page.html'

    model_name = object.__class__.__name__

    def get_profile(self):
        profile = FarmerUser.objects.all().get(id=self.object.user_id)
        return profile

    def get_photo(self):
        if self.object.photo :
            return self.object.photo.url
        return static('images/milk-products.jpg')

    def get_context_data(self, **kwargs):
        self.add_to_recently_viewed(self.object.id, 'DairyProduct', self.object.__str__(), self.get_photo())

        context = super().get_context_data(**kwargs)
        context.update({
            'recently_viewed': self.get_recently_viewed,
            'photo': self.get_photo(),
            'model_name': self.model_name,
            'profile': self.get_profile,
        })

        return context


class DairyDeleteView(views.DeleteView):
    model = DairyProduct
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_model'] = 'DairyProduct'
        return context

    def get_success_url(self):
        return reverse('profile details', kwargs={
            'pk': self.request.user.id
        })


class AnimalCreateView(views.FormView):
    template_name = 'catalog/create-animal-page.html'
    model = AnimalProduct
    form_class = AnimalCreationForm


    def get_success_url(self):
        return reverse('details animal', kwargs={
            'pk': self.object.pk,
        })

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.pk
        self.object.save()
        return super().form_valid(form)


class AnimalEditView(UserPermissionMixin, views.UpdateView):
    model = AnimalProduct
    template_name = 'catalog/edit-animal-page.html'
    form_class = AnimalCreationForm
    context_object_name = 'animal'

    def get_success_url(self):
        return reverse('details animal', kwargs={
            'pk': self.object.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AnimalDetailsView(views.DetailView, RecentlyViewedMixin):
    model = AnimalProduct
    context_object_name = 'meat'
    template_name = 'catalog/details-animal-page.html'
    model_name = object.__class__.__name__

    def get_profile(self):
        profile = FarmerUser.objects.all().get(id=self.object.user_id)
        return profile

    def get_photo(self):
        if self.object.photo:
            return self.object.photo.url
        return static('images/meat.jpg')

    def get_context_data(self, **kwargs):
        self.add_to_recently_viewed(self.object.id, 'AnimalProduct', self.object.__str__(), self.get_photo())

        context = super().get_context_data(**kwargs)
        context.update({
            'recently_viewed': self.get_recently_viewed,
            'photo': self.get_photo(),
            'model_name': self.model_name,
            'profile': self.get_profile,
        })

        return context


class AnimalDeleteView(views.DeleteView):
    model = AnimalProduct
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_model'] = 'AnimalProduct'
        return context

    def get_success_url(self):
        return reverse('profile details', kwargs={
            'pk': self.request.user.id
        })
