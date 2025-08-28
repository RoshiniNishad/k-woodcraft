from django.shortcuts import render ,get_object_or_404 ,redirect
from .models import Product  ,ContactMessage
from django.contrib import messages
from .forms import ContactForm ,PaymentForm
from django.contrib.auth.decorators import login_required
from .models import Cart
from .models import Product , Payment




def home(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'views/home.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'views/product_detail.html', {'product': product})

def living_room(request):
    products = Product.objects.filter(category='living').order_by('-created_at')
    return render(request, 'views/living_room.html', {'products': products})

def bedroom(request):
    products = Product.objects.filter(category='bedroom').order_by('-created_at')
    return render(request, 'views/bedroom.html', {'products': products})

def dining_kitchen(request):
    products = Product.objects.filter(category='dining').order_by('-created_at')
    return render(request, 'views/dining_kitchen.html', {'products': products})

def about(request):
    return render(request, 'views/about.html', {'active_page': 'about'})

def contact_view(request):
    active_page = 'contact'  # for menu highlighting

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save to ContactMessage model
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # reload page to clear form
        else:
            messages.error(request, "There was an error. Please check your input.")
    else:
        form = ContactForm()

    return render(request, 'views/contact.html', {
        'form': form,
        'active_page': active_page
    })



@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, "views/cart.html", {"cart_items": cart_items, "total": total,  "active_page": "cart"})

def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "⚠️ Please login to purchase items.")
        return redirect('login')   # redirect to login page

    product = get_object_or_404(Product, pk=pk)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect("cart")


@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("cart")

@login_required
def update_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated.")
        else:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
    return redirect("cart")




def payment_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = 1  # assuming single product checkout; adjust if multiple
    subtotal = product.price * quantity
    total_amount = subtotal
    advance_required = total_amount / 2  # 50% of total

    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES, total_amount=total_amount)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.product = product
            payment.total_amount = total_amount
            payment.remaining_amount = total_amount - payment.advance_payment
            payment.save()
            messages.success(
                request, 
                f"Payment successful! Remaining balance: ₹{payment.remaining_amount}"
            )
            return redirect("payment_success", pk=payment.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PaymentForm(total_amount=total_amount)

    return render(request, "views/payment.html", {
        "form": form,
        "product": product,
        "quantity": quantity,
        "subtotal": subtotal,
        "total_amount": total_amount,
        "advance_required": advance_required,
    })



def payment_success(request, pk):
    payment = get_object_or_404(Payment, pk=pk, user=request.user)
    return render(request, "views/success.html", {"payment": payment})



def cart_checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    half_total = total_amount / 2  # use float for accurate 50%

    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            advance = form.cleaned_data['advance_payment']

            if advance < half_total:
                messages.error(request, f"❌ Advance payment must be at least 50% of total (₹{half_total:.2f}).")
            else:
                # ✅ Successful payment
                messages.success(
                    request,
                    f"✅ Thank you for your Order! You have paid ₹{advance:.2f}. "
                    f"Remaining amount ₹{total_amount - advance:.2f}. "
                    "You will get further information regarding your Order soon."
                )
                # Clear the cart after checkout
                cart_items.delete()
                form = PaymentForm()  # reset form
    else:
        form = PaymentForm()

    return render(request, "views/payment.html", {
        "cart_items": cart_items,
        "total_amount": total_amount,
        "half_total": half_total,
        "form": form,
    })