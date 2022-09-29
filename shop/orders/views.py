from cart.cart import Cart

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created, order_to_stock


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         books=item['book'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # send email
            order_created.delay(order.id)
            order_to_stock.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            messages.success(request, f'Заказ с номером {order.id} будет скоро обработан')
            return redirect(reverse('shop:book_list'))
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})
