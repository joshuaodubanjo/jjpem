from decimal import Decimal

from django.db import transaction

from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import  Product, Category,Review, Cart,CartItem,Customer,Order,OrderItem,ProductImage

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer

class CategorySerializer(serializers.ModelSerializer):      
    class Meta:
        model = Category
        fields = ['id','title','product_count']
        
    product_count = serializers.IntegerField(read_only=True) #if you dont want this field to participate  in post request       


class ProductImageSerializer(serializers.ModelSerializer):     
    class Meta:         
        model = ProductImage         
        fields = ['id','image']

    def create(self, validated_data):        
        product_id = self.context['prod_id']         
        return ProductImage.objects.create(product_id=product_id, **validated_data)  



# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()
#     unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     product_tax = serializers.SerializerMethodField(method_name = 'calc_tax')
#     category = serializers.HyperlinkedRelatedField( queryset = Category.objects.all(), view_name='category-detail' )


#     def calc_tax(self,prod):
#         return prod.unit_price * Decimal(0.45)

class ReviewAllProdSerializer(serializers.ModelSerializer):     
    class Meta:         
        model = Review         
        fields = ['id', 'posted_at', 'reviewer_name', 'remark',] 

#PRODUCT SERIALIZER
class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    class Meta:
        model = Product
        fields = ['id','title','description','price','category','product_tax', 'images','review']

    # product_id = self.context['product_id'] 

    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    category = serializers.PrimaryKeyRelatedField( queryset = Category.objects.all() )
    product_tax = serializers.SerializerMethodField(method_name= 'calc_tax')
    images = ProductImageSerializer(many=True, read_only=True)
    # review = serializers.HyperlinkedRelatedField(queryset=Review.objects.all(),source='review_set',view_name='productreviews')  
    review = ReviewAllProdSerializer(many=True, source='review_set',read_only=True)

    def calc_tax(self,prod):
        return prod.unit_price * Decimal(0.45)


    #FUTHER VALIDATING THE DATA BY OVERIDING THE VALIDATE FUNCTION  [PRODUCT POST/PUT/PATCH REQUEST]

    # def validate(self, data):         
    #     if data['unit_price'] < 100:             
    #         raise ValidationError('Invalid Price! Price cannot be less than 100')         
    #     return data

    ##CUSTOMIZING DATA OR PERSISTING AT THE DB LEVEL  [PRODUCT POST/PUT/PATCH REQUEST]
   
    def create(self, validated_data):  #overiding the create method        
        product = Product(**validated_data)      
        product.junk = f'{product.title} -- this is my stuff'        
        product.save()         
        return product

    # def update(self, instance: Product, validated_data):         
    #     instance.title = validated_data.get('title', instance.title)         
    #     instance.price = validated_data.get('price', instance.unit_price)         
    #     instance.when_uploaded = validated_data.get( 'when_uploaded', instance.when_uploaded)         
    #     instance.last_updated = validated_data.get( 'last_updated', instance.last_updated)        
    #     instance.category = validated_data.get('category', instance.category)         
    #     instance.description = 'Lezz do deees'     
    #     instance.save()         
    #     return instance   

#REVIEW SERIALIZERS
class ReviewSerializer(serializers.ModelSerializer):     
    class Meta:         
        model = Review         
        fields = ['id', 'posted_at', 'reviewer_name', 'remark',]      

        
    def create(self, validated_data):        
        product_id = self.context['product_id']         
        return Review.objects.create(product_id=product_id, **validated_data)  


#CART SERIALIZERS
class SimpleProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','title','unit_price','category']

    category= serializers.StringRelatedField()    


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model= CartItem
        fields = ['id','product','quantity', 'sub_total']

    id = serializers.IntegerField(read_only=True)
    product = SimpleProductSerializer()
    sub_total = serializers.SerializerMethodField()  

    def get_sub_total(self, item:CartItem):
        return item.product.unit_price * item.quantity    


