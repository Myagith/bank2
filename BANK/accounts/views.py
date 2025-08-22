from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django_filters.views import FilterView

from .models import Account
from .forms import AccountForm


class AccountListView(FilterView):
    model = Account
    template_name = 'accounts/list.html'
    context_object_name = 'accounts'
    filterset_fields = ['customer__bank', 'status', 'type']
    paginate_by = 20


class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('accounts:list')


class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('accounts:list')


class AccountDetailView(DetailView):
    model = Account
    template_name = 'accounts/detail.html'


class AccountDeleteView(DeleteView):
    model = Account
    success_url = reverse_lazy('accounts:list')
    template_name = 'accounts/confirm_delete.html'
