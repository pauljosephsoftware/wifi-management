# views.py
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import SubscriberProfile, Payment
from django.contrib.auth import login
from .models import*
from django.shortcuts import get_object_or_404, redirect
from .models import Payment
from django.http import JsonResponse
from mpesa import Auth, STKPush
from django.views.decorators.http import require_POST
from decouple import config
from django.http import JsonResponse
from .utils import scan_networks, connect_to_network
from mpesa.urls import mpesa_urls
from mpesa import*
from django.urls import reverse
import requests


def welcome(request):
    return render(request, 'subscription/welcome.html')

@require_POST
def initiate_stk(request):
    phone = request.POST['phone']
    amount = request.POST['amount']

    # Authenticate using values populated via .env
    auth = Auth(
        consumer_key=None,  # passes through Config
        consumer_secret=None,
        base_url=None
    )
    auth_data = auth.get_access_token()
    token = auth_data.get('access_token')

    stk = STKPush(base_url=None, access_token=token)

    timestamp = stk.generate_timestamp()
    payload = stk.create_payload(
        BusinessShortCode=request.POST.get('short_code', '174379'),
        pass_key=request.POST.get('pass_key'),
        Timestamp=timestamp,
        TransactionType='CustomerPayBillOnline',
        Amount=amount,
        PartyA=phone,
        PartyB=request.POST.get('short_code', '174379'),
        PhoneNumber=phone,
        CallBackURL=request.build_absolute_uri('/mpesa/callback/'),
        AccountReference='REF123',
        TransactionDesc='ISP Subscription'
    )

    response = stk.send_stk_push(payload)
    return JsonResponse(response)
@login_required
def dashboard(request):
    profile, _ = SubscriberProfile.objects.get_or_create(user=request.user)
    return render(request, 'subscription/dashboard.html', {
        'user': request.user,
        'profile':profile,
    })
def plans(request):
    plans = ServicePlan.objects.all()
    return render(request, 'subscription/plans.html', {'plans':plans})


@login_required
def subscribe_to_plan(request, plan_id):
    plan = ServicePlan.objects.get(pk=plan_id)
    profile = request.user.subscriberprofile
    phone = request.user.subscriberprofile.phone_number
    
    stk_endpoint = request.build_absolute_uri(reverse('submit'))
    resp = requests.post(stk_endpoint, data={
        'amount': plan.price,
        'phone_number': request.user.subscriberprofile.phone_number,
        'account_number': f"Plan-{plan.id}",
    })
    return redirect('subscribe_success', plan_id=plan.id)
@login_required
def subscribe_success(request, plan_id):
    plan = ServicePlan.objects.get(pk=plan_id)
    return render(request, 'subscription/subscribe_success.html', {
        'plan': plan,
        'message': "STK Push sent! Check your phone to complete payment."
    })
# views.py
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'subscription/register.html', {'form': form})



@login_required
def manage_profile(request):
    profile = request.user.subscriberprofile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.subscriberprofile)
        if form.is_valid():
            form.save()
            return redirect('manage_profile')
    else:
        form = ProfileUpdateForm(instance=profile, initial={
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            
        }, user=request.user)
    return render(request, 'subscription/manage-profile.html', {'form': form})
@login_required
def profile_view(request):
    profile = request.user.subscriberprofile
    return render(request, "subscription/profile.html", {"profile": profile})


def available_networks(request):
    if request.method == 'POST':
        ssid = request.POST['ssid']
        password = request.POST.get('password','')
        success = connect_to_network(ssid, password)
        return render(request, 'subscription/networks_list.html', {
            'networks': scan_networks(),
            'message': f"Connected to {ssid}" if success else f"Failed to connect to {ssid}"
        })
    return render(request, 'subscription/networks_list.html', {
        'networks': scan_networks()
    
    })