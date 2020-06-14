from django.shortcuts import render,redirect
from django.contrib import messages

from .models import PizzaModel,SignUpModel,OrderModel

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

def adminloginview(request):
    return render(request,"adminlogin.html")


def authenticateadmin(request):
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(username=username,password=password)

    if user is not None:
        login(request,user)
        return redirect("adminhomepage")
    
    if user is None:
        messages.add_message(request,messages.ERROR,"Invalid Credentials")
        return redirect("adminloginpage")


def adminhomepageview(request):
    if not request.user.is_authenticated:
        return redirect("adminloginpage")
    context={"pizzas":PizzaModel.objects.all()}
    return render(request,'adminhomepage.html',context)


def adminlogout(request):
    logout(request)
    return redirect("adminloginpage")


def addpizza(request):
    name=request.POST['pizza']
    price=request.POST['price']

    PizzaModel(name=name,price=price).save()
    return redirect('adminhomepage')


def deletepizza(request,pizzapk):
    PizzaModel.objects.filter(id=pizzapk).delete()
    return redirect('adminhomepage')


def homepageview(request):
    
    return render(request,"index.html")


def usersignup(request):
    username=request.POST['username']
    password= request.POST['password']
    phone=request.POST['phone']
    if User.objects.filter(username=username).exists():
        messages.add_message(request,messages.ERROR,"User Already exits")
        return redirect("homepage")
    
    User.objects.create_user(username=username,password=password).save()

    lastobject=len(User.objects.all())-1
    SignUpModel(id=User.objects.all()[int(lastobject)].id,phone=phone).save()
    messages.add_message(request,messages.ERROR,"User Account Successfully Created")
    return redirect("homepage")
    
    """ulist=[]
    model=SignUpModel.objects.all()
    for user in model:
        ulist.append(user.username)
    
    if(username in ulist):
        messages.add_message(request,messages.ERROR,"User Already exits")
        return redirect("homepage")
    
    if(username not in ulist):
        SignUpModel(username=username,password=password,phone=phone).save()
        messages.add_message(request,messages.ERROR,"User Account Successfully Created")

        return redirect('homepage')"""

def userlogin(request):
    return render(request,"login.html")

def loginauthenticate(request):
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(username=username,password=password)

    if user is not None:
        login(request,user)
        return redirect("userhomepage")
    
    if user is None:
        messages.add_message(request,messages.ERROR,"Invalid Credentials")
        return redirect("userlogin")
    
    
    
    """user=SignUpModel.objects.all()
    data={}
    for i in user:
        data[i.username]=i.password
    #if login credential is correct
    if(username in data.keys() and password==data[username]):
        
        return redirect("userhomepage",pk=username)   
    else:
        messages.add_message(request,messages.ERROR,"Invalid Credential")
        return redirect("login")"""


def userhomepage(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    data=request.user.username
    context={"username":data,"pizzas":PizzaModel.objects.all()}
    return render(request,"userhomepage.html",context)

def userlogout(request):
    logout(request)
    return redirect("homepage")



def placeorder(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    username=request.user.username
    phone=""
    d=SignUpModel.objects.all()
    #(userid=request.user.id)
    for i in d:
        if(i.id==request.user.id):
            phone+=i.phone
    address=request.POST['address']
    ordereditems=""
    for pizza in PizzaModel.objects.all():
        pizzaid=pizza.id
        name=pizza.name 
        price=pizza.price 
        quantity=request.POST.get(str(pizzaid)," ")

        if str(quantity)!="0" and str(quantity)!=" ":
            ordereditems=ordereditems+name+" "+ " Price : "+str(int(price)*int(quantity)) + " Quantity : "+quantity+" "
        
        #print(pizzaid)
        #print(name)
        #print(price)
        #print(quantity)

    #print(username)
    #print(phone)
    #print(address)
    #print(ordereditems)
    OrderModel(username=username,phone=phone,address=address,ordereditems=ordereditems).save()
    messages.add_message(request,messages.ERROR,"Your Order Successfully Placed")
    return redirect("userhomepage")

    


def myorder(request):
    data=OrderModel.objects.filter(username=request.user.username)
    context={"orders":data}
    return render(request,"myorder.html",context)



def adminorders(request):
    orders=OrderModel.objects.all()
    context={"orders":orders}
    return render(request,"adminorders.html",context)

def acceptorder(request,orderpk):
    order=OrderModel.objects.filter(id=orderpk)[0]
    order.status="accepted"
    order.save()
    return redirect(request.META['HTTP_REFERER'])

def declineorder(request,orderpk):
    order=OrderModel.objects.filter(id=orderpk)[0]
    order.status="declined"
    order.save()
    return redirect(request.META['HTTP_REFERER'])