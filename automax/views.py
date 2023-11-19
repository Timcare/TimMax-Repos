from importlib import reload
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Listing
from .forms import ListingForm,LocationForm,ProfileForm,UserForm
from django.contrib import messages
from .filters import ListingFilters
from django.views import View
from .models import LinkedListing
from django.core.mail import send_mail
# Create your views here.
def main(request):
    return render(request,"views/main.html",{"name":"automax"})
    
@login_required
def home(request):
    listing=Listing.objects.all()
    listing_filters=ListingFilters(request.GET,queryset=listing)
    user_liked_listing=LinkedListing.objects.filter(profile=request.user.profile).values_list('listing')
    linked_listing_ids=[l[0] for l in user_liked_listing]
    return render(request,"views/home.html",{'listing':listing,'listing_filters':listing_filters,'linked_listing_ids':linked_listing_ids})

@login_required
def list(request):
    if request.method == 'POST':
        try:
            listing_form=ListingForm(request.POST,request.FILES)
            location_form=LocationForm(request.POST)
            if listing_form.is_valid() and location_form.is_valid():
                listing=listing_form.save(commit=False)
                listing_location=location_form.save()
                listing.seller=request.user.profile
                listing.location=listing_location
                listing.save()
                messages.info(request,f'{listing.model} posted successfully')
                return redirect('home')
            else:
                 raise Exception()
        except Exception as e:
            messages.error(request,"An error occur while posting the listing")
    else:
        if request.user.first_name=="":
            messages.error(request,'Update your profile')
            return redirect('profile')
        else:
            listing_form=ListingForm()
            location_form=LocationForm()
        
    return render(request,"views/listing.html",{'listing_form':listing_form,'location_form':location_form})

@login_required
def listing_view(request,id):
    try:
        listing=Listing.objects.get(id=id)
        if listing is None:
            raise Exception()
        return render(request,"views/listings.html",{"listing":listing})
    except Exception as e:
        messages.error(request,f"Invalid request")
        return redirect("home")

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def post(self,request):
        try:
            user_listing=Listing.objects.filter(seller=request.user.profile)
            user_liked_listing=LinkedListing.objects.filter(profile=request.user.profile).all()
            profile_form=ProfileForm(request.POST,request.FILES,instance=request.user.profile)
            user_form=UserForm(request.POST,instance=request.user)
            location_form=LocationForm(request.POST,instance=request.user.profile.location)
            if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
                user_form.save()
                profile_form.save()
                location_form.save()
                messages.success(request,'Profile Updated Successfully')
            else:
                raise Exception()
        except Exception as e:
            messages.error(request,"An error just occured")
        return render(request,"views/profile.html",{"profile_form":profile_form,"user_form":user_form,
        "location_form":location_form,"user_listing":user_listing,'user_liked_listing':user_liked_listing})
    def get(self,request):
        user_listing=Listing.objects.filter(seller=request.user.profile)
        user_liked_listing=LinkedListing.objects.filter(profile=request.user.profile).all()
        profile_form=ProfileForm(instance=request.user.profile)
        user_form=UserForm(instance=request.user)
        location_form=LocationForm(instance=request.user.profile.location)
        return render(request,"views/profile.html",{"profile_form":profile_form,"user_form":user_form,
        "location_form":location_form,"user_listing":user_listing,'user_liked_listing':user_liked_listing})

@login_required
def edit_view(request,id):
    try:
        listing=Listing.objects.get(id=id)
        if listing is None:
            raise Exception()
        if request.method=="POST":
            listing_form=ListingForm(request.POST,request.FILES,instance=listing,)
            location_form=LocationForm(request.POST,instance=listing.location,)
            if listing_form.is_valid() and location_form.is_valid():
                listing_form.save()
                location_form.save()
                messages.success(request,'You list has been successfully updated')
                return redirect('home')
            else:
                messages.error(request,'An error occur why updating your list')
                return reload()
        else:
            listing_form=ListingForm(instance=listing)
            location_form=LocationForm(instance=listing.location)
        return render(request,'views/edit.html',{'listing_form':listing_form,'location_form':location_form})

    except Exception as e:
        messages.error(request,'An error occur why updating your list')
        return redirect('home')

@login_required
def like_listing_view(request,id):

    listings=get_object_or_404(Listing,id=id)

    liked_listing,created=LinkedListing.objects.get_or_create(profile=request.user.profile,listing=listings)
    if  not created:
        liked_listing.delete()
    else:
        liked_listing.save()
    return JsonResponse({'is_liked_by_user':created})


@login_required
def inquire_listing_using_email(request, id):
    listing=get_object_or_404(Listing,id=id)
    try:
        emailSubject=f'{request.user.username} is interested in {listing.model}'
        emailMessage=f'Hi {listing.seller.user.username}, {request.user.username} is interested in your {listing.model} on TimMax'
        send_mail(emailSubject,emailMessage,'noreply06@gmail.com',[listing.seller.user.email,],fail_silently=True)
        return JsonResponse({
            'success':True,
        })
    except Exception as e:
        return JsonResponse({
            'success':False,
            'info':e,
        })




