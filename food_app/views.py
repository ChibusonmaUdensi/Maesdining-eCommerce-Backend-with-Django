from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Cart, CartItem, Product
from .serializers import CartItemSerializer, ProductSerializer, DetailedProductSerializer
from rest_framework.response import Response


@api_view(["GET"])
def products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    serializer = DetailedProductSerializer(product)
    return Response(serializer.data)

@api_view(["POST"])
def add_item(request):
    try:
        cart_code= request.data.get("cart_code")
        product_id = request.data.get("product_id")

        cart, created = Cart.objects.get_or_create(cart_code= cart_code)
        product = Product.objects.get(id=product_id)

        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity = 1
        cartitem.save()

        serializer= CartItemSerializer(cartitem)
        return Response({"data": serializer.data, "message": "CartItem created successfully"}, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(["GET"])
def product_in_cart(request):
    cart_code = request.query_params.get('cart_code')
    product_id = request.query_params.get('product_id')

    cart = Cart.objects.get(cart_code=cart_code)
    product = Product.objects.get(id=product_id)
    
    product_exists_in_cart = CartItem.objects.filter(cart=cart, product=product).exists()

    return Response({'product_in_cart': product_exists_in_cart})

@api_view(["DELETE"])
def product_remove_from_cart(request):
    cart_code = request.query_params.get('cart_code')
    product_id = request.query_params.get('product_id')
    
    cart = Cart.objects.get(cart_code=cart_code)
    product = Product.objects.get(id=product_id)
    
    cart_item = CartItem.objects.filter(cart=cart, product=product).first() 
    if cart_item:
        cart_item.delete()
        return Response({"message": "Product removed from cart successfully"})