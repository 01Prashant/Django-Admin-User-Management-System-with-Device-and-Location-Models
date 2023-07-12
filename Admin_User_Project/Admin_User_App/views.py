from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.contrib.auth.hashers import make_password, check_password
import random
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse



# Create your views here.
class SignupView(View):
    def get(self, request   ):
        return render(request,'signup.html')

    def post(self, request):
        firstName = request.POST.get('fname')
        lastName = request.POST.get('lname')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        password = request.POST.get('password')
        cpassword = request.POST.get('password2')

        email = email.lower()

        if User.objects.filter(email=email).exists():
            alert_message = 'Email already exists. Please use a different email.'
            return render(request, 'signup.html', {'alert_message': alert_message})
        
        if password != cpassword:
            return render(request, "signup.html", {'alert_message': "Password do not match. Please enter confirm password same as password."})
        
        password = make_password(password)

        if user_type == 'admin':
            User(email = email, first_name = firstName, last_name=lastName, password=password,user_type= user_type, is_active=True, is_staff=True, is_super=True).save()
        elif user_type == 'user':
            User(email = email, first_name = firstName, last_name=lastName, password=password,user_type= user_type, is_staff=True).save()
        else:
            return render(request, "signup.html", {'alert_message': "Please choose your user type."})

        return redirect('login')
    