class AddCartItemSerializer(serializers.ModelSerializer):
 
    class Meta:
        model= CartItem
        fields = ['product_id','quantity'] 

    product_id = serializers.IntegerField() 

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']  
        cart_id = self.context['cart_id']

        cartitem = CartItem.objects.filter(product_id=product_id,cart_id=cart_id).first()
        if cartitem:
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
        else:
            new_cartitem = CartItem.objects.create(cart_id=cart_id, **self.validated_data)             
            self.instance = new_cartitem 
        return self.instance 

    def validate_product_id(self,value):
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError('sorry bros, no product with id in db')
        return value 
        

    # def validate_quantity(self,value):
    #     if value < 100:
    #         raise ValidationError('Invalid Price! Price cannot be less than 100')         
    #     return value
                      

        # try:             
        #     cartitem = CartItem.objects.get(cart_id=cart_id, product_id=product_id)             
        #     # Update existing Item             
        #     cartitem.quantity += quantity             
        #     cartitem.save()             
        #     self.instance = cartitem      
        # except CartItem.DoesNotExist:             
        #     # Create a new Item             
        #     new_cartitem = CartItem.objects.create(cart_id=cart_id, **self.validated_data)             
        #     self.instance = new_cartitem  
        # return self.instance      

class UpdateCartItemSerializer(serializers.ModelSerializer):     
    class Meta:         
        model = CartItem         
        fields = ['quantity']
    
class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model= Cart
        fields = ['id','item', 'grand_total']

    id = serializers.UUIDField(read_only=True)
    item = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    grand_total = serializers.SerializerMethodField()


    def get_grand_total(self, cart:Cart):
        return sum([item.product.unit_price * item.quantity for item in cart.cartitem_set.all()])    

#DJOSER USER SERIALIZERS        

class UserCreateSerializer(BaseUserCreateSerializer):     
    class Meta(BaseUserCreateSerializer.Meta):         
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

class UserSerializer(BaseUserSerializer):     
    class Meta(BaseUserSerializer.Meta):         
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

#CUSTOMER SERILAIZER
class CustomerSerializer(serializers.ModelSerializer):    
    user_id = serializers.IntegerField(read_only=True) 
    class Meta:         
        model = Customer         
        fields = ['id', 'user_id', 'birth_date', 'membership']         

#ORDER SERILAIZER
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:         
        model = OrderItem         
        fields = ['id','product', 'price', 'quantity'] 

class OrderSerializer(serializers.ModelSerializer):    
    items = OrderItemSerializer(many=True, source='orderitem_set', read_only=True)
    class Meta:         
        model = Order         
        fields = ['id','customer', 'items', 'placed_at', 'payment_status','delivery_status']  


class CreateOrderSerializer(serializers.Serializer): 
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cartid):
        if not Cart.objects.filter(id=cartid).exists(): #checking for invalid cart id
            raise serializers.ValidationError('invalid cart id supplied')

        if not CartItem.objects.filter(cart_id=cartid).exists(): #checking for empty cart
            raise serializers.ValidationError('empty cart supplied')

        return cartid     

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id =  self.context['user_id']

            # CREATING ORDER
            customer = Customer.objects.get(user_id=user_id)
            theorder = Order.objects.create(customer=customer, delivery_status='pending')

            # COPYING THE CART ITEMS TO CREATE THE ORDER ITEM
            cartitems = CartItem.objects.filter(cart_id = cart_id)
            orderitems = [
                OrderItem(
                    order=theorder, 
                    product=item.product,
                    price= item.product.unit_price,
                    quantity = item.quantity
                ) for item in cartitems
            ]

            OrderItem.objects.bulk_create(orderitems)

            #  DELETE THE CART         
            thecart = Cart.objects.get(id=cart_id)         
            if thecart:             
                thecart.delete()

            return theorder    

class UpdateOrderSerializer(serializers.ModelSerializer):    
    class Meta:         
        model = Order         
        fields = ['payment_status','delivery_status']    