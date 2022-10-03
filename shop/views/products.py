# import telebot
import telegram_send
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from shop.forms import ProductForm, SearchForm, OrderForm, ProductAddForm
from shop.models import Product, Order, OrderProduct




class IndexView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"
    ordering = ("category", 'name')
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Product.objects.filter(
                Q(name__icontains=self.search_value) | Q(category__icontains=self.search_value))
        return Product.objects.all().order_by(('category'), ('name'))

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


class ProductView(DetailView):
    template_name = "products/product_view.html"
    model = Product


class CreateProduct(PermissionRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = "products/create.html"

    def has_permission(self):
        return self.request.user.is_superuser or 'moderators' in self.request.user.groups.all().values_list('name',
                                                                                                            flat=True)


class UpdateProduct(PermissionRequiredMixin, UpdateView):
    form_class = ProductForm
    template_name = 'products/update.html'
    model = Product

    def has_permission(self):
        return self.request.user.is_superuser or 'moderators' in self.request.user.groups.all().values_list('name',
                                                                                                            flat=True)


class DeleteProduct(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/delete.html'
    success_url = reverse_lazy('shop:index')

    def has_permission(self):
        return self.request.user.is_superuser or 'moderators' in self.request.user.groups.all().values_list('name',
                                                                                                            flat=True)


class ProductAdd(CreateView):
    form_class = ProductAddForm

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        qty = form.cleaned_data.get('balance')
        if qty > product.balance:
            pass
        else:
            if not self.request.session.get('cart'):
                self.request.session['cart'] = [{'name': product.pk, 'qty': qty}]
            else:
                cart = self.request.session.get('cart')
                if next((x for x in cart if x["name"] == product.pk), None):
                    for a in cart:
                        if a['name'] == product.pk:
                            a['qty'] += qty
                            if a['qty'] > product.balance:
                                a['qty'] -= qty
                else:
                    cart.append({'name': product.pk, 'qty': qty})
                self.request.session['cart'] = cart
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('shop:index')


class CartView(ListView):
    template_name = 'cart_view.html'
    context_object_name = 'cart'

    def get_queryset(self):
        cart = self.request.session.get('cart')
        context = []
        if not cart:
            return context
        for a in cart:
            product = get_object_or_404(Product, pk=a['name'])
            product.balance = a['qty']
            context.append(product)
        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        sum_product = []
        susm = []
        for i in context['cart']:
            sum_product.append(i.balance * i.price)
            susm.append({'product_id': i.pk, 'sum_price': (i.balance * i.price)})
        context['sums'] = susm
        sum_product = sum(sum_product)
        context['sum_product'] = sum_product
        context['form'] = OrderForm()
        return context


class DeleteCart(DeleteView):
    success_url = reverse_lazy('shop:cart')

    def get(self, request, *args, **kwargs):
        cart = self.request.session.get('cart')
        pk = self.kwargs.get('pk')
        for a in cart:
            if pk == a['name']:
                cart.remove(a)
        self.request.session['cart'] = cart
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('shop:cart')


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('shop:index')

    def form_valid(self, form):
        user = self.request.user
        order = form.save(commit=False)
        if user.is_authenticated:
            order.user = user
        order = form.save()

        cart = self.request.session.get('cart')
        context = []
        if not cart:
            return context
        for a in cart:
            product = get_object_or_404(Product, pk=a['name'])
            product.balance = a['qty']
            context.append(product)

        for i in context:
            OrderProduct.objects.create(product=i, balance=i.balance, order=order)
            for a in cart:
                if i.pk == a['name']:
                    cart.remove(a)
                product = get_object_or_404(Product, pk=a['name'])
                product.balance -= i.balance
                product.save()
        self.request.session['cart'] = cart

        phone = form.instance.phone
        name = form.instance.name
        adress = form.instance.address

        telegram_send.send(messages=[f"""Новый заказ:
            Имя: {name},
            Телефон: {phone},
            Адресс: {adress}"""])


        # bot = telebot.TeleBot('5734377640:AAHZgjRRicZjNdfxX-2dc2ogSVG8Mcx0esk')
        #
        # @bot.message_handler(commands=["start"])
        # def start(m, res=False):
        #     bot.send_message(m.chat.id, f"""Новый заказ:
        #     Имя: {name},
        #     Телефон: {phone},
        #     Адресс: {adress}""")
        #
        # bot.polling(none_stop=True, interval=0)

        return HttpResponseRedirect(self.success_url)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_listview.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
