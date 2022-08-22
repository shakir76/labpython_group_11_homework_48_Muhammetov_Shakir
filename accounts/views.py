from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm
from accounts.models import Profile
from shop.forms import SearchForm


class RegisterView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        Profile.objects.create(user=user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('shop:index_list')
        return next_url


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'profile_view.html'
    # paginate_by = 3
    # paginate_orphans = 0
    #
    # def get_context_data(self, **kwargs):
    #     paginator = Paginator(self.get_object().projects.all(), self.paginate_by, self.paginate_orphans)
    #     page_number = self.request.GET.get('page', 1)
    #     page_objects = paginator.get_page(page_number)
    #     context = super().get_context_data(**kwargs)
    #     context['page_obj'] = page_objects
    #     context['projects'] = page_objects.object_list
    #     context['is_paginated'] = page_objects.has_other_pages()
    #     return context


class ListProfile(PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = "index_user.html"
    context_object_name = "users"
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return get_user_model().objects.filter(
                Q(name__icontains=self.search_value))
        return get_user_model().objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context["query"] = query
            context["search"] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")

    def has_permission(self):
        return 'Project Manager' in self.request.user.groups.all().values_list('name', flat=True) or \
               'Team Lead' in self.request.user.groups.all().values_list('name', flat=True)


class ChangeProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'change_user.html'
    profile_form = ProfileChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in context:
            context['profile_form'] = self.profile_form(instance=self.get_object().profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object, data=request.POST)
        profile_form = self.profile_form(instance=self.object.profile, data=request.POST, files=request.FILES)
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form, profile_form):
        form.save()
        profile_form.save()
        return redirect('accounts:profile_view', self.object.pk)

        def form_invalid(self, form, profile_form):
            return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))


class ChangePasswordView(PasswordChangeView):
    template_name = 'change_password.html'

    def get_success_url(self):
        return reverse('accounts:profile_view', kwargs={'pk': self.request.user.pk})

