from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from orders.models import Order
from django.urls import reverse

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('shop:list')
                else:
                    HttpResponse('okay, not bad')
            else:
                HttpResponse('ivalid login!')
    else:
        form = LoginForm()
    return render(request,'account/registration/login.html',{'form':form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,'account/register_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form':user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                      'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

@login_required
def profile(request):
    profile = request.user.profile
    return render(request,'account/profile.html',{'user':request.user,'profile':profile})


@login_required
def order_list(request):
    orders = Order.objects.filter() 
    order_data = []
    for order in orders:
        
            order_data.append({
                'id': order.id,
                'first_name': order.first_name,
                'last_name': order.last_name,
                'email': order.email,
                'address': order.address,
                'postal_code': order.postal_code,
                'city': order.city,
                'paid': order.paid,
                'created': order.created.strftime('%d/%m/%Y'),
                'updated': order.updated.strftime('%d/%m/%Y'),
                'order_pdf': reverse('orders:admin_order_pdf', args=[order.id])
            })
    return JsonResponse({'orders': order_data})



