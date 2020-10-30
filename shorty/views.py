from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Url
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
            message = "Account has been created, " + username + "!"
            messages.success(request, message)
            return redirect('/login')

    else:
        form =  UserRegistrationForm()

    return render(request, 'shorty/signup.html', {'form': form})


@login_required()
def home(request):
    user =  request.user

    if request.method == 'POST':
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
                messages.success(request,"Shortned the Url!")            
        
        else:
            messages.warning(request,"Problem in form")
    
    
    urls = Url.objects.filter(user = user).order_by('slug')
    
    context = {
        'urls' : urls,
        'form' : UrlShorteningForm()
    }
    return render(request, 'shorty/home.html', context=context)


def slug_redirect(request, slug):
    print(slug)
    url = Url.objects.all().filter(slug=slug).first()

    if url is not None:
        return redirect(url.url)
    
    return render(request, 'shorty/not_found.html')


