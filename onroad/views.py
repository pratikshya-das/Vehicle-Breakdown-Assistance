from django.shortcuts import get_object_or_404, redirect, render 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.generic import CreateView, ListView, UpdateView,TemplateView
from .filters import RoadFilter
import hashlib
from hashlib import md5
import string
import hmac
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .forms import UserSignUpForm, ShopSignUpForm,BusinessCreate,FeedbackCreate,UserForm,ResetpasswordForm,ForgetpasswordForm,MapCreate,PayCreate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from .models import *
from django.contrib.auth import get_user_model
import datetime
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None :
            if user.is_mechanic:
                auth.login(request,user)
                return redirect('shop_home')
            else:
                auth.login(request,user)
                return redirect('home')
            
       
        else:
            return render (request,'onroad/login.html', {'error':'Username or password is incorrect!'})
    else:
    
        return render(request,'onroad/login.html')
        
 
def logout(request):
  
    return redirect('index') 

def home(request):
   
    return render(request, 'onroad/home.html')

def shop_home(request):
   
    return render(request, 'onroad/shop_home.html')
def main(request):
    return render(request, 'onroad/main.html')                
def index(request):
    return render(request, 'onroad/index.html')
    
def upload(request):
        upload = BusinessCreate(initial={'loggeduser': request.user.username,
        'status':'pending'})
        if request.method == 'POST':
                upload = BusinessCreate(request.POST, request.FILES)
                if upload.is_valid():
                    upload.save()
                    
                    return redirect('shop_home')
                else:
                    return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
        else:
            return render(request, 'onroad/upload_business.html', {'upload_form':upload})
            
def view_business(request):
    username=request.user.username
    shelf = Business.objects.filter(loggeduser =username).order_by('-id')
    if not shelf:
     
       return render (request,'onroad/view_business.html', {'error':'there is no business created by you'})
    
    else :
       
         return render(request, 'onroad/view_business.html', {'shelf': shelf})


def view_feedback(request):
    username=request.user.username
    shelf1 = Feedback.objects.filter(feedcreateuser =username).order_by('-id')
    if not shelf1:
     
       return render (request,'onroad/view_feedback.html', {'error':'there is no feedback created by you'})
    
    else :
       
         return render(request, 'onroad/view_feedback.html', {'shelf': shelf1})
def getgeo(request):
        map_form = MapCreate()
        sel = Business.objects.get(id =request.COOKIES['business_id'])
        if request.method == "POST":
           map_form = MapCreate(request.POST or None, instance=sel)    
          
           if map_form.is_valid():
              new_author = map_form.save(commit=False)
              new_author.latitude=request.COOKIES['latitude']
              new_author.longitude=request.COOKIES['longitude']
              new_author.save()
           return redirect('view_business')
        else:
           return render(request, 'onroad/get_geolocation.html', {'map_form':map_form})  
           
def showgeo(request,business_id):
    business_id = int(business_id)
    showgeo = Business.objects.get(id = business_id)
    showlat=request.COOKIES['showlat']
    showlan=request.COOKIES['showlan']
    context = {"showgeo":showgeo, 
		"showlat": showlat,"showlan": showlan}
    return render(request, 'onroad/show_geolocation.html', context) 
              
                  
                   
def all_business_details_full(request,business_id):
    business_id = int(business_id)
    full_view = Business.objects.get(id = business_id)
   
    return render(request, 'onroad/all_business_details_full.html', {'getbusiness': full_view})          
    
def mechanic_payment(request):
    username=request.user.username
    getpay = Payment.objects.filter(payuser =username).order_by('-id')
    if not getpay:
       return render (request,'onroad/mechanic_payment.html', {'error':'there is no amount credited! '})
    
    else :
       
         return render(request, 'onroad/mechanic_payment.html', {'getpay': getpay})

    
def my_payment(request):
    username=request.user.username
    getpay = Payment.objects.filter(loggeduser =username).order_by('-id')
    if not getpay:
       return render (request,'onroad/my_payment.html', {'error':'there is no payment done yet! '})
    
    else :
       
         return render(request, 'onroad/my_payment.html', {'getpay': getpay})
   
def my_feedback(request):
    username=request.user.username
    getfeed = Feedback.objects.filter(loggeduser =username).order_by('-id')
    if not getfeed:
       return render (request,'onroad/my_feedback.html', {'error':'there is no Feedback '})
    
    else :
       
         return render(request, 'onroad/my_feedback.html', {'getorder': getfeed})
def adminlogin(request):
    return redirect('admin')
             
def soldorder(request):
    

         return render(request, 'onroad/soldorder.html')
    
