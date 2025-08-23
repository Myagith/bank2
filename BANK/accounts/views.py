from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django_filters.views import FilterView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

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


def close_account(request, pk: int):
    account = get_object_or_404(Account, pk=pk)
    if account.status != Account.Status.CLOSED:
        account.status = Account.Status.CLOSED
        account.closed_at = timezone.now()
        account.save(update_fields=['status', 'closed_at'])
        messages.success(request, 'Compte clôturé.')
    else:
        messages.info(request, 'Compte déjà clôturé.')
    return redirect('accounts:detail', pk=pk)


def mark_closing(request, pk: int):
    account = get_object_or_404(Account, pk=pk)
    if account.status == Account.Status.OPEN:
        account.status = Account.Status.CLOSING
        account.save(update_fields=['status'])
        messages.success(request, 'Compte marqué en cours de fermeture.')
    else:
        messages.info(request, 'Statut du compte inchangé.')
    return redirect('accounts:detail', pk=pk)
