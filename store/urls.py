from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views

# router = SimpleRouter()
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('carts', views.CartViewSet, basename='carts')
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('orders', views.OrderViewSet, basename='orders')

# To register as a resource with a nested router url








# products_router = routers.NestedDefaultRouter(router, 'products', lookup='product') 
# products_router.register('reviews', views.ReviewViewSet, basename='productreviews')
# products_router.register('images', views.ProductImageViewSet, basename='product-images')
# cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart') 
# cart_router.register('items', views.CartItemViewset,basename='cart-items')


urlpatterns = [

    ##urls for model viewsets
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(cart_router.urls)),

    ##urls for cbv and generic view
    # path ('products/', views.ProductList.as_view()),
    # path ('product/<pk>/', views.ProductDetail.as_view()),

    ##urls for normal view endpoint
    # path ('product/<pk>/', views.product_detail),
    # path ('products/', views.product_list),

    # #filtering products in a given category urls using
    # path ('productincat/<pk>/', views.products_in_category), #view method
    # path ('productincategory/<pk>/', views.ProductInCat.as_view()), #cbv method
    # path ('product_in_cat/<int:pk>/', views.Product_In_Cat.as_view()), #generic view method

    path ('category/', views.CategoryList.as_view()),
    # path ('category/', views.category_list),
    # path ('category/<pk>/', views.category_detail, name='category-detail'),

    # path ('review/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),
    # path ('review/<pk>/', views.review_detail, name='reviewdetail'),

]