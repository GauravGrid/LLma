from rest_framework import serializers
from .models import User,FileUpload,FolderUpload,Logic,JavaCode,MermaidDiagrams,GitHubRepository,HighLevel,ScaniaBusinessLogic
class UserSerializer(serializers.ModelSerializer):
    class Meta : 
        model = User
        fields = '__all__'



class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['fileId', 'filename', 'file', 'parentFolder', 'code_language']
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


class GithubRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubRepository
        fields = '__all__'

class ShareCodeSerializer(serializers.Serializer):
    folder_structure_id = serializers.IntegerField()

class HighLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighLevel
        fields = '__all__'

class ScaniaLogicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScaniaBusinessLogic
        fields = '__all__'