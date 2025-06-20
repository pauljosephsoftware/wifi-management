# views.py
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import SubscriberProfile
from django.contrib.auth import login
from .models import*
from django.shortcuts import get_object_or_404, redirect
from .models import Payment
from django.http import JsonResponse
from mpesa import Auth, STKPush
from django.views.decorators.http import require_POST
from decouple import config
from django.http import JsonResponse


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
    plan = get_object_or_404(ServicePlan, id=plan_id)
    profile = request.user.subscriberprofile
    profile.activate_plan(plan)
    return redirect('dashboard')

#payment component of the application


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                
            )

        
        # Save profile manually
            
            profile = user.subscriberprofile
            profile.mac_address = form.cleaned_data['mac_address']
            profile.ip_address = form.cleaned_data['ip_address']
            profile.save()
            login(request, user)  # Optional auto-login
            return redirect('dashboard')  # Change to your landing view
    else:
        form = UserRegistrationForm()
    return render(request, 'subscription/register.html', {'form': form})


@login_required
def manage_profile(request):
    profile = request.user.subscriberprofile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile, user=request.user)
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