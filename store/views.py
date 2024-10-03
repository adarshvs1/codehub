from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect

from django.urls import reverse_lazy #is used to redirect

from django.views.generic import View,TemplateView,UpdateView,CreateView,DetailView,ListView,FormView

from store.forms import SignUpForm, SignInForm,UserprofileForm,ProjectForm,ReviewForm

from django.contrib.auth import login,logout,authenticate

from store.models import UserProfile,Project,WishListItems,OrderSummary,Reviews

from django.urls import reverse_lazy

from decouple import config  #is used to hide the razorpay secreat key and id with the help of decouple,





KEY_ID= config('KEY_ID')

KEY_SECRET= config('KEY_SECRET')


# Create your views here.


#registration

class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpForm()

        return render(request,'store/signup.html',{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            return redirect('signin')
        
        else:

            return render(request,'store/signup.html',{'form':form_instance})
        
#login

class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm

        return render(request,'store/login.html',{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            user_obj=authenticate(request,**data)

            if user_obj:

                login(request,user_obj)

                return redirect('index')
            
            else:
                
                return render(request,'store/login.html',{'form':form_instance})
            

# indexpage view

class IndexView(View):  #is used for html template

    template_name='store/index.html'

    def get(self,request,*args,**kwargs): #porject list

        qs=Project.objects.all().exclude(owner=request.user)

        return render(request,self.template_name,{'projects':qs})


#profile edit


class UserProfileUpdateView(UpdateView):

    model=UserProfile

    form_class=UserprofileForm

    template_name='store/profile_edit.html'

    success_url=reverse_lazy('index')

    #def get(self,request,*args,**kwargs):

        #id=kwargs.get('pk')

        #profile_obj=UserProfile.objects.get(id=id)

        #form_instance=UserprofileForm(instance=profile_obj)

        #return render(request,'store/profile_edit.html',{'form':form_instance})


#create view

class ProjectCreateView(CreateView):

    model=Project

    form_class=ProjectForm

    template_name='store/project_add.html'

    success_url=reverse_lazy('index')

    #if you want to add extra operation  before saving is used form_valid

    def form_valid(self, form):

        form.instance.owner=self.request.user

        return super().form_valid(form)
    
    
#Project List

class MyprojectListView(View):

    def get(self,request,*args,**kwargs):
       

       # qs=Project.objects.filter(owner=request.user)

       qs=request.user.projects.all()
       
       return render(request,'store/myprojects.html',{'works':qs})
    
    
#project delete 

class ProjectDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        Project.objects.get(id=id).delete()

        return redirect('myworks')
    
    
#project detail

class ProjectDetailView(DetailView):

    template_name='store/project_detail.html'

    context_object_name='project' #dictionary key

    model=Project

#Add to wishlist

class AddToWishListView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        project_obj=Project.objects.get(id=id)

        WishListItems.objects.create(wishlist_object=request.user.basket, #logged user 
                                     
                                     project_object=project_obj) #id
        
        print('item has been added to wishlist')

        return redirect('index')
    

#Cart 

from django.db.models import Sum  #is used to see tha total amount of your cart items

class MyCartListView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.basket.basket_items.filter(is_order_placed=False)

        total=request.user.basket.wishlist_total  #(model wishlist_total called)

        return render(request,'store/wishlist_summary.html',{'cartitems':qs,'total':total})
    

#Wishlist item remove(cart)

class WishListItemDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        WishListItems.objects.get(id=id).delete()

        return redirect('my-cart')
    
#cart/checkout (total_amount/cart/)

import razorpay #payment

class CheckOutView(View):

    def get(self,request,*args,**kwargs):

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))    #site/python/paymentgateway

        amount=request.user.basket.wishlist_total * 100     #taking the total amount in the wishlist and converting into rupess

        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)

        #create order_object

        cart_items=request.user.basket.basket_items.filter(is_order_placed=False)  #taking cart items

        Order_summary_obj=OrderSummary.objects.create(
            user_object=request.user,

            order_id=payment.get('id'),

            total = request.user.basket.wishlist_total  #taking the total amount in orders
        )

        #Order_summary_obj.project_objects.add(cart_items.values('project_object'))

        for ci in cart_items: #taking cart items

            Order_summary_obj.project_objects.add(ci.project_object)  #taking the cart items

            Order_summary_obj.save()

        for ci in cart_items:

            ci.is_order_placed=True

            ci.save()
        
        

        # print(payment)  #id

        context={

            'key':KEY_ID,

            'amount':data.get('amount'),

            'currency':data.get('currency'),

            'order_id':payment.get('id')

        }

        return render(request,'store/payment.html',context)
    

#payment verification

from django.views.decorators.csrf import csrf_exempt 

from django.utils.decorators import method_decorator #this decrtr is used to avoid csrf token checking

@method_decorator(csrf_exempt,name='dispatch')
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET)) #payment authentication

        order_summary_object=OrderSummary.objects.get(order_id=request.POST.get('razorpay_order_id')) #taking the user

        login(request,order_summary_object.user_object)

        try:

            # error doubtful code
            client.utility.verify_payment_signature(request.POST)
            print('payment success')

            order_id=request.POST.get('razorpay_order_id')    #taking order id

            OrderSummary.objects.filter(order_id=order_id).update(is_paid=True)  #taking order summary and updating is_paid true



        except:

            print('payment failed')

            # handling code

        #return render(request,'store/success.html')

        return redirect('index')
    
#purchase summary 

class MyPurchaseView(View):

    model=OrderSummary

    context_object_name='orders'

    def get(self,request,*args,**kwargs):

        qs=OrderSummary.objects.filter(user_object=request.user,is_paid=True).order_by('created_date') # loged user is_paid=true taking

        return render(request,'store/order_summary.html',{'orders':qs})

    
#review create view

#url:lh/8000/project/<int:pk>/review/add/

class ReviewCreateView(FormView):   #passing html page to form

    template_name= 'store/review.html'  

    form_class= ReviewForm

    def post(self,request,*args,**kwargs):

        id= kwargs.get('pk')

        project_obj= Project.objects.get(id=id)

        form_instance= ReviewForm(request.POST)
        
        if form_instance.is_valid():

            form_instance.instance.user_object=(request.user)

            form_instance.instance.project_object= project_obj

            form_instance.save()

            return redirect('index')
        
        else:

            return render(request,self.template_name,{'form':form_instance})





        

        




        

        
























    




            



       