class LoginView(View):
    def get(self, request):  
        return render(request,'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        email = email.lower()

        if User.objects.filter(email=email).exists():
            user_info = User.objects.get(email=email)
            if check_password(password, user_info.password):
                id = user_info.id
                print(id)
                request.session['id'] = id
                return redirect("display")
            return render(request, "login.html", {'alert_message': "Invalid email and password"})
        alert_message = 'Email does not exists. Please use a different email.'
        return render(request, 'login.html', {'alert_message': alert_message})

class ForgotView(View):
    def get(self, request   ):  
        return render(request,'forgot.html')
    
    def post(self, request):
        email = request.POST.get('email')
        email = email.lower()

        if User.objects.filter(email=email).exists():
            user_info = User.objects.get(email=email)

            id = user_info.id
            request.session['id'] = id

            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            print(otp)

            # Send the email
            subject = 'OTP Verification'
            message = f'Your OTP is: {otp}'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [email]
            send_mail(subject, message, from_email, to_email)

            return redirect('otp')

        alert_message = 'Email does not exists. Please enter a valid email.'
        return render(request, 'forgot.html', {'alert_message': alert_message})



class OTPView(View):
    def get(self, request):  
        id = request.session.get('id')
        otp = request.session.get('otp')
        if(otp == None):
            return redirect('home')
        if(id == None):
            return redirect('login')
        return render(request,'otp.html')
    
    def post(self, request):
        id = request.session.get('id')

        stored_otp = request.session.get('otp')
        entered_otp = f"{request.POST['otp1']}{request.POST['otp2']}{request.POST['otp3']}{request.POST['otp4']}{request.POST['otp5']}{request.POST['otp6']}"

        if int(entered_otp) == stored_otp:
            request.session.pop('otp', None)
            return redirect('reset')
        alert_message = 'Invalid OTP'
        context = {'id': id, 'alert_message': alert_message}
        return render(request, 'otp.html', context)


class ResetView(View):
    def get(self, request):  
        id = request.session.get('id')
        if(id == None):
            return redirect('login')
        return render(request,'reset.html')
    
    def post(self, request):
        id = request.session.get('id')
        password = request.POST.get('password')
        cpassword = request.POST.get('password2')
        if password != cpassword:
            alert_message = 'Password do not match. Please enter confirm password same as password.'
            context = {'id': id, 'alert_message': alert_message}
            return render(request, "reset.html", context)
        user_info = User.objects.get(id=id)
        print(user_info.password)

        if check_password(password, user_info.password):
            alert_message = 'Password is same as old password. Please enter new password'
            context = {'id': id, 'alert_message': alert_message}
            return render(request, "reset.html", context)
        password = make_password(password)
        my_object = User.objects.get(id=id)  # Retrieve the object
        my_object.password = password  # Modify the desired field
        my_object.save()

        return redirect('home')
    
class LogoutView(View):
    def get(self, request):
        request.session.pop('id', None)
        return redirect('login')
    

class DisplayView(View):
    def get(self, request):
        id = request.session.get('id')
        if(id == None):
            return redirect('login')
        user = User.objects.get(id = id)
        if( user.user_type == 'admin'):
            user_details = User.objects.all()
            devices = Device.objects.all()
            context = {'user': user, 'user_details': user_details, 'devices': devices}
            return render(request, 'display.html', context)

        devices = user.device_set.all()
        context = {'user': user, 'devices': devices}
        return render(request, 'display.html', context)
    
    def post(self, request):
        return render(request, 'display.html')
        
class AddDeviceView(View):
    def get(self, request, id):
        Sid = request.session.get('id')
        if(Sid == None):
            return redirect('login')
        return render(request, "addDevice.html", {id:id})
    
    def post(self, request, id):
        Sid = request.session.get('id')
        dname = request.POST.get('dname')
        dtype = request.POST.get('dtype')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        user_instance = User.objects.get(id=id)

        device_instance = Device.objects.create(user=user_instance, name=dname, type=dtype, price=price, quantity=quantity)

        lname = request.POST.get('locationName')
        address = request.POST.get('address')      
        pin = request.POST.get('pin')      
        landmarks = request.POST.get('landmarks')  

        location = Location.objects.create(device=device_instance, name=lname, address=address, pin=pin, landmarks=landmarks)

        return redirect('display')
    
class EditDeviceView(View):
    def get(self, request, id):
        Sid = request.session.get('id')
        if(Sid == None):
            return redirect('login')
        device = Device.objects.get(id=id)
        location = Location.objects.get(device=device)

        return render(request, "addDevice.html", {id:id, 'device': device, 'location': location})

    def post(self, request, id):
        Sid = request.session.get('id')

        dname = request.POST.get('dname')
        dtype = request.POST.get('dtype')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        device = Device.objects.get(id=id)
        device.name = dname
        device.type = dtype
        device.price = price
        device.quantity = quantity
        device.save()

        location = Location.objects.get(device=device)
        lname = request.POST.get('locationName')
        address = request.POST.get('address')      
        pin = request.POST.get('pin')      
        landmarks = request.POST.get('landmarks')  

        location.name = lname
        location.address = address
        location.pin = pin
        location.landmarks = landmarks
        location.save()

        return redirect('display')
    

class EditUserView(View):
    def get(self, request, id):
        Sid = request.session.get('id')
        if(Sid == None):
            return redirect('login')
        user = User.objects.get(id=id)

        return render(request, "editUser.html", {id:id, 'user': user})
    
    def post(self, request, id):
        Sid = request.session.get('id')

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        utype = request.POST.get('utype')

        user = User.objects.get(id=id)
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.address = address
        user.contact = contact
        user.save()

        return redirect('display')

class AddUserView(View):
    def get(self, request, id):
        Sid = request.session.get('id')
        if(Sid == None):
            return redirect('login')
        return render(request, "editUser.html", {'id':id})
    
    def post(self, request, id):
        Sid = request.session.get('id')

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        contact = request.POST.get('contact')

        User(email = email, first_name = fname, last_name=lname, address=address, contact= contact, user_type= 'User', is_staff=True).save()

        return redirect('display')
    

class DeleteDeviceView(View):
    def get(self, request, id):
        Sid = request.session.get('id')
        if(Sid == None):
            return redirect('login')
        device = Device.objects.get(id=id)
        location = Location.objects.get(device=device)

        device.delete()
        location.delete()

        return redirect('display')

# class DeleteUserView(View):
#     def get(self, request, id):
#         Sid = request.session.get('id')
#         if(Sid == None):
#             return redirect('login')
        
#         user = User.objects.get(id=id)
#         devices = user.device_set.all()

#         for device in devices:
#             device = Device.objects.get(id=device.id)
#             location = Location.objects.get(device=device)

#             device.delete()
#             location.delete()

#         user.delete()



#         return redirect('display')