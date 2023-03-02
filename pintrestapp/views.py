import random
from django.shortcuts import render,redirect,get_object_or_404, redirect
from .models import tag,userdetails,Like,Post
from .forms import postform
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator


# Create your views here.

@never_cache
def home(request):
    alldata = Post.objects.get_queryset().order_by('id')
    paginator = Paginator(alldata, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'home.html',{'alldata':page_obj})


@login_required(login_url='login')
def create(request):
    if request.method == 'GET':
        form = postform()
        return render(request,'create.html',{'form':form})
    else:
        form = postform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request,'create.html')
    
        
        
        
def update(request,id):
    if request.method == "GET":
        data = Post.objects.get(id=id)
        form = postform(instance=data)
        return render(request,'create.html',{'form':form})
    else:
        data = Post.objects.get(id=id)
        form = postform(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('home')
        
def delete(request,id):
    del_data = Post.objects.get(id= id)
    del_data.delete()
    return redirect('home')


def readmore(request,id):
    postid = Post.objects.get(id=id)
    return render(request, 'updatepost.html',{'post':postid})

@login_required(login_url='login')
def fullpost(request,id):
    fullp = Post.objects.get(id=id)
    b = random.randint(1,Post.objects.all().count())
    a = random.randint(1,Post.objects.all().count())
    c = random.randint(1,Post.objects.all().count())
    d = random.randint(1,Post.objects.all().count())
    e = random.randint(1,Post.objects.all().count())
    post2 =  Post.objects.filter(id__in=[a,b,c]).order_by("?")
    a1 = random.randint(1,Post.objects.filter(tag = fullp.tag).count())
    b1 = random.randint(1,Post.objects.filter(tag = fullp.tag).count())
    c1 = random.randint(1,Post.objects.filter(tag = fullp.tag).count())
    d1 = random.randint(1,Post.objects.filter(tag = fullp.tag).count())
    e1 = random.randint(1,Post.objects.filter(tag = fullp.tag).count())
    f1 = random.randint(1,Post.objects.filter(tag = fullp.tag).count())
    g1 = random.randint(1,Post.objects.filter(tag = fullp.tag).count())
    h1 = random.randint(1,Post.objects.filter(tag = fullp.tag).count())
    i1 = random.randint(1,Post.objects.filter(tag = fullp.tag).count())
    j1 = random.randint(1,Post.objects.filter(tag = fullp.tag).count())
    k1 = random.randint(1,Post.objects.filter(tag = fullp.tag).count())
    done=0
    postid = get_object_or_404(Post,id=id)
    if Like.objects.filter(Q(user = request.user) & Q(post = postid.id)):
        done = 1
    else:
        done = 0
    
    tagimage = Post.objects.filter(Q(tag = fullp.tag ) & Q(id__in=[a1,b1,c1,d1,e1,f1,g1,h1,i1,j1,k1])).order_by("?")
    return render(request,'fullpost.html',{'allpost':post2,'tagimage':tagimage,'post':postid,'done':done})


def tagpost(request,id):
    print(id)
    dd = tag.objects.get(id = id)
    tagimage = Post.objects.filter(tag=dd)
    # print("hello",tagpost1)
    return render (request,'fullpost.html',{'tagimage':tagimage})
    


        


def register(request):
    if request.method == 'POST':
        # name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confpassword = request.POST['confirmpassword']
        if password == confpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Exist')
                return redirect('register')
            
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Exists')
                return redirect('register')
            
            else:
                user = User.objects.create_user(email=email,password=password,username=username)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'password Not matching')
            return redirect('register')
    else:
        return render(request,'register.html')
    
@never_cache  
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username / Password is not matching')
            return redirect('login')
    else:
        return render(request,'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('home')

def search(request):
    inputsearch = request.post['inputsearch']
    searc = Post.objects.filter(title__contains = inputsearch)
    return render(request,'home.html',{'alldata':searc})
    

@login_required(login_url="login")
def profile(request):
    if request.user.is_authenticated:
        if userdetails.objects.filter(name__exact = request.user).exists():
            
            b = userdetails.objects.get(name__exact = request.user)
            return render(request,'profile.html',{'b':b})
        else:
            return redirect('adduserdata')
    else:
        return redirect('login')

def userpost(request):
    if request.user.is_authenticated:
        if userdetails.objects.filter(name__exact = request.user).exists():
            a = Post.objects.filter(uploadby = request.user)
            b = userdetails.objects.get(name__exact = request.user)
            return render(request,'userpost.html',{'form_a':a,'b':b})
        else:
            return redirect('profile')
    else:
        return redirect('login')
                
        
def adduserdata(request):
    if request.user.is_authenticated:
        if userdetails.objects.filter(name__exact = request.user).exists():
            return redirect('profile')
        else:
            if request.method == "POST":
                name = request.user
                profileimage = request.FILES['profileimage']
                phonenumber = request.POST['phonenumber']
                gender = request.POST['gender']
                
                userdata = userdetails(name=name,profileimage=profileimage,phonenumber=phonenumber,gender=gender)
                if len(phonenumber)>10:
                    return redirect('profile')
                else:
                    userdata.save()
                return redirect('profile')
            return render(request,'adduserdata.html')
    else:
        return redirect('login') 
    
    
def likepost(request,id):
    post = get_object_or_404(Post,id=id)
    like,created = Like.objects.get_or_create(user=request.user ,post=post)
    if not created:
        like.delete()
        post.likes -=1
    else: 
        post.likes +=1
        
    post.save()
    return redirect('readmore',id=id) 

        
      


        
        