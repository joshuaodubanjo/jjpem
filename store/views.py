from django.shortcuts import render, get_object_or_404,get_list_or_404
from django.db.models import Count

from django_filters.rest_framework import DjangoFilterBackend #works only for viewsets and generic views class
from .filters import ProductFilter

from .models import Product,Category,Promotion,Customer,Review, Cart, CartItem,Order,OrderItem,ProductImage

from .serializers import ProductSerializer, CategorySerializer,ReviewSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer
from .serializers import CustomerSerializer,OrderSerializer, CreateOrderSerializer,UpdateOrderSerializer,ProductImageSerializer

from rest_framework import status

from rest_framework.decorators import api_view #used for creating url endpoints usingg normal views
from rest_framework.views import APIView  #used for creating url endpoints usinh classed based views
from rest_framework.generics import ListAPIView, ListCreateAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView,RetrieveAPIView,DestroyAPIView #for creating url endpoints using generic mixins views
from rest_framework.viewsets import ModelViewSet,GenericViewSet #for creating endpoint using viewsets
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin,ListModelMixin

from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response
from rest_framework.validators import ValidationError

from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny,IsAuthenticatedOrReadOnly

from .pagination import DefaultPagination, ProductPagination 

from rest_framework.decorators import action 

from .permissions import IsAdminOrReadOnly,FullDjangoModelPermissions



''' GET,POST METHODS'''
#FOURTH METHOD FOR WRITING API WITH VIEWSETS
class ProductViewSet(ModelViewSet):
    queryset= Product.objects.all()
    filter_backends = [DjangoFilterBackend,SearchFilter] 
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    pagination_class = ProductPagination 
    serializer_class = ProductSerializer
    # permission_classes = [FullDjangoModelPermissions]
    permission_classes = [IsAdminOrReadOnly]

    # def get_queryset(self):  
    #     queryset= Product.objects.all()
    #     catid = self.request.query_params.get('category_id')
    #     if catid:
    #         queryset = Product.objects.filter(category_id=self.request.query_params.get('category_id'))

    #     return queryset    

#     def destroy(self,request,pk):  
#         product = get_object_or_404(Product, pk=pk)
#         if product.id == 1:
#             raise ValidationError('sorry you cannot delete this product')   
#         product.delete() 
#         return Response({"message":"object deleted successfully"}, status=status.HTTP_204_NO_CONTENT) 

'''Product image viewset'''
class ProductImageViewSet(ModelViewSet):     
    def get_queryset(self):         
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    serializer_class = ProductImageSerializer     # queryset = ProductImage.objects.all()  
    def get_serializer_context(self):         
        return {'prod_id': self.kwargs['product_pk']}  


###THIRD METHOD FOR WRITING API WITH GENERIC MIXINS
# class ProductList(ListCreateAPIView):
#     queryset= Product.objects.all()
#     # filter_backends = [DjangoFilterBackend] 
#     # filterset_fields = ['category_id', 'unit_price']
#     serializer_class = ProductSerializer



## SECOND METHOD FOR WRITING API WITH CBV
# class ProductList(APIView):
#     def get(self,request):
#         productqs = Product.objects.all().select_related('category')
#         serializer = ProductSerializer(productqs, many=True, context={'request':request})
#         return Response(serializer.data)

#     def post(self,request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)   
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

  

##FIRST METHOD FOR WRITING API WITH DECORATORS
# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method == 'GET':
#          productqs = Product.objects.all().select_related('category')
#          serializer = ProductSerializer(productqs, many=True, context={'request':request})
#          return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)   
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      

''' GET,PUT,PATCH, DELETE METHODS FOR DETAILS'''
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset= Product.objects.all()
#     serializer_class = ProductSerializer

#     def delete(self,request,pk):  
#         product = get_object_or_404(Product, pk=pk)
#         if product.id == 1:
#             raise ValidationError('sorry you cannot delete this product')   
#         product.delete() 
#         return Response({"message":"object deleted successfully"}, status=status.HTTP_204_NO_CONTENT) 

# self.kwargs['pk']

#     def put(self,request,pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product, data=request.data)         
#         if serializer.is_valid():        
#            serializer.save()        
#            return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)         

#     def delete(self,request,pk):  
#         product = get_object_or_404(Product, pk=pk)   
#         product.delete() 
#         return Response({"message":"object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)   

# @api_view(['GET','PUT','DELETE']) 
# def product_detail(request, pk): #supply **kwargs if you want to get product by other field eg title 
#     product = get_object_or_404(Product, pk=pk) #supply title=kwargs['title'] if you want to get product by 
#     if request.method == 'GET':
#         serializer = ProductSerializer(product,context={'request':request})
#         return Response(serializer.data) 
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)         
#         if serializer.is_valid():        
#            serializer.save()        
#            return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
#     elif request.method == 'DELETE':
#         product.delete() 
#         return Response({"message":"object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# def product_detail(request, ):
#     product = get_object_or_404(Product, )        


