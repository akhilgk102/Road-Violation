from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from django.views.generic import View
from road_app.forms import SignUpForm,SignInForm,RoadViolationForm
from django.contrib.auth import login,authenticate,logout
from road_app.models import RoadViolation

from django.utils.decorators import method_decorator

from road_app.decorators import signin_required

from django.views.decorators.cache import never_cache



decs=[signin_required,never_cache]

class SignUpView(View):

    template_name="register.html"

    form_class=SignUpForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            form_instance.save()

            return render(request,self.template_name,{"form":form_instance})
        
        return render(request,self.template_name,{"form":form_instance})

class SignInView(View):

    template_name="login.html"

    form_class=SignInForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                print("Loginned")

                return redirect("upload")
            
            print("Failed")
            
            return render(request,self.template_name,{"form":form_instance})

@method_decorator(decs,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")





@method_decorator(decs,name="dispatch")
class UploadViolationView(View):

    template_name="road_violation.html"

    form_class=RoadViolationForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data,request.FILES)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            return redirect("list")
        
        return render(request,self.template_name,{"form":form_instance})

@method_decorator(decs,name="dispatch")
class ViolationListView(View):

    template_name='list_violation.html'

    def get(self,request,*args,**kwargs):

        all_violations=RoadViolation.objects.filter(owner=request.user)

        return render(request,self.template_name,{"all_violations":all_violations})
    
@method_decorator(decs,name="dispatch")
class ViolationUpdateView(View):

    template_name="update_violation.html"

    form_class=RoadViolationForm

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        violation_obj=RoadViolation.objects.get(id=id)

        form_instance=self.form_class(instance=violation_obj)

        return render(request,self.template_name,{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        violation_obj=RoadViolation.objects.get(id=id)

        form_data=request.POST

        form_instance=self.form_class(form_data,request.FILES,instance=violation_obj)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            return redirect("list")
        
        return render(request,self.template_name,{"form":form_instance})

@method_decorator(decs,name="dispatch")
class ViolationDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        get_object_or_404(RoadViolation,id=id).delete()

        return redirect("list")




