from rest_framework import serializers

class ResponseSerializer(serializers.Serializer):
    """レスポンス用にカスタマイズされたSerializer"""
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.is_valid()
        
    def get_data(self):
        """レスポンス用にシリアライズされた状態のdataを返す"""
        return self.validated_data