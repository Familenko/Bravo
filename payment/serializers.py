from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    pass


class PaymentListSerializer(serializers.ModelSerializer):
    pass


class PaymentDetailSerializer(serializers.ModelSerializer):
    pass


class PaymentCreateSerializer(serializers.ModelSerializer):
    pass
