from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django_filters.views import FilterView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Transaction
from .forms import TransactionForm
from .services import post_transaction


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/create.html'
    success_url = reverse_lazy('transactions:history')

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            post_transaction(self.object)
            messages.success(self.request, 'Transaction posted.')
        except Exception as e:
            messages.error(self.request, str(e))
        return response


class TransactionHistoryView(LoginRequiredMixin, FilterView):
    model = Transaction
    template_name = 'transactions/history.html'
    context_object_name = 'transactions'
    filterset_fields = {
        'created_at': ['date__gte', 'date__lte'],
        'amount': ['gte', 'lte'],
        'type': ['exact'],
        'account__customer__bank': ['exact'],
    }
    paginate_by = 20
