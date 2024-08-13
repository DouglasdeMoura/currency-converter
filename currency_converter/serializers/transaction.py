from decimal import Decimal

from rest_framework import serializers

from currency_converter import models


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = models.Transaction
        fields = [
            "id",
            "user_id",
            "currency_from",
            "currency_to",
            "amount",
            "conversion_rate",
            "converted_amount",
            "timestamp",
        ]
        read_only_fields = ["id", "user", "conversion_rate", "converted_amount", "timestamp"]

    def create(self, validated_data):
        """
        Create and return a new `Transaction` instance, given the validated data.
        """
        return models.Transaction.objects.create(**validated_data)

    def to_internal_value(self, data):
        """Converts the amount field from dollars to cents

        Args:
            instance (Any): The instance to convert

        Returns:
            Any: The converted instance
        """
        data = super().to_internal_value(data)
        data["amount"] = int(data["amount"] * 100)
        return data

    def to_representation(self, instance):
        """Converts the amount and converted_amount fields from cents to dollars

        Args:
            instance (Any): The instance to convert

        Returns:
            Any: The converted instance
        """

        data = super().to_representation(instance)
        data["amount"] = Decimal(str(instance.amount)) / 100
        data["converted_amount"] = Decimal(str(instance.converted_amount)) / 100
        return data
