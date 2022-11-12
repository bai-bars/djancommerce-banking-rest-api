from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from apps.cart.models import CartItem


from apps.products.models import ProductInventory
from apps.products.permissions import (ReadOrIsSeller, ReadOrIsAdmin,
                                        IsAllowedToChangeInventory)
from apps.cart import serializers
from apps.cart import utils

class CartFilteredListAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartItemSerializer
    

    def get_queryset(self):
        user = self.request.user

        if user.role == '1':
            carts = CartItem.objects.all()
        else:
            carts = CartItem.objects.filter(user__id = user.id)

        return carts
    


class AddAndUpdateToCartAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartItemSerializer

    def post(self, request):
        cart_items = CartItem.objects.filter(user__id = request.user.id)
        cart_data = request.data
        
        if isinstance(cart_data, list):
            for data in cart_data:
                data['user'] = request.user.id
                check = utils.check_existence_in_cart(data, cart_items)

                if check['does_exist']:
                    if int(data['quantity']) <= 0:
                        check['item'].delete()
                    else:
                        if utils.quantity_lt_remaining_units(data):
                            serializer = serializers.CartItemSerializer(instance=check['item'],
                                                    data = data, partial=True)
                        
                            if serializer.is_valid(raise_exception=True):
                                serializer.save()
                else:
                    if int(data['quantity']) > 0 and utils.quantity_lt_remaining_units(data):
                        serializer = serializers.CartItemSerializer(data = data)

                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                
        elif isinstance(cart_data, dict):
                check = utils.check_existence_in_cart(cart_data, cart_items)
                cart_data['user'] = request.user.id

                if check['does_exist']:
                    if int(cart_data['quantity']) <= 0:
                        check['item'].delete()

                    else:
                        if utils.quantity_lt_remaining_units(cart_data):
                            serializer = serializers.CartItemSerializer(instance=check['item'],
                                                    data = cart_data, partial=True)

                            if serializer.is_valid(raise_exception=True):
                                serializer.save()
                else:
                    if int(cart_data['quantity']) > 0 and utils.quantity_lt_remaining_units(cart_data):
                        serializer = serializers.CartItemSerializer(data = cart_data)

                        if serializer.is_valid(raise_exception=True):
                            serializer.save()


        cart_items = CartItem.objects.filter(user__id = request.user.id)
        serializer = serializers.CartItemSerializer(cart_items, many=True)

        return Response(serializer.data, status = status.HTTP_200_OK)


class DeleteAllCartItemAPI(views.APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request):
        CartItem.objects.filter(user__id = request.user.id).delete()

        return Response({'msg' : 'All Deletion Successful'}, status = status.HTTP_200_OK)


class DeleteSingleCartItemAPI(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request, id):
        CartItem.objects.filter(id = id).delete()

        return Response({'msg' : 'Single Deletion Successful'}, status = status.HTTP_200_OK)
