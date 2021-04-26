from django.shortcuts import render,reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from home.models import Categories, Contacts
from threads.models import Discussions
# Q objects can be used with boolean & (and) or | (or) statements to have multiple conditions expressed within a single lookup.
from django.db.models import Q

from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# Create your views here.
# Home page
def home(request):
    title = "Home"
    active_home = "active"
    allCategories = Categories.objects.all()
    context = {'allCategories' : allCategories, 'title' : title , 'active_home' : active_home}
    return render(request, "home/home.html",context)
    # return render(request, "home/home.html",{'title':title, 'active_home': active_home})

# About Page
def about(request):
    title = "About"
    active_about = "active"
    return render(request, "home/about.html",{'title':title, 'active_about': active_about})

# Contact Page
def contacts(request):
    title = "Contact Us"
    active_contacts = "active"
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']

        if len(name)<2 or len(email)<4 or len(phone)<10 or len(desc)<3:
            messages.error(request, 'Please fill the form correctly')
        else:      
            contact = Contacts(name= name , email=email,phone= phone,desc=desc)
            contact.save()
            messages.success(request, 'Your form has been successfully filled.')
    return render(request, "home/contacts.html",{'title':title, 'active_contacts': active_contacts})

def search(request):
    if request.method == 'GET':
        query= request.GET.get('query')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(queTitle__icontains=query) | Q(queDesc__icontains=query)

            results= Discussions.objects.filter(lookups).distinct()

            context={'results': results,
                    'query' : query,
                     'submitbutton': submitbutton}

            return render(request, 'home/search.html', context)

        else:
            return render(request, 'home/search.html')

    else:
        return render(request, 'home/search.html')


# HAndle the signup Or Create an account 
def signupHandle(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists! Try a different username.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        elif password == cpassword:
            user = User.objects.create_user(username,email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request,'Your account has been successfully created !')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    else:
        # return render(request,"home/home.html")
        # return to the previous page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

# Login

def loginHandle(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        
        user = authenticate(request, username=username, password=password)

        # If user object is returned, log in and route to current page
        if user:
            login(request, user)
            messages.success(request,'You have been successfully logged in !')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        # Otherwise, rthrow an error on current page
        else:
            messages.error(request, 'Invalid credentials. Please try again !')
            # return render(request, "home/home.html")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    else:
        return render(request,"home/home.html")  

# Logout Handle
def logoutHandle(request):
    
    logout(request)
    messages.success(request,'You have been logged out !')
    # return render(request, "home/home.html") 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))   

# password reset
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "home/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ("main:homepage")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="home/password/password_reset.html", context={"password_reset_form":password_reset_form})