''' CATEGORY SECTION'''
class CategoryList(ListCreateAPIView):
    queryset = Category.objects.annotate( product_count = Count('product'))
    serializer_class = CategorySerializer


# @api_view()
# def category_list(request):
#     categoryqs = Category.objects.all()
#     serializer = CategorySerializer(categoryqs, many=True)
#     return Response(serializer.data)


# @api_view()
# def category_detail(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     serializer = CategorySerializer(category)
#     return Response(serializer.data)   

'''REVIEW'''
class ReviewViewSet(ModelViewSet):     #Get the reviews for a given product id  
    def get_queryset(self):        
        return Review.objects.filter(product__id=self.kwargs['product_pk']) 

    def get_serializer_context(self):         
        return {'product_id': self.kwargs['product_pk']}     

    serializer_class = ReviewSerializer

# @api_view()
# def review_detail(request, pk):
#     review = Review.objects.filter(product__id=product.pk) 
#     serializer = ReviewSerializer(review, many=True)
#     return Response(serializer.data) 


# class ReviewDetail(ListAPIView):
#         def get_queryset(self):  
#             self.product = get_object_or_404(Product, id=['pk'])      
#             return Review.objects.filter(product_id=self.product)

#         def get_serializer_class(self):         
#             return ReviewSerializer

class ReviewViewSet(ModelViewSet):     #Get the reviews for a given product id  
    def get_queryset(self):        
        return Review.objects.filter(product__id=self.kwargs['product_pk']) 

    def get_serializer_context(self):         
        return {'product_id': self.kwargs['product_pk']}     

    serializer_class = ReviewSerializer  

# class AllReviewViewSet(ModelViewSet):     #Get the reviews for a given product id  
#     queryset = Review.objects.all()   
#     serializer_class = ReviewSerializer       


'''CART SECTION'''
class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.prefetch_related('cartitem_set__product').all()
    serializer_class = CartSerializer

class CartItemViewset(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

    def get_serializer_class(self):
        if self.request.method == 'POST':    
            return AddCartItemSerializer
        elif self.request.method == 'PATCH': 
            return UpdateCartItemSerializer  
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}           



'''Customer Section'''
class CustomerViewSet(CreateModelMixin,ListModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):     
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [IsAuthenticatedOrReadOnly()]
    #     return [IsAdminUser()]    

    @action(detail=False, methods=['GET', 'PUT'],permission_classes=[IsAuthenticated])     
    def me(self, request):         
        customer = Customer.objects.get(user__id=request.user.id)
        # (customer,created) = Customer.objects.get_or_create(user__id=request.user.id, user_id=request.user.id)           
        if request.method == 'GET':             
            serializer = CustomerSerializer(customer)             
            return Response(serializer.data)         
        elif request.method == 'PUT':             
            serializer = CustomerSerializer(customer, data=request.data)            
            if serializer.is_valid():                 
                serializer.save()                 
                return Response(serializer.data)             
            else:                 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


'''ORDER SECTION'''
class OrderViewSet(ModelViewSet): 
    http_method_names = ['get','post','patch','delete']

    #PERMISSIONS
    def get_permissions(self):       
        if self.request.method in ['PATCH', 'DELETE']:             
           return [IsAdminUser()]        
        return [IsAuthenticated()]

    #QUERYSET    
    def get_queryset(self):
        if self.request.user.is_staff:
            Order.objects.all()
        return Order.objects.filter(customer__user_id=self.request.user.id)

    #SERIALIZERS    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer   
        return CreateOrderSerializer 

    #OVERIDING THE CREATE METHOD TO RETURN THE ORDERSERIALIZER WHEN IT IS A POST REQUEST 
    def create(self, request, *args, **kwargs):    
         serializer = CreateOrderSerializer(data=request.data, context={'user_id': request.user.id})         
         serializer.is_valid(raise_exception=True)         
         order = serializer.save()         
         
         serializer = OrderSerializer(order)         
         return Response(serializer.data)

    def get_serializer_context(self):
        return{
            'user_id': self.request.user.id
        }      
    






''' FILTERING'''
##Filtering products in a given category using VEW METHOD,  APIVIEW METHOD AND GENERIC VIEW METHOD
# @api_view(['GET'])
# def products_in_category(request,pk):
#     productcat = Product.objects.filter(category_id=pk)
#     serializer = ProductSerializer(productcat, many=True, context={'request':request})
#     return Response(serializer.data)

# class ProductInCat(APIView):
#     def get(self, request, pk):
#         productincatqs= Product.objects.filter(category_id=pk)
#         # productincatqs= get_list_or_404(Product, category_id=pk)
#         serializer = ProductSerializer(productincatqs, many=True)

#         return Response(serializer.data)

# class Product_In_Cat(ListAPIView):
#         def get_queryset(self):  
#             self.category = get_object_or_404(Category, id=self.kwargs['pk'])      
#             return Product.objects.filter(category_id=self.category)

#         def get_serializer_class(self):         
#             return ProductSerializer
