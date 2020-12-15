from django.contrib import admin
from django.urls import path
from .views import acceptorder, declineorder, adminorders, userorders, placeorder, userlogout, authenticateuser, welcomeuser,userlogin, homepage, signupuser, deletepizza, adminlogin, addpizza, adminhomepage,authenticateadmin,adminlogout

urlpatterns = [
    path('admin/', adminlogin, name='adminloginpage'),
    path('adminauthenticate/', authenticateadmin),
 	path('admin/homepage/', adminhomepage, name='adminhomepage'),
 	path('adminlogout/',adminlogout),
 	path('addpizza/',addpizza),
 	path('deletepizza/<int:pizzapk>/',deletepizza),
 	path('', homepage, name = 'homepage'),
 	path('signup/',signupuser),
 	path('userlogin/',userlogin,name = 'loginuser'),
 	path('user/welcome/',welcomeuser,name = 'userhomepage'),
 	path('user/authenticate/',authenticateuser),
 	path('userlogout/',userlogout),
 	path('placeorder/',placeorder),
 	path('userorders/', userorders),
 	path('adminorders/',adminorders),
 	path('acceptorder/<int:orderpk>/',acceptorder),
 	path('declineorder/<int:orderpk>/',declineorder)
]
