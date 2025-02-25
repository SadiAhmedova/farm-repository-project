from itertools import chain
from django.contrib import messages

from django.conf.urls.static import static
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, get_user_model
from django.urls import reverse_lazy, reverse, resolve
from django.views.generic import FormView

from farm_app.accounts.forms import CreateProfileForm, LoginProfileForm, EditProfileForm
from farm_app.accounts.models import FarmerUser
from farm_app.catalog.models import VegetableAndFruit, DairyProduct, Nut, AnimalProduct

import cloudinary.uploader
UserModel = get_user_model()


class ProfileLoginView(FormView):
    template_name = 'accounts/profile_login.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        login_form = LoginProfileForm()
        register_form = CreateProfileForm()
        return render(request, self.template_name, {'login_form': login_form, 'register_form': register_form})

    def post(self, request, *args, **kwargs):
        if 'login_submit' in request.POST:
            return self.handle_login(request)
        elif 'register_submit' in request.POST:
            return self.handle_register(request)
        return self.get(request)

    def handle_login(self, request):
        login_form = LoginProfileForm(data=request.POST)
        register_form = CreateProfileForm()

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect(self.success_url)

        return render(request, self.template_name, {'login_form': login_form, 'register_form': register_form})

    def handle_register(self, request):
        register_form = CreateProfileForm(request.POST, request.FILES)
        login_form = LoginProfileForm()

        if register_form.is_valid():
            user = register_form.save(commit=False)

            if request.FILES.get('profile_picture'):
                upload_result = cloudinary.uploader.upload(request.FILES['profile_picture'])
                user.profile_picture = upload_result['secure_url']

            user.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully!")
            return redirect(self.success_url)

        return render(request, self.template_name, {'login_form': login_form, 'register_form': register_form})

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
    success_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('home')

def error_404_view(request, exception):
    return render(request, 'main/404page.html')