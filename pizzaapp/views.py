from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import PizzaModel, CustomerModel, OrderModel

# Create your views here.
def adminlogin(request):
	return render(request, "pizzaapp/adminlogin.html")

def authenticateadmin(request):
	username = request.POST['username']
	password = request.POST['password']

	user = authenticate(username = username, password = password)

	# user exists
	if user is not None:
		login(request, user)
		return redirect('adminhomepage')

	# user doesn't exists
	if user is None:
		messages.add_message(request, messages.ERROR, "invalid credentials")
		return redirect('adminloginpage')


def adminhomepage(request):
	context = {'pizzas' : PizzaModel.objects.all()}
	return render(request, 'pizzaapp/adminhomepage.html',context)

def adminlogout(request):
	logout(request)
	return redirect('adminloginpage')

def addpizza(request):
	#write a code to add pizza in the databse
	name = request.POST.get('pizza')
	price = request.POST.get('price')
	PizzaModel(name	= name, price = price).save()
	return redirect('adminhomepage')

def deletepizza(request, pizzapk):
	PizzaModel.objects.filter(id = pizzapk).delete()
	return redirect('adminhomepage')

def homepage(request):
	return render(request, 'pizzaapp/homepage.html')

def signupuser(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	phoneno = request.POST.get('phoneno')

	#if username already exists
	if User.objects.filter(username = username).exists():
		messages.add_message(request, messages.ERROR, "user already exists")
		return redirect('homepage')

	#if username doesn't exist already(proceed to create user)
	User.objects.create_user(username=username,password=password).save()
	lastobject = len(User.objects.all())-1
	CustomerModel(userid = User.objects.all()[int(lastobject)].id,phoneno = phoneno).save()
	messages.add_message(request, messages.ERROR, "user successfully created")
	return redirect('homepage')

def userlogin(request):
	return render(request, "pizzaapp/userlogin.html")

def authenticateuser(request):
	username = request.POST['username']
	password = request.POST['password']

	user = authenticate(username = username, password = password)

	#if user exists
	if user is not None:
		login(request,user)
		return redirect('userhomepage')

	#if user doesn/t exist
	if user is None:
		messages.add_message(request,messages.ERROR,"invalid credentials")
		return redirect('loginuser')

def welcomeuser(request):
	if not request.user.is_authenticated:
		return redirect('loginuser')

	username = request.user.username
	context = {'username' : username, 'pizzas' : PizzaModel.objects.all()}
	return render(request,"pizzaapp/userwelcome.html",context)

def userlogout(request):
	logout(request)
	return redirect('loginuser')

def placeorder(request):
	if not request.user.is_authenticated:
		return redirect('loginuser')
	username = request.user.username
	phoneno = CustomerModel.objects.filter(userid = request.user.id)[0].phoneno
	address = request.POST['address']
	ordereditems = ""
	for pizza in PizzaModel.objects.all():
		pizzaid = pizza.id
		name = pizza.name
		price = pizza.price
		quantity = request.POST.get(str(pizzaid)," ")

		if str(quantity)!="0" and str(quantity)!=" ":
			ordereditems = ordereditems + name + " " + "price:"+ " "+str(int(price)*int(quantity)) + " " + "quantity : " + quantity + " "
	print(ordereditems)
	OrderModel(username = username, phoneno = phoneno, address = address, ordereditems = ordereditems).save()
	messages.add_message(request,messages.ERROR,"order successfully placed")
	return redirect('userhomepage')


def userorders(request):
	orders = OrderModel.objects.filter(username = request.user.username)
	context = {'orders' : orders}
	return render(request, 'pizzaapp/userorders.html',context)

def adminorders(request):
	orders = OrderModel.objects.all()
	context = {'orders' : orders}
	return render(request, 'pizzaapp/adminorders.html',context)

def acceptorder(request,orderpk):
	order = OrderModel.objects.filter(id = orderpk)[0]
	order.status = "Accepted"
	order.save()
	return redirect(request.META['HTTP_REFERER'])

def declineorder(request,orderpk):
	order = OrderModel.objects.filter(id = orderpk)[0]
	order.status = "Declined"
	order.save()
	return redirect(request.META['HTTP_REFERER'])
