from rest_framework import serializers

from .models import HydroponicSystem, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'ph', 'tds', 'water_temperature', 'created_at']
        read_only_fields = ['created_at']


class HydroponicSystemSerializer(serializers.ModelSerializer):
    latest_measurements = MeasurementSerializer(source='measurement_set.all', many=True, read_only=True)
    measurement_count = serializers.IntegerField(source='measurement_set.count', read_only=True)

    class Meta:
        model = HydroponicSystem
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 
                 'owner', 'latest_measurements', 'measurement_count']
        read_only_fields = ['created_at', 'updated_at', 'owner']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['latest_measurements'] = MeasurementSerializer(
            instance.measurement_set.all().order_by('-created_at')[:10],
            many=True
        ).data
        return representation


class MeasurementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['system', 'ph', 'tds', 'water_temperature']

    def validate_system(self, value):
        if value.owner != self.context['request'].user:
            raise serializers.ValidationError("Nie możesz dodawać pomiarów do systemu, który nie należy do Ciebie.")
        return value
