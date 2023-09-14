from rest_framework import serializers
from .models import User,FileUpload,FolderUpload,Logic,JavaCode,MermaidDiagrams
class UserSerializer(serializers.ModelSerializer):
    class Meta : 
        model = User
        fields = '__all__'



class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['fileId', 'filename', 'file', 'parentFolder']
        read_only_fields = ['fileId','filename', 'parentFolder']

class FolderSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)
    class Meta : 
        model = FolderUpload
        fields = '__all__'


class LogicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logic
        fields = '__all__'

class JavaCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JavaCode
        fields = '__all__'


class MermaidDiagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = MermaidDiagrams
        fields = '__all__'