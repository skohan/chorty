from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, Url
from .forms import UrlShorteningForm, UserRegistrationForm

# Create your views here.
'''
Login is already done by django
'''
def index(request):
    return render(request, 'shorty/index.html')


def signup(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.filter(username=username).first()   
            profile = Profile(user=user)
            profile.save()
            message = "Account has been created, " + username + "!"
            messages.success(request, message)
            return redirect('/login')

    else:
        form =  UserRegistrationForm()

    return render(request, 'shorty/signup.html', {'form': form})


@login_required()
def home(request):
    user =  request.user

    profile = Profile.objects.filter(user= user).first()

    
    if request.method == 'POST':
        if profile.no_of_urls < 10 or (profile.is_premium and profile.no_of_urls < 20):
            form = UrlShorteningForm(request.POST)

            if form.is_valid():
                form = form.save(commit=False)
                print(form.url)
                form_url = Url.objects.all().filter(slug=form.slug).first()
                if form_url != None :
                    if form_url.user != user:
                        messages.warning(request,"Already exist :(")   
                    else:
                        form_url.url = form.url
                        form_url.save()
                        messages.success(request,"Updated Url!") 
                else:
                    form.user = user
                    form.save()
                    profile.no_of_urls += 1
                    profile.save()
                    messages.success(request,"Shortned the Url!")            
            
            else:
                messages.warning(request,"Problem in input you have given. Please enter valid values.")

        else:
            messages.warning(request, "You have reached the free limit of 10 urls! Premium service coming soon...")
    
    print(user)
    urls = Url.objects.filter(user = user).order_by('slug')
    profile = Profile.objects.filter(user=user).first()
    print(profile)
    context = {
        'urls' : urls,
        'profile': profile,
        'form' : UrlShorteningForm()
    }
    return render(request, 'shorty/home.html', context=context)

@login_required
def delete(request, slug):
    user = request.user
    profile = Profile.objects.filter(user= user).first()

    if request.method == 'POST':
        url = Url.objects.all().filter(slug=slug).first()
        print(user)
        print(url.user)

        if user == url.user:
            url.delete()
            profile.no_of_urls -= 1
            profile.save()
            message = "Successfully deleted url!"
        else:
            message = "You don't own this url to delete!"
        messages.success(request = request, message=message) 
        return redirect(request.META['HTTP_REFERER'])
    
    return redirect('home')
        

def slug_redirect(request, slug):
    print(slug)
    url = Url.objects.all().filter(slug=slug).first()

    if url is not None:
        return redirect(url.url)
    
    return render(request, 'shorty/not_found.html')


