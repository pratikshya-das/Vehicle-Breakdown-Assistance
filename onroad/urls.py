from django.urls import path
from . import views
from onroadapp.settings import DEBUG, STATIC_URL, MEDIA_URL, MEDIA_ROOT

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
#DataFlair Django Tutorials
urlpatterns = [
path('', views.index, name = 'index'),

path('main/', views.SignUpView.as_view(), name="signup"),
 
    path('shop/', views.ShopSignUpView.as_view(), name='shop_signup'),
    path('user/', views.UserSignUpView.as_view(), name='user_signup'),
     path('shop_home/', views.shop_home, name='shop_home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name="login"),   
	path('logout/', views.logout, name="logout"),
    path('admin/', views.adminlogin, name="adminlogin"),
    path('forget_password/', views.forget_password, name="forget_password"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('view_business/getgeo/', views.getgeo, name="getgeo"),
    path('view_business/', views.view_business, name='view_business'),
    path('userpage/', views.userpage, name = "userpage"),
    path('business_user/', views.business_user, name = "business_user"),
 	path('upload/', views.upload, name = 'upload-shop'),
    path('upload_feedback/', views.upload_feedback, name = 'upload_feedback'),
    path('upload_payment/', views.upload_pay, name = 'upload_pay'),
    path('createorder/', views.createorder,  name = 'createorder'),
    path('all_business_details/', views.all_business_details, name='all_business_details'),
    
     path('all_business_details/all_business_details_full/<int:business_id>', views.all_business_details_full, name='all_business_details_full'),
    path('all_business_details/all_business_details_full/showgeo/<int:business_id>', views.showgeo, name='showgeo'),
    path('my_feedback/', views.view_feedback, name='view_feedback'),
    path('my_payment/', views.my_payment, name='my_payment'),
    path('mechanic_payment/', views.mechanic_payment, name='mechanic_payment'),
    
    path('checkplaceorder/', views.checkplaceorder),
    path('soldorder/', views.soldorder, name='soldorder'),
    path('view_business/update/<int:business_id>', views.update_business),
    
	path('view_business/delete/<int:business_id>', views.delete_business)
]
urlpatterns += staticfiles_urlpatterns()
if DEBUG:
   
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)


'''x-html has doctype manadatory while html doesn't require you to declare doctype
xmlns type is mandatory in html
html, head, body and title is mandatory
must be properly nested
must be properly closed
must be used in lowercase

'''