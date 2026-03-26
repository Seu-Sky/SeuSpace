from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.blog, name='post_list'),
    path('category/<slug:category_slug>/', views.blog, name='post_list_by_category'),
    path('<int:id>/', views.post_detail, name='post_detail'), 
    path('<int:id>/edit/', views.edit_post, name='edit_post'), 
    path('<int:id>/delete/', views.delete_post, name='delete_post'),
    path('category/<int:id>/delete/', views.delete_category, name='delete_category'),
    path('add_blog/', views.create_post, name='create_post'),
]