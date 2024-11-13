from itertools import chain

from django.conf.urls.static import static
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, get_user_model
from django.urls import reverse_lazy, reverse, resolve

from farm_app.accounts.forms import CreateProfileForm, LoginProfileForm, EditProfileForm
from farm_app.accounts.models import FarmerUser
from farm_app.catalog.models import VegetableAndFruit, DairyProduct, Nut, AnimalProduct

UserModel = get_user_model()


class ProfileLoginView(auth_views.LoginView):
    form_class = LoginProfileForm
    template_name = 'accounts/profile_login.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form


class ProfileRegisterView(views.CreateView):
    model = FarmerUser
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class ProfileLogoutView(auth_views.LogoutView):
    pass


class ProfileDetailsView(views.DetailView):
    model = FarmerUser
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'
    picture = static('images/profile.jpg')

    def get_profile_image(self):
        if self.object.profile_picture is not None:
            return self.object.profile_picture
        return self.picture

    def model_name(self, product):
        return str(product.__class__.__name__)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.get_object()
        vegetable = VegetableAndFruit.objects.filter(user_id=user.id)
        dairy = DairyProduct.objects.filter(user_id=user.id)
        nut = Nut.objects.filter(user_id=user.id)
        animal = AnimalProduct.objects.filter(user_id=user.id)
        all_products = list(chain(vegetable, dairy, nut, animal))

        context['veg_fruit'] = vegetable
        context['dairies'] = dairy
        context['nuts'] = nut
        context['animal_products'] = animal
        context['profile_picture'] = self.get_profile_image()
        context['all_my_products'] = [
            {'product': product, 'model_name': self.model_name(product)} for product in all_products
        ]
        context['products_count'] = int(vegetable.count() + dairy.count() + nut.count() + animal.count())

        return context


class ProfileEditView(views.UpdateView):
    model = FarmerUser
    form_class = EditProfileForm
    template_name = 'accounts/profile_edit.html'
    def dispatch(self, request, *args, **kwargs):
        user_in_url = get_object_or_404(FarmerUser, pk=self.kwargs['pk'])

        if request.user.id != user_in_url.id:
            return render(request, 'main/404page.html')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile details', kwargs={
            'pk': self.object.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfileDeleteView(views.DeleteView):
    model = FarmerUser
    success_url = reverse_lazy('profile details')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def error_404_view(request, exception):
    return render(request, 'main/404page.html')