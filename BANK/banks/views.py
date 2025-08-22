from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django_filters.views import FilterView
from django.db.models import Count

from .models import Bank
from .forms import BankForm
from .filters import BankFilter


class BankListView(FilterView):
    model = Bank
    template_name = 'banks/list.html'
    context_object_name = 'banks'
    filterset_class = BankFilter
    paginate_by = 20


class BankCreateView(CreateView):
    model = Bank
    form_class = BankForm
    template_name = 'banks/create.html'
    success_url = reverse_lazy('banks:list')


class BankUpdateView(UpdateView):
    model = Bank
    form_class = BankForm
    template_name = 'banks/update.html'
    success_url = reverse_lazy('banks:list')


class BankDetailView(DetailView):
    model = Bank
    template_name = 'banks/detail.html'
    context_object_name = 'bank'


class BankDeleteView(DeleteView):
    model = Bank
    success_url = reverse_lazy('banks:list')
    template_name = 'banks/confirm_delete.html'


class BankTop15View(ListView):
    model = Bank
    template_name = 'banks/top15.html'
    context_object_name = 'banks'

    def get_queryset(self):
        return Bank.objects.annotate(num_customers=Count('customers')).order_by('-num_customers')[:15]
