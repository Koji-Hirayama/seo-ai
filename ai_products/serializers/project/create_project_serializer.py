from rest_framework import serializers
from ..custom_serializers import ResponseSerializer

# 一旦サンプル
# class NameVlidate(serializers.Serializer):
#     @classmethod
#     def validate(self, value):
#         name = value
#         if name == "a":
#             raise serializers.ValidationError("aは不可能です")
#         return name
    
# Postで受け取る値用
class RequestCreateProjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    
    # 一旦サンプル
    # def validate_name(self, value):
    #     # name = NameVlidate.validate(value)
    #     return NameVlidate.validate(value)
    
# response用
class CreateProjectSerializer(ResponseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    
