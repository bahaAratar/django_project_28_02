from rest_framework import serializers
from .models import Order
from .tasks import send_order_confirmation_code

class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.EmailField(required=False)
    
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        amount = validated_data.get('amount')
        product = validated_data.get('product')

        if amount > product.amount:
            raise serializers.ValidationError('нет такого количества')
        
        if amount == 0:
            raise serializers.ValidationError('необходимо заказать минимум 1 товар')
        
        product.amount -= amount
        product.save(update_fields=['amount'])
        order = Order.objects.create(**validated_data)
    
        send_order_confirmation_code.delay(order.owner.email, order.activation_code, order.product.title, order.total_price)
        return order