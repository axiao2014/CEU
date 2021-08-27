from django.shortcuts import render, redirect
from ceuApp.models import *
import bcrypt
from django.views.generic.base import TemplateView
from django.http.response import JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
import stripe
from django.conf import settings

# Create your views here.
from django.shortcuts import render, HttpResponse
def index(request):
    request.session.pop('my_courses', None)
    request.session.pop('courses', None)
    courses = []
    my_courses = []
    user_courses = []
    if 'user_id' in request.session:
        user_courses = User.objects.get(id=request.session['user_id']).courses.all()
    for x in Course.objects.all():
        course = {
            'name': x.name,
            'desc': x.desc,
            'date': str(x.date),
            'start_time': x.start_time.strftime('%#I:%M %p'),
            'end_time': x.end_time.strftime('%#I:%M %p'),
            'unit': x.unit,
            'price': str(x.price),
            'id': x.id,
        }
        if x in user_courses:
            my_courses.append(course)
        else:
            courses.append(course)
    request.session['courses'] = courses
    if 'user_id' in request.session:
        request.session['admin'] = User.objects.get(id=request.session['user_id']).admin
    if len(my_courses) > 0:
        request.session['my_courses'] = my_courses
    return render(request, "course.html")

def register(request):
    if 'user_id' in request.session:
        return redirect('/')
    if request.method == 'POST':
        rq = request.POST
        errors = User.objects.basic_validator(request.POST)
        email_check = User.objects.filter(email=rq['email'])
        username_check = User.objects.filter(username=rq['username'])
        license_check = User.objects.filter(lnum=rq['lnum'])
        if email_check:
            errors['email_check'] = 'Email address already taken.'
        if username_check:
            errors['username_check'] = 'Username already taken.'
        if license_check:
            errors['license_check'] = 'License number already taken.'
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        password = rq['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(fname=rq['fname'],lname=rq['lname'],lnum=rq['lnum'],lexpire=rq['lexpire'],ltype=rq['ltype'],lboard=rq['lboard'],email=rq['email'],username=rq['username'],password=pw_hash)
        request.session['user_id'] = user.id
        return redirect('/')
    return render(request, "register.html")

def login(request):
    if 'user_id' in request.session:
         return redirect('/')
    if request.method == 'POST':
        rq = request.POST
        errors = {}
        user = User.objects.filter(username=rq['username'])
        if not user:
            errors['login_error'] = 'Incorrect username or password.'
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')
        logged_user = user[0]
        if bcrypt.checkpw(rq['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/')
        else:
            errors['login_error'] = 'Incorrect email or password.'
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')
    return render(request, "login.html")

def create(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        rq = request.POST
        Course.objects.create(name=rq['name'],desc=rq['desc'],date=rq['date'],start_time=rq['start_time'],end_time=rq['end_time'],unit=rq['unit'],price=rq['price'])
        return redirect('/')
    return render(request, 'create.html')

def destroy(request, course_id):
    if 'user_id' not in request.session:
        return redirect('/')
    course = Course.objects.get(id=course_id)
    course.delete()
    return redirect('/')

def logout(request):
    if 'user_id' not in request.session:
        return redirect('/')
    request.session.flush()
    return redirect('/login')

def add(request, course_id):
    if 'user_id' not in request.session:
        return redirect('/')
    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=request.session['user_id'])
    user.courses.add(course)
    user.save()
    return redirect('/')

def drop(request, course_id):
    if 'user_id' not in request.session:
        return redirect('/')
    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=request.session['user_id'])
    user.courses.remove(course)
    user.save()
    # return redirect('/')
    # return redirect('/add/%s' % course_id)
    context = {
        # 'course_added' : user.courses.get(id=course_id),
        'course_added' : user.courses.all(),
    }
    return redirect('/cart')

def contact(request):
    return render(request, 'contact.html')
    
def about(request):
    return render(request, 'about.html')

def home(request):
    return redirect('/')

def order():
    if 'user_id' in request.session:
         return redirect('/')
    if request.method == 'POST':
        rq = request.POST
        Order.objects.create(name=rq['ord_dt'])

def cart(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user_cart = User.objects.get(id=request.session['user_id'])
    total = 0
    unit = 0
    courses = user_cart.courses.all()
    for course in courses:
        total += course.price
        unit += course.unit
    print(total)
    print(unit)

    context = {
        # 'course_added' : user.courses.get(id=course_id),
        'course_added' : user_cart.courses.all(),
        'total' : total,
        'units' : unit,
    }
    return render(request, "add_to_cart.html", context)

def purchase(request):
    return render(request, 'purchase.html')

def cartpurchase(request):
    user_cart = User.objects.get(id=request.session['user_id'])
    courses = user_cart.courses.all()
    for course in courses:
        print(course)
        return(course)

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        user_cart = User.objects.get(id=request.session['user_id'])
        courses = user_cart.courses.all()
        try:
            
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'cart item',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '10000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def success(request):
    return render(request,'success.html')


def cancelled(request):
    return render(request, 'cancelled.html')