def checkplaceorder(request):
    
         return render (request,'onroad/home.html')
           
def upload_feedback(request):
    cookies=request.COOKIES['business_user']
    data = Business.objects.filter(loggeduser=request.COOKIES['business_user'])
    feedback_form = FeedbackCreate(initial={'loggeduser': request.user.username,'feedcreateuser': request.COOKIES['business_user']})
    if request.method == 'POST':
        feedback_form = FeedbackCreate(request.POST, request.FILES)
           
        if feedback_form.is_valid():
           
            feedback_form.save()
            messages.success(request,('Your feedback was successfully updated!'))
            return redirect('home')   
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    
     
        
            
    else:
            return render(request, 'onroad/upload_feedback.html',{'feedback_form':feedback_form,'cookies': cookies})
          
    
def upload_pay(request):
    cookies=request.COOKIES['pay_user']
    data = Business.objects.filter(loggeduser=request.COOKIES['pay_user'])
    pay_form = PayCreate(initial={'loggeduser': request.user.username,'payuser': request.COOKIES['pay_user']})
    if request.method == 'POST':
        pay_form = PayCreate(request.POST, request.FILES)
           
        if pay_form.is_valid():
           
            pay_form.save()
            messages.success(request,('Your payment was successfully debited!'))
            return redirect('home')   
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
             
    else:
            return render(request, 'onroad/upload_payment.html',{'pay_form':pay_form,'cookies': cookies})
          
      
def update_business(request, business_id):
    business_id = int(business_id)
    try:
        business_sel = Business.objects.get(id = business_id)
    except Business.DoesNotExist:
        return redirect('shop_home')    
    business_form = BusinessCreate(request.POST or None, instance = business_sel)
    if business_form.is_valid():
        business_form.save()
        return redirect('view_business')
    return render(request, 'onroad/update_business.html', {'upload_form':business_form})

def delete_business(request, business_id):
    business_id = int(business_id)
    try:
        business_sel = Business.objects.get(id = business_id)
    except Business.DoesNotExist:
        return redirect('shop_home')
    business_sel.delete()
    return redirect('view_business')
    




   
def createorder(request):  
   
           
            return render(request, 'onroad/order_food.html')
            
def forget_password(request):
    
    if request.method == 'POST':
       
        if User.objects.get(answer1=request.POST['answer1']) :
        
            return redirect('reset_password')
        else:
          
             return render (request,'onroad/forget_password.html', {'error':'Your answer is incorrect!'})
            
       
    return render(request,'onroad/forget_password.html')
          
def reset_password(request):
     
      try:
            data = User.objects.get(answer1=request.COOKIES['answer1'])
      except User.DoesNotExist:
             messages.success(request,('There is no user'))
      reset_form = ResetpasswordForm(request.POST or None, instance = data)
      if reset_form.is_valid():
         new_author = reset_form.save(commit=False)
        
         hash = hmac.new(b'key',new_author, md5).hexdigest()
        
         hash.save()
         return redirect('login')
      return render(request, 'onroad/reset_password.html', {'reset_form':reset_form})
       

def userpage(request):
	if request.method == "POST":
		user_form = UserForm(request.POST, instance=request.user)
		
		if user_form.is_valid():
		    user_form.save()
		    messages.success(request,('Your profile was successfully updated!'))
	
		else:
		    messages.error(request,('Unable to complete request'))
		
	user_form = UserForm(instance=request.user)
	
	return render(request = request, template_name ="onroad/user.html", context = {"user":request.user, 
		"user_form": user_form})
def business_user(request):
	if request.method == "POST":
		user_form = UserForm(request.POST, instance=request.user)
		
		if user_form.is_valid():
		    user_form.save()
		    messages.success(request,('Your profile was successfully updated!'))
	
		else:
		    messages.error(request,('Unable to complete request'))
		
	user_form = UserForm(instance=request.user)
	
	return render(request = request, template_name ="onroad/business_user.html", context = {"user":request.user, 
		"user_form": user_form})
        
def all_business_details(request):
    getallcity=Business.objects.all()
    city_filter = request.GET.get('city')
     
    f = RoadFilter(request.GET, queryset=Business.objects.filter(status ='approved').order_by('-id'))
   
   
    return render(request, 'onroad/all_business_details.html', {'filter': f,'getallcity':getallcity})
  
 
class SignUpView(TemplateView):
    template_name = 'onroad/main.html'



    

class ShopSignUpView(CreateView):
    model = User
    form_class = ShopSignUpForm
    template_name = 'onroad/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'shop'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('shop_home')

class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'onroad/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'user'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('home')


        
    
