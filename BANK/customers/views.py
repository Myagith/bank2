from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django_filters.views import FilterView

from .models import Customer
from .forms import CustomerForm
from .filters import CustomerFilter


class CustomerListView(FilterView):
    model = Customer
    template_name = 'customers/list.html'
    context_object_name = 'customers'
    filterset_class = CustomerFilter
    paginate_by = 20


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/form.html'
    success_url = reverse_lazy('customers:list')


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/form.html'
    success_url = reverse_lazy('customers:list')


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/detail.html'


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customers:list')
    template_name = 'customers/confirm_delete.html'
