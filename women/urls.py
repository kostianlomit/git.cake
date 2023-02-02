from django.urls import path

from .views import *

urlpatterns = [
    path('', WomenHome.as_view(), name='home'),
    path('about/', AboutHome.as_view(), name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('work/', WorkHome.as_view(), name='work'),
    path('contact/', ContactCreate.as_view(), name='contact'),
    path('contact/success/', SuccessView.as_view(), name='success'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('work_one/<int:work_id>/', show_work_one, name='work_detail'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
    path('<slug:slug>/', WomenHome.as_view(), name='post')
]
