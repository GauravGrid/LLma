from django.http import JsonResponse
import keys
import base64
from .service import business_logic
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from .service import generateJava,generateFlowChart,generateClassDiagram,javaCompiler,detectLanguage
from .new_prompts import business_logic_to_mermaid_diagram,business_logic_to_code,business_logic_to_mermaid_flowchart,code_to_business_logic, file_business_logic,file_mermaid_diagram,file_mermaid_flowchart,combine_business_logic,combine_mermaid_diagram,combine_mermaid_flowchart
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FolderUpload, FileUpload,User,Logic,JavaCode,MermaidDiagrams,GitHubRepository,ShareCode,HighLevel
import zipfile
from .authorisation import CustomIsAuthenticated,TokenAuthentication
import tempfile
from .serializers import FileSerializer,LogicSerializer,JavaCodeSerializer,MermaidDiagramSerializer,GithubRepositorySerializer,ShareCodeSerializer,HighLevelSerializer
from django.http import Http404
import requests
import tiktoken
from django.shortcuts import redirect
from rest_framework.decorators import permission_classes,authentication_classes
from .newrepo import create_repository,get_git_repo_owner,create_github_branch,push_to_github
import os
from pydantic import BaseModel
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatAnthropic
from langchain.output_parsers import StructuredOutputParser,ResponseSchema
from .prompt_code_to_business_logic import java_example1,python_example1,sql_example1,mongodb_example1,react_example1,angular_example1,rpg_example1,sas_example1, dspf_exampler1,dspf_examplea1,assembly_example1,rpg_exampleh
from .prompt_business_logic_to_mermaid_diagram import java_example2,python_example2,sql_example2,mongodb_example2,react_example2,angular_example2,rpg_example2,sas_example2, dspf_exampler2,dspf_examplea2,assembly_example2
from .prompt_business_logic_to_mermaid_flowchart import java_example3,python_example3,sql_example3,mongodb_example3,react_example3,angular_example3,rpg_example3,sas_example3, dspf_exampler3,dspf_examplea3,assembly_example3
from .prompt_business_logic_to_code import java_example4,python_example4,sql_example4,mongodb_example4,react_example4,angular_example4,rpg_example4,sas_example4, dspf_exampler4,dspf_examplea4,assembly_example4
from .prompt_code_to_business_logic import java_example1,python_example1,sql_example1,mongodb_example1,react_example1,angular_example1,rpg_example1,sas_example1, dspf_exampler1,dspf_examplea1,rpg_example11,rpg_example12
from .prompt_business_logic_to_mermaid_diagram import java_example2,python_example2,sql_example2,mongodb_example2,react_example2,angular_example2,rpg_example2,sas_example2, dspf_exampler2,dspf_examplea2
from .prompt_business_logic_to_mermaid_flowchart import java_example3,python_example3,sql_example3,mongodb_example3,react_example3,angular_example3,rpg_example3,sas_example3, dspf_exampler3,dspf_examplea3
from .prompt_business_logic_to_code import java_example4,python_example4,sql_example4,mongodb_example4,react_example4,angular_example4,rpg_example4,sas_example4, dspf_exampler4,dspf_examplea4
import keys
from dotenv import load_dotenv
from time import time
load_dotenv()
ChatAnthropic.api_key=os.getenv("ANTHROPIC_API_KEY")
ChatAnthropic.api_key=keys.anthropic_key
import logging

import hashlib 

def index(request):
    return JsonResponse({'Message':'Hello World. Welcome to CodeBridge'})

class FolderUploadView(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        project_name = request.POST.get('project_name') 
        username = request.user
        user = User.objects.get(username=username)

        
        parent_folder = FolderUpload.objects.create(foldername=project_name, parentFolder=None, user=user)
        root_folder = parent_folder.folderId

        files = request.FILES.getlist('files')  
        zip_file = request.FILES.get('zip_file')  

        if zip_file:
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, zip_file.name)
                with open(zip_path, 'wb') as f:
                    for chunk in zip_file.chunks():
                        f.write(chunk)
                
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir) 
                self.process_folder(temp_dir, parent_folder,request,root_folder)  

        for file in files:
            file_contents = file.read().decode('utf-8') 
            file_upload = FileUpload(
                filename=file.name,
                file=file_contents,  
                parentFolder=parent_folder,
                user=user
            )
            file_upload.save() 

        return Response("Files uploaded successfully")

    def process_folder(self, folder_path, parent_folder,request,root_folder):
        username = request.user
        user = User.objects.get(username=username)
        for item in os.listdir(folder_path): 
            item_path = os.path.join(folder_path, item) 
            if os.path.isdir(item_path):  
                subfolder = FolderUpload.objects.create(foldername=item, parentFolder=parent_folder, user=user)
                self.process_folder(item_path, subfolder,request,root_folder) 
            else:
                rpg_extensions = ['.rpgle', '.sqlrpgle', '.clle', '.RPGLE', '.SQLRPGLE', '.CLLE','.py','.java','.jsx','.tsx','.js','.ts','.sql','.PY','.JAVA','.JSX','.TSX','.JS','.TS','.SQL','.sas','.SAS']
                if any(item.endswith(ext) for ext in rpg_extensions):
                    with open(item_path, 'rb') as file:
                        print('fileSelected',item)
                        file_contents = file.read().decode('utf-8')
                        code_language = 'RPG'
                        file_upload = FileUpload(
                            filename=item,
                            file=file_contents,
                            parentFolder=parent_folder,
                            user=user,
                            code_language = code_language,
                            rootFolder = root_folder
                        )
                        file_upload.save()
                        print('fileUploaded',item)
    
    def get_folder_data(self, folder):
        folder_data = {
            'id': folder.folderId,
            'foldername': folder.foldername,
            'parentFolder': folder.parentFolder.folderId if folder.parentFolder else None,
            'user': folder.user.username,
            'files': [],
            'subfolders': [],
        }

        files = FileUpload.objects.filter(parentFolder=folder)
        for file in files:
            folder_data['files'].append({
                'id': file.fileId,
                'filename': file.filename,
                'user': file.user.username,
            })
        subfolders = FolderUpload.objects.filter(parentFolder=folder)
        for subfolder in subfolders:
            subfolder_data = self.get_folder_data(subfolder)
            folder_data['subfolders'].append(subfolder_data)

        return folder_data
       
    def get(self, request,folder_id=None):
        username = request.user
        user = User.objects.get(username=username)
        if folder_id:
            try:
                project = FolderUpload.objects.get(folderId=folder_id,user=user)
                folder_data = self.get_folder_data(project)
                return Response(folder_data)
            except FolderUpload.DoesNotExist:
                try:
                    project = FolderUpload.objects.get(folderId=folder_id)
                    shareable_link = ShareCode.objects.get(folder_structure__folderId=folder_id)
                    if user in shareable_link.users.all():
                        folder_data = self.get_folder_data(project)
                        return Response(folder_data)
                except ShareCode.DoesNotExist:
                    return Response('Folder not found', status=404)
                return Response('Folder not found', status=404)
        else:
            projects = FolderUpload.objects.filter(user=user, parentFolder=None)
            project_list = [
                {
                    'project_id': project.folderId,
                    'project_name': project.foldername
                }
                for project in projects
            ]
            shareable_links = ShareCode.objects.filter(users=user)
            for shareable_link in shareable_links:
                folder_data = FolderUpload.objects.get(folderId=shareable_link.folder_structure.folderId)
                project_list.append({
                    'project_id': folder_data.folderId,
                    'project_name': folder_data.foldername
                })

            return Response(project_list)

class FileContentAPIView(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, file_id):
        username = request.user
        user = User.objects.get(username=username)
        try:
            file = FileUpload.objects.get(fileId=file_id, user=request.user)
            serializer = FileSerializer(file)
            return Response(serializer.data)
        except FileUpload.DoesNotExist:
            try:
                file = FileUpload.objects.get(fileId=file_id)
                shareable_link = ShareCode.objects.get(folder_structure__folderId=file.rootFolder)
                if user in shareable_link.users.all():
                    serializer = FileSerializer(file)
                return Response(serializer.data)
            except:
                return Response({'error': 'File not found'}, status=404)
        
class LogicDetailAPIView(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, file_id, logic_id=None):
        try:
            file = FileUpload.objects.get(fileId=file_id, user=self.request.user)
            if logic_id:
                logic = Logic.objects.get(id=logic_id, file=file)
                return logic
            return file
        except FileUpload.DoesNotExist:
            raise Http404
        except Logic.DoesNotExist:
            raise Http404

    def get(self, request, file_id):
        file = self.get_object(file_id)
        try:
            logic = Logic.objects.get(file=file, user=request.user)
            serializer = LogicSerializer(logic)
        except Logic.DoesNotExist:
            return Response({'error': 'File not found'}, status=404)
        return Response(serializer.data)

    def post(self, request, file_id):
        
        username = request.user
        user = User.objects.get(username=username)
        
        if not file_id:
            return Response({'error': 'file_id is required'}, status=400)
        try:
            file = FileUpload.objects.get(fileId=file_id, user=user)
        except FileUpload.DoesNotExist:
            return Response({'error': 'File not found'}, status=404)
        logic_exists = Logic.objects.filter(file=file, user=user).exists()
        if logic_exists:
            logic = Logic.objects.filter(file=file, user=request.user).first()
            serializer = LogicSerializer(logic)
            return Response(serializer.data,status=200)
        code=file.file
        businessLogic =  business_logic(code)
        logicData = {
            'logic':businessLogic,
            'user':request.user,
            'file':file_id
        }
        serializer = LogicSerializer(data=logicData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
         return Response(serializer.errors, status=400)

    def put(self, request, file_id, logic_id):
        logic = self.get_object(file_id, logic_id)
        serializer = LogicSerializer(logic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, file_id, logic_id):
        logic = self.get_object(file_id, logic_id)
        logic.delete()
        return Response(status=204)
    
class JavaCodeAPIView(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, file_id, logic_id=None):
        try:
            file = FileUpload.objects.get(fileId=file_id, user=self.request.user)
            if logic_id:
                logic = Logic.objects.get(id=logic_id, file=file)
                return logic
            return file
        except FileUpload.DoesNotExist:
            raise Http404
        except Logic.DoesNotExist:
            raise Http404

    def generate_code(self, file_id, logic_id):
        file = self.get_object(file_id)
        logic = self.get_object(file_id, logic_id)
        logic_str = logic.logic
        generated_code = generateJava(logic_str) 
        code_data = {
            'code': generated_code,
            'logic': logic_id,
            'user': self.request.user,
            'file': file_id
        }
        
        existing_code = JavaCode.objects.filter(file=file, logic=logic, user=self.request.user).first()
        
        if existing_code:
            serializer = JavaCodeSerializer(existing_code, data=code_data)
        else:
            serializer = JavaCodeSerializer(data=code_data)
        
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            return None

    def get(self, request, file_id, logic_id):
        file = self.get_object(file_id)
        logic = self.get_object(file_id, logic_id)
        code = JavaCode.objects.filter(file=file, logic=logic, user=request.user)
        serializer = JavaCodeSerializer(code, many=True)
        return Response(serializer.data)

    def post(self, request, file_id, logic_id):
        if not file_id:
            return Response({'error': 'file_id is required'}, status=400)

        try:
            logic = self.get_object(file_id, logic_id)
        except FileUpload.DoesNotExist:
            return Response({'error': 'Logic not generated'}, status=404)

        file = self.get_object(file_id)
        code_exists = JavaCode.objects.filter(file=file, logic=logic, user=request.user).exists()

        if code_exists:
            code = JavaCode.objects.filter(file=file, logic=logic, user=request.user).first()
            serializer = JavaCodeSerializer(code)
            return Response(serializer.data, status=200)

        new_code_data = self.generate_code(file_id, logic_id)

        if new_code_data:
            return Response(new_code_data, status=201)
        else:
            return Response({'error': 'Failed to generate code'}, status=400)

    def put(self, request, file_id, logic_id):
        new_code_data = self.generate_code(file_id, logic_id)

        if new_code_data:
            return Response(new_code_data)
        else:
            return Response({'error': 'Failed to generate code'}, status=400)

    def delete(self, request, file_id, logic_id):
        logic = self.get_object(file_id, logic_id)
        file = self.get_object(file_id)
        code = JavaCode.objects.filter(file=file, logic=logic, user=request.user).first()
        code.delete()
        return Response(status=204)
  
# class MermaidAPIView(APIView):
#     permission_classes = [CustomIsAuthenticated]
#     authentication_classes = [TokenAuthentication]
#     def get_object(self, file_id, logic_id=None):
#         try:
#             file = FileUpload.objects.get(fileId=file_id, user=self.request.user)
#             if logic_id:
#                 logic = Logic.objects.get(id=logic_id, file=file)
#                 return logic
#             return file
#         except FileUpload.DoesNotExist:
#             raise Http404
#         except Logic.DoesNotExist:
#             raise Http404
#     def generate_diagrams(self, file_id, logic_id):
#         file = self.get_object(file_id)
#         logic = self.get_object(file_id, logic_id)
#         logic_str = logic.logic
#         mermaidDiagramClass = generateClassDiagram(logic_str)
#         mermaidDiagramFlow = generateFlowChart(logic_str)  
#         diagram_data = {
#             'classDiagram': mermaidDiagramClass,
#             'flowChart': mermaidDiagramFlow,
#             'logic': logic_id,
#             'user': self.request.user,
#             'file': file_id
#         }       
#         existing_diagram = MermaidDiagrams.objects.filter(file=file, logic=logic, user=self.request.user).first()      
#         if existing_diagram:
#             serializer = MermaidDiagramSerializer(existing_diagram, data=diagram_data)
#         else:
#             serializer = MermaidDiagramSerializer(data=diagram_data)        
#         if serializer.is_valid():
#             serializer.save()
#             return serializer.data
#         else:
#             return None
#     def get(self, request, file_id, logic_id):
#         file = self.get_object(file_id)
#         logic = self.get_object(file_id, logic_id)
#         diagram = MermaidDiagrams.objects.get(file=file, logic=logic, user=request.user)
#         serializer = MermaidDiagramSerializer(diagram)
#         return Response(serializer.data)
#     def post(self, request, file_id, logic_id):
#         if not file_id:
#             return Response({'error': 'file_id is required'}, status=400)
#         try:
#             logic = self.get_object(file_id, logic_id)
#         except FileUpload.DoesNotExist:
#             return Response({'error': 'Logic not generated'}, status=404)
#         file = self.get_object(file_id)
#         logicObj = self.get_object(file_id, logic_id)
#         try:
#             diagram = MermaidDiagrams.objects.get(file=file, logic=logicObj, user=request.user)
#             serializer = MermaidDiagramSerializer(diagram)
#             return Response(serializer.data)
#         except MermaidDiagrams.DoesNotExist:
#             new_diagram_data = self.generate_diagrams(file_id, logic_id)
#             if new_diagram_data:
#                 return Response(new_diagram_data, status=201)
#             else:
#                 return Response({'error': 'Failed to generate diagrams'}, status=400)
#     def put(self, request, file_id, logic_id):     
#         new_diagram_data = self.generate_diagrams(file_id, logic_id)
#         if new_diagram_data:
#             return Response(new_diagram_data)
#         else:
#             return Response({'error': 'Failed to generate diagrams'}, status=400)  
#     def delete(self, request, file_id, logic_id):
#         logic = self.get_object(file_id, logic_id)
#         file = self.get_object(file_id)
#         code = MermaidDiagrams.objects.filter(file=file, logic=logic, user=request.user).first()
#         code.delete()
#         return Response(status=204)    
               
class JavaCompilerView(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self,request):
        javaCompiler()
        return Response(status=200)

class LogicDetailAPIViewNew(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, file_id, logic_id=None):
        username = self.request.user
        user = User.objects.get(username=username)
        try:
            file = FileUpload.objects.get(fileId=file_id, user=self.request.user)
            if logic_id:
                logic = Logic.objects.get(id=logic_id, file=file)
                return logic
            return file
        except FileUpload.DoesNotExist:
            try:
                file = FileUpload.objects.get(fileId=file_id)
                shareable_link = ShareCode.objects.get(folder_structure__folderId=file.rootFolder)
                if user in shareable_link.users.all():
                    file = FileUpload.objects.get(fileId=file_id)
                    if logic_id:
                        logic = Logic.objects.get(id=logic_id, file=file)
                        return logic
                    return file
            except:
                return Response({'error': 'File not found'}, status=404)
            raise Http404
        except Logic.DoesNotExist:
            raise Http404
        
    def get_users_with_access(self,folder_structure_id):
        try:
            folder = FolderUpload.objects.get(folderId=folder_structure_id)
            owner = folder.user
            user = User.objects.get(username=self.request.user)

            if owner.username == self.request.user:
                shareable_link = ShareCode.objects.get(folder_structure_id=folder_structure_id)
                users_with_access = shareable_link.users.all()
                return users_with_access

            shareable_link = ShareCode.objects.get(folder_structure_id=folder_structure_id)
            if user in shareable_link.users.all():
                users_with_access = shareable_link.users.all()
                if owner not in users_with_access:
                    users_with_access = list(users_with_access)
                    users_with_access.remove(user)
                    users_with_access.append(owner)
                return users_with_access

        except (FolderUpload.DoesNotExist, ShareCode.DoesNotExist, User.DoesNotExist):
            pass

        return []

    def get(self, request, file_id):
        file = self.get_object(file_id)
        users = self.get_users_with_access(file.rootFolder)
        try:
            logics = Logic.objects.filter(file=file, user__in=users)
            serializer = LogicSerializer(logics, many=True)
        except Logic.DoesNotExist:
            return Response({'error': 'File not found'}, status=404)
        return Response(serializer.data)

    def post(self, request, file_id):
        
        username = request.user
        user = User.objects.get(username=username)
        
        if not file_id:
            return Response({'error': 'file_id is required'}, status=400)
        try:
            file = FileUpload.objects.get(fileId=file_id, user=user)
        except FileUpload.DoesNotExist:
            try:
                file = FileUpload.objects.get(fileId=file_id)
                shareable_link = ShareCode.objects.get(folder_structure__folderId=file.rootFolder)
                if user in shareable_link.users.all():
                    file = FileUpload.objects.get(fileId=file_id)
            except:
                return Response({'error': 'File not found'}, status=404)
        logic_exists = Logic.objects.filter(file=file, user=user).exists()
        if logic_exists:
            logic = Logic.objects.filter(file=file, user=request.user).first()
            serializer = LogicSerializer(logic)
            return Response(serializer.data,status=200)
        source = request.data.get('source')
        # destination = request.data.get('destination')
        code=file.file
        businessLogic =  code_to_business_logic(code,source)
        logicData = {
            'logic':businessLogic,
            'user':request.user,
            'file':file_id
        }
        serializer = LogicSerializer(data=logicData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=200)
 

    def put(self, request, file_id, logic_id):
        logic = self.get_object(file_id, logic_id)
        serializer = LogicSerializer(logic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, file_id, logic_id):
        logic = self.get_object(file_id, logic_id)
        logic.delete()
        return Response(status=204)
    
class CodeGenAPIViewNew(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, file_id, logic_id=None):
        username = self.request.user
        user = User.objects.get(username=username)
        try:
            file = FileUpload.objects.get(fileId=file_id, user=self.request.user)
            if logic_id:
                logic = Logic.objects.get(id=logic_id, file=file)
                return logic
            return file
        except FileUpload.DoesNotExist:
            try:
                file = FileUpload.objects.get(fileId=file_id)
                shareable_link = ShareCode.objects.get(folder_structure__folderId=file.rootFolder)
                if user in shareable_link.users.all():
                    file = FileUpload.objects.get(fileId=file_id)
                    if logic_id:
                        logic = Logic.objects.get(id=logic_id, file=file)
                        return logic
                    return file
            except:
                return Response({'error': 'File not found'}, status=404)
            raise Http404
        except Logic.DoesNotExist:
            raise Http404
        
    def get_users_with_access(self,folder_structure_id):
        try:
            folder = FolderUpload.objects.get(folderId=folder_structure_id)
            owner = folder.user
            user = User.objects.get(username=self.request.user)

            if owner.username == self.request.user:
                shareable_link = ShareCode.objects.get(folder_structure_id=folder_structure_id)
                users_with_access = shareable_link.users.all()
                return users_with_access

            shareable_link = ShareCode.objects.get(folder_structure_id=folder_structure_id)
            if user in shareable_link.users.all():
                users_with_access = shareable_link.users.all()
                if owner not in users_with_access:
                    users_with_access = list(users_with_access)
                    users_with_access.remove(user)
                    users_with_access.append(owner)
                return users_with_access

        except (FolderUpload.DoesNotExist, ShareCode.DoesNotExist, User.DoesNotExist):
            pass

        return []

    def generate_code(self, file_id, logic_id, source, destination):
        file = self.get_object(file_id)
        logic = self.get_object(file_id, logic_id)
        logic_str = logic.logic
        # var="RPG"
        generated_code = business_logic_to_code(logic_str,source, destination,file.file) 
        code_data = {
            'code': generated_code,
            'logic': logic_id,
            'user': self.request.user,
            'file': file_id,
            'language_converted' : destination
        }
        
        existing_code = JavaCode.objects.filter(file=file, logic=logic, user=self.request.user, language_converted = destination).first()
        
        if existing_code:
            serializer = JavaCodeSerializer(existing_code, data=code_data)
        else:
            serializer = JavaCodeSerializer(data=code_data)
        
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            return None

    def get(self, request, file_id):
        file = self.get_object(file_id)
        # logic = self.get_object(file_id, logic_id)
        users = self.get_users_with_access(file.rootFolder)
        code = JavaCode.objects.filter(file=file,  user__in=users)
        serializer = JavaCodeSerializer(code, many=True)
        return Response(serializer.data)

    def post(self, request, file_id, logic_id):
        if not file_id:
            return Response({'error': 'file_id is required'}, status=400)

        try:
            logic = self.get_object(file_id, logic_id)
        except FileUpload.DoesNotExist:
            return Response({'error': 'Logic not generated'}, status=404)
        
        source = request.data.get('source')
        destination = request.data.get('destination')

        file = self.get_object(file_id)
        code_exists = JavaCode.objects.filter(file=file, logic=logic, user=request.user,language_converted = destination).exists()# github rep collab check instead of user

        if code_exists:
            code = JavaCode.objects.filter(file=file, logic=logic, user=request.user, language_converted = destination).first()
            serializer = JavaCodeSerializer(code)
            return Response(serializer.data, status=200)

       
        new_code_data = self.generate_code(file_id, logic_id, source, destination)

        if new_code_data:
            return Response(new_code_data, status=201)
        else:
            return Response({'error': 'Failed to generate code'}, status=400)

    def put(self, request, file_id, logic_id):
        source = request.data.get('source')
        destination = request.data.get('destination')
        new_code_data = self.generate_code(file_id, logic_id, source, destination)

        if new_code_data:
            return Response(new_code_data)
        else:
            return Response({'error': 'Failed to generate code'}, status=400)

    def delete(self, request, file_id, logic_id):
        logic = self.get_object(file_id, logic_id)
        file = self.get_object(file_id)
        code = JavaCode.objects.filter(file=file, logic=logic, user=request.user).first()
        code.delete()
        return Response(status=204)
   
class MermaidAPIViewNew(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, file_id, logic_id=None):
        username = self.request.user
        user = User.objects.get(username=username)
        try:
            file = FileUpload.objects.get(fileId=file_id, user=self.request.user)
            if logic_id:
                logic = Logic.objects.get(id=logic_id, file=file)
                return logic
            return file
        except FileUpload.DoesNotExist:
            try:
                file = FileUpload.objects.get(fileId=file_id)
                shareable_link = ShareCode.objects.get(folder_structure__folderId=file.rootFolder)
                if user in shareable_link.users.all():
                    file = FileUpload.objects.get(fileId=file_id)
                    if logic_id:
                        logic = Logic.objects.get(id=logic_id, file=file)
                        return logic
                    return file
            except:
                return Response({'error': 'File not found'}, status=404)
            raise Http404
        except Logic.DoesNotExist:
            raise Http404
        
    def get_users_with_access(self,folder_structure_id):
        try:
            folder = FolderUpload.objects.get(folderId=folder_structure_id)
            owner = folder.user
            user = User.objects.get(username=self.request.user)

            if owner.username == self.request.user:
                shareable_link = ShareCode.objects.get(folder_structure_id=folder_structure_id)
                users_with_access = shareable_link.users.all()
                return users_with_access

            shareable_link = ShareCode.objects.get(folder_structure_id=folder_structure_id)
            if user in shareable_link.users.all():
                users_with_access = shareable_link.users.all()
                if owner not in users_with_access:
                    users_with_access = list(users_with_access)
                    users_with_access.remove(user)
                    users_with_access.append(owner)
                return users_with_access

        except (FolderUpload.DoesNotExist, ShareCode.DoesNotExist, User.DoesNotExist):
            pass

        return []

    def generate_diagrams(self, file_id, logic_id, source, destination,diagram_type = None):
        file = self.get_object(file_id)
        logic = self.get_object(file_id, logic_id)
        logic_str = logic.logic
        # var="RPG"
        existing_diagram = MermaidDiagrams.objects.filter(file=file, logic=logic, user=self.request.user).first()
        if existing_diagram:
            if diagram_type == 'classDiagram':
                mermaidDiagramClass = business_logic_to_mermaid_diagram(logic_str,source, destination)
                print('hi',mermaidDiagramClass)
                mermaidDiagramFlow = existing_diagram.flowChart
            elif diagram_type == 'flowChart':
                mermaidDiagramClass = existing_diagram.classDiagram
                mermaidDiagramFlow = business_logic_to_mermaid_flowchart(logic_str,source, destination)
        else:
            mermaidDiagramClass = business_logic_to_mermaid_diagram(logic_str,source, destination)
            mermaidDiagramFlow = business_logic_to_mermaid_flowchart(logic_str,source, destination)

        
        diagram_data = {
            'classDiagram': mermaidDiagramClass,
            'flowChart': mermaidDiagramFlow,
            'logic': logic_id,
            'user': self.request.user,
            'file': file_id
        }
                
        if existing_diagram:
            serializer = MermaidDiagramSerializer(existing_diagram, data=diagram_data)
        else:
            serializer = MermaidDiagramSerializer(data=diagram_data)
        
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            return None

    def get(self, request, file_id):
        file = self.get_object(file_id)
        users = self.get_users_with_access(file.rootFolder)
        diagram = MermaidDiagrams.objects.filter(file=file, user__in=users)
        serializer = MermaidDiagramSerializer(diagram,many=True)
        return Response(serializer.data)

    def post(self, request, file_id, logic_id):
        if not file_id:
            return Response({'error': 'file_id is required'}, status=400)
        try:
            logic = self.get_object(file_id, logic_id)
        except FileUpload.DoesNotExist:
            return Response({'error': 'Logic not generated'}, status=404)
        file = self.get_object(file_id)
        logicObj = self.get_object(file_id, logic_id)
        try:
            diagram = MermaidDiagrams.objects.get(file=file, logic=logicObj, user=request.user)
            serializer = MermaidDiagramSerializer(diagram)
            return Response(serializer.data)
        except MermaidDiagrams.DoesNotExist:
            source = request.data.get('source')
            destination = request.data.get('destination')
            new_diagram_data = self.generate_diagrams(file_id, logic_id, source, destination)
            if new_diagram_data:
                return Response(new_diagram_data, status=201)
            else:
                return Response({'error': 'Failed to generate diagrams'}, status=400)

    def put(self, request, file_id, logic_id):
        diagram_type = request.data.get('diagram_type', None)
        source = request.data.get('source')
        destination = request.data.get('destination')

        if diagram_type not in ['classDiagram', 'flowChart']:
            return Response({'error': 'Invalid diagram_type parameter'}, status=status.HTTP_400_BAD_REQUEST)

        new_diagram_data = self.generate_diagrams(file_id, logic_id, source, destination, diagram_type)

        if new_diagram_data:
            return Response(new_diagram_data)
        else:
            return Response({'error': 'Failed to generate diagrams'}, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, file_id, logic_id):
        logic = self.get_object(file_id, logic_id)
        file = self.get_object(file_id)
        code = MermaidDiagrams.objects.filter(file=file, logic=logic, user=request.user).first()
        code.delete()
        return Response(status=204)    

import os
import requests
from django.shortcuts import redirect
from django.http import JsonResponse
import uuid 
from django.core.cache import cache

def github_oauth_callback(request):
    code = request.GET.get('code')

    client_id = os.environ.get("GITHUB_CLIENT_ID")
    client_secret = os.environ.get("GITHUB_CLIENT_SECRET")
    response = requests.post(
        'https://github.com/login/oauth/access_token',
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
        },
        headers={
            'Accept': 'application/json',
        }
    )

    data = response.json()
    access_token = data.get('access_token')
    if access_token:
        oauth_identifier = generate_unique_identifier() 
        store_temporary_github_token(oauth_identifier, access_token)
        return redirect(f'http://localhost:5173/repositories?oauth_identifier={oauth_identifier}')

    return JsonResponse({'error': 'Unable to obtain GitHub access token'})

def generate_unique_identifier():
    return str(uuid.uuid4())

def store_temporary_github_token(oauth_identifier, access_token):
    cache.set(oauth_identifier, access_token, 1800)

def retrieve_temporary_github_token(oauth_identifier):
    access_token = cache.get(oauth_identifier)
    return access_token

def remove_temporary_github_token(oauth_identifier):
    cache.delete(oauth_identifier)

class GithubAccessView(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self,request):
        oauth_identifier = request.GET.get('oauth_identifier')
        access_token = retrieve_temporary_github_token(oauth_identifier)
        if access_token:
            username = request.user
            user_profile = User.objects.get(username=username)
            user_profile.access_token = access_token
            user_profile.save()
            remove_temporary_github_token(oauth_identifier)
            return JsonResponse({'message': 'GitHub access token associated successfully'})
        else:
            return JsonResponse({'error': 'GitHub access token not found or expired'})

    def post(self,request):
        username = request.user
        user_profile = User.objects.get(username=username)
        access_token = user_profile.access_token

        if access_token:
            headers = {
                'Authorization': f'Bearer {access_token}',
            }
            github_api_url = 'https://api.github.com/user/repos'
            params = {
                'visibility': 'all',  # 'all' includes both public and private repositories
            }
            
            all_repositories = []
            while True:
                response = requests.get(github_api_url, headers=headers, params=params)
                
                if response.status_code == 200:
                    repositories = response.json()
                    all_repositories.extend(repositories)
                    
                    if 'next' in response.links:
                        github_api_url = response.links['next']['url']
                    else:
                        break
                else:
                    return JsonResponse({'error': 'Failed to fetch GitHub repositories'}, status=response.status_code)

            return JsonResponse({'repositories': all_repositories})
        else:
            return JsonResponse({'error': 'GitHub access token not found'})

import git
import tempfile
import shutil
import os
from .models import ClonedRepository
from urllib.parse import urlparse

class CloneRepositoryAPIView(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_repository_name_from_url(repository_url):
        parsed_url = urlparse(repository_url)
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) >= 2:
            return path_parts[-2] 
        return None

    def process_folder(self, folder_path, parent_folder,user):
        for item in os.listdir(folder_path): 
            item_path = os.path.join(folder_path, item) 
            if os.path.isdir(item_path):  
                subfolder = FolderUpload.objects.create(foldername=item, parentFolder=parent_folder, user=user)
                self.process_folder(item_path, subfolder,user) 
            else:
                rpg_extensions = ['.rpgle', '.sqlrpgle', '.clle', '.RPGLE', '.SQLRPGLE', '.CLLE','.py','.java','.jsx','.tsx','.js','.ts','.sql','.PY','.JAVA','.JSX','.TSX','.JS','.TS','.SQL']
                if any(item.endswith(ext) for ext in rpg_extensions):
                    with open(item_path, 'rb') as file:
                        print('fileSelected',item)
                        file_contents = file.read().decode('utf-8')
                        code_language = detectLanguage(file_contents)
                        file_upload = FileUpload(
                            filename=item,
                            file=file_contents,
                            parentFolder=parent_folder,
                            user=user,
                            code_language = code_language
                        )
                        file_upload.save()
                        print('fileUploaded',item)

    # def clone_github_repository(self,repository_url, branch_name, access_token, user_profile, repository_name=None):
      
    #     try:
    #         with tempfile.TemporaryDirectory() as temp_dir:
    #             git_url = f"https://{access_token}@github.com/{repository_url.split('/')[3]}/{repository_url.split('/')[4]}.git"
                
    #             git.Repo.clone_from(git_url, temp_dir, depth=1, branch=branch_name)
    #             parent_folder = FolderUpload.objects.create(foldername=repository_name, parentFolder=None, user=user_profile)

    #             self.process_folder(temp_dir,parent_folder=parent_folder,user=user_profile)
    #             if not repository_name:
    #                 repository_name = self.get_repository_name_from_url(repository_url)
    #             cloned_repo = ClonedRepository(
    #                 user=user_profile,
    #                 repository_name=repository_name,  
    #                 repository_url=repository_url,
    #                 branch=branch_name,  
    #             )
    #             cloned_repo.save()
                
    #         return True
    #     except git.exc.GitCommandError as e:
    #         print(f"Error cloning repository: {str(e)}")
    #         return False
    def user_has_access(self, user_profile, repository_url, branch_name):
        try:
            parts = repository_url.split('/')
            owner = parts[3]
            repo_name = parts[4].split('.')[0]  # Remove '.git' from repo name
            
            access_token = user_profile.access_token  
            
            url = f'https://api.github.com/repos/{owner}/{repo_name}/collaborators'
            headers = {'Authorization': f'token {access_token}'}

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error checking repository access: {str(e)}")
            return False
    
    def clone_github_repository(self, repository_url, branch_name, access_token, user_profile, repository_name=None):
        try:
            existing_cloned_repo = ClonedRepository.objects.filter(repository_url=repository_url, branch=branch_name).first()
            if existing_cloned_repo:
                if not self.user_has_access(user_profile, repository_url, branch_name):
                    return "User does not have access to clone this repository."
                existing_cloned_repo.users.add(user_profile)
            else:

                with tempfile.TemporaryDirectory() as temp_dir:
                    git_url = f"https://{access_token}@github.com/{repository_url.split('/')[3]}/{repository_url.split('/')[4]}.git"
                    
                    git.Repo.clone_from(git_url, temp_dir, depth=1, branch=branch_name)
                    parent_folder = FolderUpload.objects.create(foldername=repository_name, parentFolder=None, user=user_profile)

                    self.process_folder(temp_dir, parent_folder=parent_folder, user=user_profile)
                    if not repository_name:
                        repository_name = self.get_repository_name_from_url(repository_url)

                    cloned_repo = ClonedRepository(
                        repository_name=repository_name,
                        repository_url=repository_url,
                        branch=branch_name,
                        folder_id=parent_folder
                    )
                    cloned_repo.save()
                    cloned_repo.users.set([user_profile])
                
            return True
        except git.exc.GitCommandError as e:
            print(f"Error cloning repository: {str(e)}")
            return False

    def post(self, request):
        repository_url = request.data.get('repository_url')
        branch_name = request.data.get('branch_name')
        username = request.user
        user_profile = User.objects.get(username=username)
        access_token = user_profile.access_token
        repository_name = request.data.get('repository_name')
        result = self.clone_github_repository(repository_url, branch_name, access_token, user_profile, repository_name)

        if result:
            return Response({'message': 'Repository cloned and processed successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to clone repository'}, status=status.HTTP_400_BAD_REQUEST)

class CreateGitHubRepository(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self,request):
        username = request.user
        repos = GitHubRepository.objects.filter(collaborators__username=username)
        unique_repository_urls = set()
        unique_repos = []
        for repo in repos:
            if repo.repository_url not in unique_repository_urls:
                unique_repos.append(repo)
                unique_repository_urls.add(repo.repository_url)
        serializer = GithubRepositorySerializer(unique_repos,many=True)
        return Response(serializer.data)

    def post(self, request):
        username = request.user
        user_profile = User.objects.get(username=username)
        access_token = user_profile.access_token
        repository_name = request.data.get('repository_name')
        description = request.data.get('description')

        response = create_repository(access_token, repository_name, description)

        if response:
            repository_url = response.get('html_url')
            owner = get_git_repo_owner(repository_url)
            try:    
                self.perform_initial_commit(access_token, owner, repository_name, branch_name='main')
            except Exception as e:
                print(e)

            try:    
                commit = self.get_commit(access_token, owner, repository_name,'main')
            except Exception as e:
                print(e)
            github_repo = GitHubRepository.objects.create(
                owner=owner,
                repository_name=repository_name,
                repository_url=repository_url,
                branch="main",
                commit_sha=commit
                
            )
            github_repo.collaborators.add(user_profile)

            return Response({'message': 'GitHub repository created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create GitHub repository'}, status=status.HTTP_400_BAD_REQUEST)
        
    def perform_initial_commit(self,access_token, owner, repo_name, branch_name='main'):
        url = f'https://api.github.com/repos/{owner}/{repo_name}/contents/README.md'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/vnd.github.v3+json',
        }
        
        content = base64.b64encode('This is the initial commit of the repository.'.encode()).decode()
        
        data = {
            'message': 'Initial commit',
            'content': content,
            'branch': branch_name,
        }

        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 201:
            return True
        else:
            print(f"Failed to create initial commit: {response.text}")
            return False
        
    def get_commit(self,access_token, owner, repo, default_branch):
        url = f'https://api.github.com/repos/{owner}/{repo}/commits/{default_branch}'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            commit_data = response.json()
            return commit_data['sha']
        else:
            print(f"Failed to get latest commit SHA: {response.text}")
            return None     

class CreateGitHubBranch(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        username = request.user
        user_profile = User.objects.get(username=username)
        access_token = user_profile.access_token
        url = request.data.get('repository_url')
        branch_name = request.data.get('branch_name')
        start_branch = request.data.get('start_branch')
         

        try:
            github_repo = GitHubRepository.objects.get(repository_url=url , branch = start_branch)
        except GitHubRepository.DoesNotExist:
            return Response({'error': 'GitHub repository not found'}, status=status.HTTP_404_NOT_FOUND)

        owner = github_repo.owner
        repo = github_repo.repository_name
        start_sha = github_repo.commit_sha
        collaborators_to_add = github_repo.collaborators.all()


        response = create_github_branch(access_token, owner, repo, branch_name, start_sha)

        if response:
            owner = get_git_repo_owner(url)
            commit = self.get_commit(access_token,owner,repo,branch_name)
            new_branch = GitHubRepository.objects.create(
                owner=owner,
                repository_name=repo,
                repository_url=url,
                branch=branch_name,
                commit_sha = commit
                
            )
            new_branch.collaborators.add(*collaborators_to_add)
            new_branch.save()

            return Response({'message': 'GitHub branch created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create GitHub branch'}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_commit(self,access_token, owner, repo, default_branch):
        url = f'https://api.github.com/repos/{owner}/{repo}/commits/{default_branch}'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            commit_data = response.json()
            return commit_data['sha']
        else:
            print(f"Failed to get latest commit SHA: {response.text}")
            return None
        
class ListBranches(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        username = request.user
        user_profile = User.objects.get(username=username)
        access_token = user_profile.access_token
        url = request.data.get('url')
        owner = get_git_repo_owner(url)
        repo = request.data.get('name')
        branches = self.get_repository_branches(access_token, owner, repo)

        if branches:
            return Response({'branches': branches})
        else:
            return Response({'error': 'Failed to retrieve branches'}, status=status.HTTP_400_BAD_REQUEST)

    def get_repository_branches(self, access_token, owner, repo):
        url = f'https://api.github.com/repos/{owner}/{repo}/branches'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            branches_data = response.json()
            branches = [branch['name'] for branch in branches_data]
            return branches
        else:
            print(f"Failed to retrieve branches: {response.text}")
            return None
        
class PullCodeFromGitHub(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        repository_url = request.data.get('repository_url')
        parts = repository_url.strip("/").split("/")
        owner, repo = parts[-2], parts[-1]
        branch = request.data.get('branch_name')
        try:
            username = request.user
            user_profile = User.objects.get(username=username)
            access_token = user_profile.access_token

            api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/json',
            }

            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                contents = response.json().get('tree', [])

                file_contents = []

                for item in contents:
                    if item['type'] == 'blob':
                        file_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{item['path']}?ref={branch}"
                        file_response = requests.get(file_url, headers=headers)

                        if file_response.status_code == 200:
                            file_data = file_response.json()
                            file_content_base64 = file_data['content']

                            file_content = base64.b64decode(file_content_base64).decode('utf-8')

                            file_contents.append({
                                'path': item['path'],
                                'content': file_content,
                            })
                        else:
                            error_message = f"Failed to fetch content for {item['path']}. Status code: {file_response.status_code}"
                            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(file_contents, status=status.HTTP_200_OK)
            else:
                error_message = response.text
                return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except GitHubRepository.DoesNotExist:
            return Response({'error': 'GitHubRepository not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.db.models import Q

class PushCodeToGitHub(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        repository_url = request.data.get('repository_url') 
        branch = request.data.get('branch')
        commit_message = request.data.get('commit_message')
        file_ids = request.data.get('file_ids')
        destination = request.data.get('destination')
        try:
            username = request.user
            user_profile = User.objects.get(username=username)
            access_token = user_profile.access_token

            # file = FileUpload.objects.get(fileId=file_id)
            # root_folder_id = file.rootFolder
            # code_files = JavaCode.objects.filter(file__rootFolder=root_folder_id)
            code_files = JavaCode.objects.filter(file__fileId__in=file_ids,user=self.request.user,language_converted = destination)
            response = push_to_github(access_token, repository_url, code_files ,branch , commit_message)
            if response:
                # repository_info = GitHubRepository.objects.get(repository_url=repository_url, branch=branch)
                # self.update_repository_info(code_files=code_files,repository_info=repository_info)
                return Response({'Message': "Pushed Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({'Error': "Git Push Failed"})
        except User.DoesNotExist: 
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update_repository_info(self,code_files, repository_info):
        new_code_entries = []
        for code_file in code_files:
            if not code_file.repository:
                code_file.repository = repository_info
                code_file.save()
            elif code_file.repository == repository_info:
                pass
            else:
                new_code_entry = JavaCode(
                code=code_file.code,
                logic=code_file.logic,
                user=code_file.user,
                file=code_file.file,
                repository=repository_info,
                language_converted=code_file.language_converted
                )
                if new_code_entry:
                    new_code_entries.append(new_code_entry)
        if new_code_entries:
                    JavaCode.objects.bulk_create(new_code_entries)

class CreatePullRequest(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        username = request.user
        user_profile = User.objects.get(username=username)
        access_token = user_profile.access_token 
        owner = request.data.get('owner')
        repo_name = request.data.get('repo_name')
        base_branch = request.data.get('base_branch')
        head_branch = request.data.get('head_branch')
        title = request.data.get('title')
        body = request.data.get('body', '')

        pull_request = self.create_pull_request(access_token, owner, repo_name, base_branch, head_branch, title, body)

        if pull_request:
            return Response({'message': f"Pull request created successfully: {pull_request['html_url']}"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create pull request.'}, status=status.HTTP_400_BAD_REQUEST)

    def create_pull_request(self, access_token, owner, repo_name, base_branch, head_branch, title, body=''):
        url = f'https://api.github.com/repos/{owner}/{repo_name}/pulls'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/vnd.github.v3+json',
        }
        data = {
            'title': title,
            'body': body,
            'head': head_branch,
            'base': base_branch,
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Failed to create pull request: {response.text}")
            return None
    
class GenerateUUID(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        serializer = ShareCodeSerializer(data=request.data)
        if serializer.is_valid():
            folder_structure_id = serializer.validated_data['folder_structure_id']
            print(folder_structure_id)
            try:
                folder_structure = FolderUpload.objects.get(folderId=folder_structure_id, user=request.user)
                shareable_link, created = ShareCode.objects.get_or_create(folder_structure=folder_structure)
                return Response({'uuid': shareable_link.uuid}, status=status.HTTP_201_CREATED)
            except FolderUpload.DoesNotExist:
                return Response({'error': 'Folder not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccessRepository(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        uuid = request.data.get('uuid')
        try:
            shareable_link = ShareCode.objects.get(uuid=uuid)
            folder_structure = shareable_link.folder_structure
            if request.user not in shareable_link.users.all():
                shareable_link.users.add(request.user)
            return Response({'repository_id': folder_structure.folderId, 'repositoryname': folder_structure.foldername}, status=status.HTTP_200_OK)
        except ShareCode.DoesNotExist:
            return Response({'error': 'Repository not found'}, status=status.HTTP_404_NOT_FOUND)
        


# Calculate Token

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def file_business_logic(code): 
    source="RPG"   
    if source.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas","dspfr","dspfa","assembly"]:
        return "Invalid source specified."
    
    example_code="" 
    if(source.lower()=="java"):
        example_code=java_example1   
    elif(source.lower()=="python"):
       example_code=python_example1
    elif(source.lower()=="sql"):
        example_code=sql_example1
    elif(source.lower()=="mongodb"):
        example_code=mongodb_example1
    elif(source.lower()=="angular"):
        example_code=angular_example1
    elif(source.lower()=="react"):
        example_code=react_example1
    elif(source.lower()=="rpg"):
        example_code=rpg_exampleh
    elif(source.lower()=="sas"):
        example_code=sas_example1
    elif(source.lower()=="dspfr"):
        example_code=dspf_exampler1
    elif(source.lower()=="dspfa"):
        example_code=dspf_examplea1
    elif(source.lower()=="assembly"):
        example_code=assembly_example1
    
    template='''Pretend to be an expert in {source} code and provide a comprehensive explanation of the user-provided {source} code, converting it into
    understandable business logic. If the variables in the code have values relevant to the business logic, please include them.I am interested 
    solely in the business logic and do not require introductory statements such as 'Here is the business logic extracted from this code.'
    Your task also involves analyzing the code, identifying its core functionality, and presenting this functionality clearly and concisely. 
    Ensure that the extracted business logic is well-documented.
    This process involves multiple steps:
    1.Analyze the provided {source} code to comprehend its purpose.
    2.Identify and abstract the key algorithmic steps and logic used in the {source} code.
    3.Express this logic in a high-level, language-agnostic format.
    4.Identify the type of code and if there is any database, other files or ui interaction.
    5.Any important information about the file structure should be identified and added to the interactions. 
    6.Please specify these interactions towards the end of the generated response in a well formatted manner.
    7.Be as verbose as needed.
    Make sure that the output provides a clear and concise representation of the business logic within the {source} code. If the {source} code is complex,
    please include comments or explanations to clarify the logic.I am providing an example how to generate business logic 
    using the {source} code as shown in the following example.
    
    Example:
    {example_code}
    
    Now the User will provide {source} code, please generate correct buisness logic as shown in above example.
    Share business logic and related files like database , ui and other files as part of the response.
    User: {input}
    Business_Logic:
    '''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","source","example_code"], template=template),
        verbose=True,
    )
    logic= llm_chain.predict(input=code,source=source,example_code=example_code)
    return f"{logic}"

# Higher Level Business Logic For all Files at a same time

def higher_level_business_logic(business_logic,folder_name):
    
    template='''I would like to generate comprehensive higher-level business logic for a specific folder, which is identified by the name {folder_name}. This business logic
    should encompass the entirety of the folder, including all subfiles and subfolder files, in order to provide developers with a clear and concise overview of the code
    within this directory. The objective is to make it easier for developers to understand the codebase contained in this folder.

    The process involves the user providing the business logic for all the files and subfolder files within the specified directory. After gathering this information, 
    I will synthesize a higher-level business logic that summarizes the individual inputs. It's important to note that this higher-level business logic should also be
    suitable for generating a mermaid flowchart diagram. This diagram will serve as a visual representation of the folder's code structure, utilizing the synthesized 
    business logic to create an informative visual aid.

    User: {input}
    Higher_Level_Business_Logic:
    
    '''
    
    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","folder_name"], template=template),
        verbose=True,
    )
    
    logic= llm_chain.predict(input=business_logic,folder_name=folder_name)
    return logic

def process_folder_business_logic(parent_folder_id):    
    
    try:
        folder = FolderUpload.objects.get(folderId=parent_folder_id)
        folder_name = folder.foldername
        folder_business_logic_dict = {}
        
        files = FileUpload.objects.filter(parentFolder=folder)
        for file in files:
            try:
                existing_logic = Logic.objects.get(file=file)
                file_logic = existing_logic.logic
            except:
                file_logic = file_business_logic(file.file)
            folder_business_logic_dict[file.filename] = file_logic

        subfolders = FolderUpload.objects.filter(parentFolder=folder)
        for subfolder in subfolders:
            subfolder_logic = process_folder_business_logic(subfolder.folderId)
            folder_business_logic_dict[subfolder.foldername] = subfolder_logic
            
        try:
            logic = higher_level_business_logic(folder_business_logic_dict,folder_name)
            return logic
        except:
            return "Error"
        
    except FolderUpload.DoesNotExist:
        logging.error(f"Folder with ID {parent_folder_id} not found.")
        return ""
    except Exception as e:
        logging.error(f"An error occurred while processing folder {parent_folder_id}: {str(e)}")
        return ""
    
# Higher Level Business Logic one by one to handle token problems
 
def get_folder_structure(folder_id):
    
    folder = FolderUpload.objects.get(folderId=folder_id)
    
    folder_structure = {
        'files': [],
    }

    subfolders = FolderUpload.objects.filter(parentFolder=folder)
    files = FileUpload.objects.filter(parentFolder=folder)

    for subfolder in subfolders:
        subfolder_structure = get_folder_structure(subfolder.folderId)
        folder_structure.setdefault('sub_folders', []).append({
            'folder_name': subfolder.foldername,
            'content': subfolder_structure
        })

    for file in files:
        folder_structure['files'].append(file.filename)

    return folder_structure
 
def combine_business_logic(folder_name,
                           folder_structure,
                           files_name,
                           previous_business_logic,
                           current_directory_name,
                           current_directory_business_logic):
    
    template='''Assume the role of a system design expert.

    You are tasked with creating a comprehensive high-level business logic overview for a module identified by the name {folder_name}. 
    This overview should encompass the entire module, providing developers with a clear and concise understanding of its business logic.
    The primary goal is to facilitate developers' comprehension of the module's overall business logic.

    The process involves users supplying business logic for all files and subfolder files within the specified directory individually. Once this
    information is gathered, you will synthesize higher-level business logic that summarizes the individual inputs. It is essential to note that 
    this higher-level business logic should be easy for developers to understand and suitable for generating a mermaid flowchart diagram, serving
    as a visual representation of the folder's code structure. This diagram will utilize the synthesized business logic to create an informative
    visual aid.

    Higher-Level Business Logic includes the interaction of files and higher business logic encompasses all files' logic.

    The folder structure is as follows: '{folder_structure}'.

    Please combine the previously provided business logic with the current directory's business logic. The previous business logic pertains to 
    the files named {files_name}, while the current directory business logic relates to the file named {current_directory_name}.

    Previous Business Logic =

    {previous_business_logic}

    Current Directory Business Logic =

    {current_directory_business_logic}

    Combined Business Logic =
    '''

    llm_chain = LLMChain(llm=ChatAnthropic(temperature=0.8,model="claude-2.0",max_tokens_to_sample=100000),
    prompt=PromptTemplate(input_variables=["folder_name","folder_structure","previous_business_logic","current_directory_name","current_directory_business_logic"],
            template=template),
        verbose=True,
    )

    logic= llm_chain.predict(folder_name=folder_name,
                             folder_structure=folder_structure,
                             files_name=files_name,
                             previous_business_logic=previous_business_logic,
                             current_directory_name=current_directory_name,
                             current_directory_business_logic=current_directory_business_logic)
    return f"{logic}"    

def process_folder_business_logic_1Y1(parent_folder_id):    
    
    try:
        folder = FolderUpload.objects.get(folderId=parent_folder_id)
        folder_name = folder.foldername
        folder_structure=get_folder_structure(parent_folder_id)
        folder_business_logic=""
        
        files_name=[]
        
        files = FileUpload.objects.filter(parentFolder=folder)
        
        for file in files:
            files_name.append(file.filename)
            
            try:
                existing_logic = Logic.objects.get(file=file)
                file_logic = existing_logic.logic
            except:
                file_logic = file_business_logic(file.file)
                
            if (folder_business_logic==""):
                folder_business_logic = file_logic
            else:
                folder_business_logic = combine_business_logic(folder_name, folder_structure,files_name, folder_business_logic, file.filename, file_logic)
    
        subfolders = FolderUpload.objects.filter(parentFolder=folder)
        
        for subfolder in subfolders:
            files_name.append(subfolder.foldername)
            subfolder_business_logic = process_folder_business_logic(subfolder.folderId)
            
            if(folder_business_logic==""):
                folder_business_logic=subfolder_business_logic
            else:
                folder_business_logic = combine_business_logic(folder_name, folder_structure,files_name, folder_business_logic, subfolder.foldername, subfolder_business_logic)

        return folder_business_logic
        
    except FolderUpload.DoesNotExist:
        logging.error(f"Folder with ID {parent_folder_id} not found.")
        return ""
    except Exception as e:
        logging.error(f"An error occurred while processing folder {parent_folder_id}: {str(e)}")
        return ""

# Higher Level Business API View

class HigherLevelBusinessLogic(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        folder_id = request.data.get('id') 
        
        existing_logic = HighLevel.objects.filter(user=request.user,folder_id=folder_id).first()
        if existing_logic:
            serializer = HighLevelSerializer(existing_logic)
            return Response(serializer.data, status=201)
        else:
            business_logic = process_folder_business_logic(folder_id)
            # business_logic = process_folder_business_logic_1Y1(folder_id)

            logicData = {
                'logic':business_logic,
                'user':request.user,
                'folder_id':folder_id
            }
            serializer = HighLevelSerializer(data=logicData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
         return Response(serializer.errors, status=400)
        # print(business_logic)
        # return Response({"response":business_logic}, status=200)
      
# Higher Level Mermaid Diagram

def higher_level_mermaid_diagram(business_logic):
    
    classDiagram_schema = ResponseSchema(name='mermaid_class_diagram_code', description='This schema represents the Mermaid class diagram code, which is compatible with MermaidJS version 8.11.0. The code should be represented as a valid JSON string with new lines replaced with "\\n".')
    classDiagram_description_schema = ResponseSchema(name='mermaid_class_diagram_code_description', description='This schema represents the description of the class diagram code generated by MermaidJS.')

    response_schema = (classDiagram_schema,classDiagram_description_schema)
    parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = parser.get_format_instructions()
    
    example_code=rpg_example2
    
    template='''I would like to generate code using backticks to create a Mermaid Class diagram that represents the high-level business logic 
    of a codebase. This Mermaid diagram serves the purpose of visualizing the interplay of business logic within a codebase, showcasing how 
    different files interact with one another. If certain files do not interact, we should still generate Mermaid diagrams for them.

    In accordance with this, please generate Mermaid code that encapsulates the business logic of an entire codebase.

    Additionally, please ensure that the provided code is in the correct syntax, compatible with rendering using mermaidjs version 8.11.0. 
    The code should be formatted as a valid JSON string with new lines replaced by '\n'.

    Example:
    {example_code}

    Now, the user will provide the business logic of a complete folder along with its associated files. Your task is to generate accurate and
    executable code for a Mermaid class diagram in JSON format, with 'mermaid_class_diagram_code' as the key.

   Take a deep breath and think step by step to solve this task.

    User: {input}
    Mermaid_Code:
    {format_instructions}'''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","example_code"],partial_variables={"format_instructions":format_instructions}, template=template),
        verbose=True,
    )
    
    mermaid_diagram= llm_chain.predict(input=business_logic,example_code=example_code)
    result=parser.parse(mermaid_diagram)
    return result['mermaid_class_diagram_code']
    
class HigherLevelMermaidDiagram(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        folder_id = request.data.get('id') 
        folder = FolderUpload.objects.get(folderId=folder_id)
        existing_logic = HighLevel.objects.filter(user=request.user,folder_id=folder_id).first()

        if not existing_logic.classDiagram:
            mermaid_diagram=higher_level_mermaid_diagram(existing_logic.logic)
            data = {
                'logic':existing_logic.logic,
                'user':request.user,
                'folder_id':folder_id,
                'classDiagram':mermaid_diagram,
                'flowChart':existing_logic.flowChart
            }
            serializer = HighLevelSerializer(existing_logic,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            serializer = HighLevelSerializer(existing_logic)
            return Response(serializer.data, status=201)
        
    def put(self, request):
        folder_id = request.data.get('id') 
        folder = FolderUpload.objects.get(folderId=folder_id)
        existing_logic = HighLevel.objects.filter(user=request.user,folder_id=folder_id).first()


        mermaid_diagram=higher_level_mermaid_diagram(existing_logic.logic)
        data = {
            'logic':existing_logic.logic,
            'user':request.user,
            'folder_id':folder_id,
            'classDiagram':mermaid_diagram,
            'flowChart':existing_logic.flowChart
        }
        serializer = HighLevelSerializer(existing_logic,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
         
# Higher Level Mermaid Flowchart
def higher_level_mermaid_flowchart(business_logic):
    
    flowchart_schema = ResponseSchema(name='mermaid_flowchart_code', description='This schema represents the Mermaid flowchart code, designed to generate properly linked nodes that can be rendered by MermaidJS version 8.11.0. The code must be formatted as a valid JSON string, with newline characters replaced by "\\n". All nodes within the code should contain strings to ensure compatibility and avoid issues with special characters.')
    flowchart_description_schema = ResponseSchema(name='flowchart_code_description', description='This schema provides a description of the flowchart code generated by MermaidJS. It includes details about the structure and relationships of the nodes within the flowchart, as well as any additional information relevant to understanding the flowchart.')

    response_schema = (flowchart_schema,flowchart_description_schema)
    parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = parser.get_format_instructions()
    
    example_code=rpg_example3
    
    template='''
    Convert Business Logic to Mermaid Flow chart Diagram of a codebase.
    I want to generate code for Mermaid Flow chart diagram using business logic of a codebase and Remember this mermaid class diagram code is used by
    developers to visualize the codebase's code logic. Also give code in correct syntax so that it can be rendered by mermaidjs 8.11.0 . Make sure the
    blocks are properly linked . Here is also an example how to generate mermaid class diagram using the business logic. and remember also don't give
    any inital word and sentence like here is mermaid flow chart diagram of this business logic.Mermaid flow chart diagram that visually represents 
    this logic.The Mermaid flow chart diagram also should visually represent the flow and sequence of the business logic,including key decision points
    and data dependencies. Ensure that the resulting diagram is comprehensive and self-explanatory. 
    
    Remember this Mermaid Flowchart diagram serves the purpose of visualizing the interplay of business logic within a codebase, showcasing how 
    different files interact with one another. If certain files do not interact, we should still generate Mermaid flowchart diagrams for them.

    In accordance with this, please generate Mermaid code that encapsulates the business logic of an entire codebase.
    Follow these steps:
        1. Review the provided business logic.
        2. Identify key components, decisions, and flow control in the logic.
        3. Create a Mermaid flow chart diagram that illustrates the flow of logic, including decisions, loops, and data flow.
        4. Ensure that the files , databases and other UI elements which might be present are properly shown.
        5. Ensure the Mermaid flow chartdiagram is clear, well-structured, and accurately represents the business logic.
        
    Example:
    {example_code}
    
    Now the User will provide business logic,generate correct and running code for mermaid Flowchart diagram as shown in above example without any 
    initial text in a JSON format with "mermaid_flowchart_code" as the key and make sure that the blocks areproperly linked in the code.
    
    Take a deep breath and think step by step to solve this task.
    
    User: {input}
    Mermaid_Flowchart_Code:
    {format_instructions}'''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","example_code"],partial_variables={"format_instructions":format_instructions}, template=template),
        verbose=True,
    )
    
    mermaid_flowchart= llm_chain.predict(input=business_logic,example_code=example_code)
    result=parser.parse(mermaid_flowchart)
    return result['mermaid_flowchart_code']

class HigherLevelMermaidFlowchart(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        folder_id = request.data.get('id') 
        folder = FolderUpload.objects.get(folderId=folder_id)
        existing_logic = HighLevel.objects.filter(user=request.user,folder_id=folder_id).first()
        
        if not existing_logic.flowChart:
            mermaid_flowchart=higher_level_mermaid_flowchart(existing_logic.logic)
            data = {
                'logic':existing_logic.logic,
                'user':request.user,
                'folder_id':folder_id,
                'classDiagram':existing_logic.classDiagram,
                'flowChart':mermaid_flowchart
            }
            serializer = HighLevelSerializer(existing_logic,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            serializer = HighLevelSerializer(existing_logic)
            return Response(serializer.data, status=201)
        
    def put(self, request):
        folder_id = request.data.get('id') 
        folder = FolderUpload.objects.get(folderId=folder_id)
        existing_logic = HighLevel.objects.filter(user=request.user,folder_id=folder_id).first()
        
        
        mermaid_flowchart=higher_level_mermaid_flowchart(existing_logic.logic)
        data = {
            'logic':existing_logic.logic,
            'user':request.user,
            'folder_id':folder_id,
            'classDiagram':existing_logic.classDiagram,
            'flowChart':mermaid_flowchart
        }
        serializer = HighLevelSerializer(existing_logic,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
    
        
    def file_mermaid_flowchart(file_path):
        with open(file_path, 'rb') as file:
            code = file.read() 
        
        source=""
        destination=""
        logic=code_to_business_logic(code,source)
        mermaid_flowchart = business_logic_to_mermaid_flowchart(logic,source,destination)
        return mermaid_flowchart
        
    def combine_mermaid_flowchart(folder_name,
                            folder_structure,
                            previous_mermaid_flowchart,
                            current_directory_name,
                            current_directory_mermaid_flowchart):
        
        
        flowchart_schema = ResponseSchema(name='mermaid_flowchart_code',description='This is the mermaid flowchart code with properly linked nodes which can be rendered by mermaidjs 8.11.0. ,converted to a correct json string with new line replaced with \\n. Also all the nodes should contain strings so that any special characters do not cause problems')
        flowchart_description_schema = ResponseSchema(name='flowchart_code_description',description='This is the description of the flowchart code generated')

        response_schema = (flowchart_schema,flowchart_description_schema)
        parser = StructuredOutputParser.from_response_schemas(response_schema)
        format_instructions = parser.get_format_instructions()

        
        template='''
        I want to generate the complete Mermaid Diagram for the folder named '{folder_name}'. The folder structure of this folder is '{folder_structure}'.
        To achieve this, I will consolidate the Mermaid Diagram from each directory within it one by one. Specifically, I will merge the Mermaid Diagram
        from directories some within the folder structure with the current directory's Mermaid Diagram named 
        '{current_directory_name}'. This process will result in the combined Mermaid Diagram up to the specified directory and the Mermaid Diagram of 
        the current directory.and the remember in future anyone can convert this mermaid diagram code to business logic easily.Also give code in correct
        syntax so that it can be rendered by mermaidjs 8.11.0 . Make sure the blocks are properly linked .Mermaid flow chart diagram that visually
        represents this logic.Now give me combined Mermaid Flowchart Code using Previous Memaid Flowchart and Current Directory Mermaid Flowchart given below:

        Previous Mermaid Flowchart:
        
        {previous_mermaid_flowchart}
        
        Current Directory Mermaid Flowchart: 
        
        {current_directory_mermaid_flowchart}

        {format_instructions}
        '''

        llm_chain = LLMChain(
            llm = ChatAnthropic(temperature= 0.8,model = "claude-2.0",max_tokens_to_sample=100000),
            prompt=PromptTemplate(input_variables=["folder_name","folder_structure","previous_mermaid_flowchart",
                                                "current_directory_name","current_directory_mermaid_flowchart"],partial_variables={"format_instructions":format_instructions}, template=template),
            verbose=True,
        )
        mermaid_flowchart= llm_chain.predict(folder_name=folder_name,
                                folder_structure=folder_structure,
                                previous_mermaid_flowchart=previous_mermaid_flowchart,
                                current_directory_name=current_directory_name,
                                current_directory_mermaid_flowchart=current_directory_mermaid_flowchart)
        return f"{mermaid_flowchart}"
                
    def process_folder_mermaid_flowchart(self,folder_path):
        mermaid_flowchart=""
        folder_name=os.path.basename(folder_path)
        folder_structure=os.listdir(folder_path)
        src_path = os.path.join(folder_path, "src")

        if os.path.exists(src_path) and os.path.isdir(src_path):
            for item in os.listdir(src_path): 
                
                if item in (".DS_Store", ".gitignore","_pycache_","README.md","pom.xml",".idea",".mvn","mvnw.cmd","HELP.md","target","data","Data"):
                    continue
                item_path = os.path.join(src_path, item) 
                if os.path.isdir(item_path):  
                    Mermaid_Flowchart = self.process_folder_mermaid_flowchart(item_path) 
                else:
                    Mermaid_Flowchart = self.file_mermaid_flowchart(item_path)
                
                mermaid_flowchart= self.combine_mermaid_flowchart(folder_name,folder_structure,mermaid_flowchart,
                                                        item,Mermaid_Flowchart)
        else:
            for item in os.listdir(folder_path): 
                
                if item in (".DS_Store", ".gitignore","_pycache_","README.md","pom.xml",".idea",".mvn","mvnw.cmd","HELP.md","target","data","Data"):
                    continue
                item_path = os.path.join(folder_path, item) 
                if os.path.isdir(item_path):  
                    Mermaid_Flowchart = self.process_folder_mermaid_flowchart(item_path) 
                else:
                    Mermaid_Flowchart = self.file_mermaid_flowchart(item_path)   
                
                mermaid_flowchart= self.combine_mermaid_flowchart(folder_name,folder_structure,mermaid_flowchart,
                                                        item,Mermaid_Flowchart)
        
        return mermaid_flowchart



# Pratice

# num_tokens_from_string(logic, "cl100k_base")

def process_folder_business_logicP(parent_folder_id):    
    
    try:
        folder = FolderUpload.objects.get(folderId=parent_folder_id)
        folder_name = folder.foldername
        logic=""
        folder_business_logic_dict = {'HS0095.txt': ' Here is the extracted business logic from the provided RPG code:\n\nThe code contains several procedures:\n\n1. toUppercase:\n   - Accepts a string parameter\n   - Calls the built-in %xlate function to translate the string to uppercase\n   - Returns the uppercase string\n\nThis implements the logic to convert a string to uppercase.\n\n2. toLowercase:\n   - Accepts a string parameter\n   - Calls the built-in %xlate function to translate the string to lowercase \n   - Returns the lowercase string\n\nThis implements the logic to convert a string to lowercase.\n\n3. allocSpace:\n   - Accepts a pointer and a byte size \n   - Checks if pointer is null\n     - If null, allocates new memory of given size and assigns to pointer\n   - If not null, reallocates memory of given size to pointer\n\nThis implements the logic to dynamically allocate and reallocate memory for a pointer variable.\n\n4. deallocSpace:\n   - Accepts a pointer\n   - Checks if pointer is not null\n     - If not null, deallocates the memory for the pointer\n\nThis implements the logic to free dynamically allocated memory for a pointer variable.\n\nIn summary, these procedures provide string case conversion, dynamic memory allocation, and deallocation capabilities that can be utilized in an RPG application.\n\nThe code interacts with memory and strings but does not seem to access any files or UI. It is a self-contained RPG code module focused on string and memory handling functions.','HS0097.txt': " Here is the business logic extracted from the provided RPG code:\n\nThe code appears to be for a user interface that allows selecting and displaying printers/output queues. The key steps are:\n\n1. Determine the user ID and translate to uppercase\n2. Lookup the user's organization information like region, office code etc from a file\n3. Based on input parameter 'Display', load printers into a subfile:\n   - If 'REG' - Show all printers in region\n     - First load printer for current office\n     - Load other offices in region\n     - Load other offices in country \n   - If 'NDL' - Show all printers in office\n     - First load printer for current office  \n     - Load other offices in office\n   - If 'BST' - Show only current office printer\n4. The printer records are read from a file and filtered based on criteria\n5. The selected printer is returned in output field 'Outq'\n\nFiles Used:\n- Adusrf - User Details file\n- Cdorgl1 - Organization Details file \n- Hioutqpf - Printer Details file\n- Hs0097s1 - Printer Subfile\n\nThe code displays the subfile, handles paging and allows selecting a printer. It is focused on retrieving the printer records and presenting them in a subfile for selection. The key business logic is filtering and loading the printer records based on the region/office scope selected."}
        folder_structure=get_folder_structure(parent_folder_id)
        
        files_name=[]
        
        files = FileUpload.objects.filter(parentFolder=folder)
        # for file in files:
        #     try:
        #         existing_logic = Logic.objects.get(file=file)
        #         file_logic = existing_logic.logic
        #     except:
        #         file_logic = file_business_logic(file.file)
        #     folder_business_logic_dict[file.filename] = file_logic
        
        subfolders = FolderUpload.objects.filter(parentFolder=folder)
        for subfolder in subfolders:
            subfolder_logic = process_folder_business_logic(subfolder.folderId)
            folder_business_logic_dict[subfolder.foldername] = subfolder_logic
            
        try:
            flag=0
            # If folder_business_logic_dict token limit is greater than 100000 token
            for file in folder_business_logic_dict:
                if(flag==0):
                    flag=flag+1
                    files_name.append(file)
                    logic=folder_business_logic_dict[file]
                else:
                    files_name.append(file)
                    logic = combine_business_logic(folder_name,folder_structure,files_name,logic,file,folder_business_logic_dict[file])
            return logic
            
            
            # If folder_business_logic_dict is less than 100000
            # logic = higher_level_business_logic(folder_business_logic_dict,folder_name)
            # return logic   
            
        except:
            return "Error"
        
    except FolderUpload.DoesNotExist:
        logging.error(f"Folder with ID {parent_folder_id} not found.")
        return ""
    except Exception as e:
        logging.error(f"An error occurred while processing folder {parent_folder_id}: {str(e)}")
        return ""

class HigherLevelBusinessLogicP(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        folder_id = request.data.get('id') 
        business_logic = process_folder_business_logicP(folder_id)
        return Response({"response":business_logic}, status=200)
 

















# Higher Level For Specific Files

# HS023 Files Higher Level Business Logic

business_023={
"HS023V":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program is named HS023V and titled \"SDPS Customer Master Default Values from SDE\". It appears to be called from program HS0230.\n\nThe purpose of this program is to retrieve default values for customer master records from an interface file and assign them to output parameters.\n\nIt does the following:\n\n1. Opens the interface file HSKUILF1 for reading. This is likely an extract file containing customer default values.\n\n2. Reads records from HSKUILF1 sequentially using a key of KEYKUD. \n\n3. Checks if the interface record has KUI000 = 'SDE', indicating it is a record from SDE (likely another system).\n\n4. If it is a record from SDE, copies values from the interface file to the output parameters:\n\n    - KUI180_SDE = KUI180 (AXA Customer Group)\n    - KUI190_SDE = KUI190 (AXA Tax Group)\n\n5. Continues reading records until end of file is reached.\n\nSo in summary, this program retrieves default customer group and tax group values from an SDE extract file and assigns them to output parameters that are likely used in another program that maintains customer master records.\n\nThe program interacts with two files:\n\n- HSKUILF1 - Input extract file containing customer default values \n- FKUDSTAM - Likely customer master file, not directly used here but based on program name\n\nNo database or UI interaction is indicated in this code.",
"HS023S":"Here is the extracted business logic from the provided RPG code:\n\nThis code appears to be for customer management in an ordering system. The main functions are:\n\n1. Display and maintain customer contacts (subfile maintenance)\n\n- Allow adding, changing and deleting customer contacts \n- Contacts have name, email, date fields\n- Validate required fields on add/change\n- Show message if no contacts exist\n\n2. Link customers to operating sites\n\n- Allow selecting operating site (dropdown?) \n- Validate site is valid using site master file\n- Save site linkage in customer master record\n\n3. Save customer record \n\n- Validate contact and site data  \n- Save or update customer record with key fields, site, order type and date\n- Delete customer record if unlinking site\n\n4. Clean up orphaned contacts\n\n- Delete contacts not linked to customer records\n\nThe code interacts with these files:\n\n- SPOCUSF - Customer master file\n- SPOCUAF - Customer contact file\n- HSBTSPF - Site master file \n- Plus work files\n\nThe UI is a 5250 green screen using subfile for contact maintenance.\n\nThe core logic revolves around maintaining contacts, validating data, and linking records between the customer, contact and site files. Let me know if any part needs further explanation!",
"HS023L":"Here is the extracted business logic from the provided RPG code:\n\nThis code appears to be for maintaining customer master data related to country codes.\n\nIt contains the following key steps:\n\n1. Initialize data structures and files:\n\n- INFDS: Input data structure\n- HS023LS1: Output file in SFL format \n\n2. Get current user ID into ALGUSR field\n\n3. Read customer master records (KUDSTAR) by key (KUI020/KUI030):\n\n- KUI020/KUI030: Key fields for customer number\n\n4. Check if country code (KUD070) matches selection criteria (SEL):\n\n- KUD070: Country code field\n- SEL: Selection criteria variable \n\n5. If country code matches:\n\n- Write customer record (KUDSTAR) to output file HS023LS1\n- Increment record counter ZL1\n\n6. End of customer master read loop\n\n7. Read output file HS023LS1 and update country codes (KUD070):\n\n- Update customer master (KUDSTAR) with new country code\n\nSo in summary, this program:\n- Reads customer master records \n- Selects records matching given country code\n- Writes those records to an output file\n- Then reads back and updates the country codes\n\nIt interacts with the following files:\n- KUDSTAR - Customer master file\n- HSLAEPR - Country code validation file\n- HS023LS1 - Temporary output file\n\nThe output file HS023LS1 is in SFL (save file) format, indicating temporary storage of selected records.\n\nLet me know if you need any clarification or have additional questions!",
"HS023I":"Here is the extracted business logic from the provided RPG code:\n\nPurpose:\n- This program retrieves the number of users (KUI) associated with each customer address. \n- It also checks if the customer name should be locked based on certain criteria.\n\nParameters:\n- KUI020 - Input - A key field to identify the customer address\n- KUI030 - Input - A key field to identify the customer address  \n- ANZ_KUI - Output - A 3-byte integer field containing the number of KUI records for the customer address\n- LOC_NAME - Output - A 1-byte indicator set to 'J' if the customer name should be locked, 'N' otherwise\n\nFiles Used:\n- FKUDSTAM - DISK file - Customer master file (HDLZENTRAL library) \n- FHSKUILF1 - DISK file - User master file (HDLZENTRAL library)\n\nLogic:\n1. Initialize ANZ_KUI counter to zero\n2. Read FHSKUILF1 file by key KUI020/KUI030 to retrieve KUI records for the customer address\n   - For each KUI record found, increment ANZ_KUI counter\n3. Check if customer names should be locked\n   - Read DTAARA KUDNAMS - If it contains 'J', evaluate locking logic\n   - Chain customer master record using KUI020/KUI030 as key\n   - If country = 'D' (Germany) and ANZ_KUI > 1, set LOC_NAME = 'J' \n4. Return ANZ_KUI and LOC_NAME to calling program\n\nSummary:\n- This program retrieves the number of users for a customer address from the user master file. \n- It also sets an indicator if the customer name should be locked based on country and number of users.\n- The program interacts with the customer master file, user master file, and a DTAARA.",
"HS023H":"Here is the extracted business logic from the provided RPG code:\n\nThis program appears to be related to updating and maintaining customer master data.\n\nThe key steps are:\n\n1. Read customer master record (KUDSTAR file) \n\n2. Loop through address users for this customer (HSKUILR2 file)\n\n3. If the address user made the change, write a history record (HSKUDPR file) containing the address user details and the before image of the customer master record\n\n4. For dependent address users not making the change, set change indicator (KUI260) \n\n5. The history record contains all fields from the customer master record, address user details, change details like date/time, user and change reason.\n\n6. The main files used are:\n\n- KUDSTAR - Customer master file\n- HSKUILR2 - Address user file \n- HSKUDPR - Customer history file\n\n7. Input parameters:\n- Change date/user\n- Old and new customer number\n- Change reason code  \n\n8. The program seems to be called from other programs like HS0510, HS0550 etc. to maintain history when customer records are changed.\n\n9. There is also some logic to handle AX customers differently, avoiding setting of KUI260.\n\nIn summary, this program maintains history of changes to customer master records by address users and propagates change notifications to dependent address users. The key data files used are customer master, address user and customer history files.",
"HS0239_2":"Here is the extracted business logic from the provided RPG code:\n\nThe code appears to be for maintaining bank account information for customers/vendors.\n\nIt does the following:\n\n1. Reads payment schedule data (CSCOHF) for active records in the payment terms file (CSPASL2).\n\n2. For each active payment terms record:\n\n- Gets the country code (COH_LAND) and partner ID (PAS_B_DEBI)\n- Checks if partner is a subsidiary (BTS050 starts with 'T')  \n- Calls a subroutine to validate and enrich bank details (account number, IBAN, BIC etc)\n- If bank details are valid:\n  - Updates payment terms file (CSPASL2) with enriched bank details \n  - Writes a bank account record (HSBNKL1) for the partner\n    - For non-German partners, adds new bank accounts\n    - For German partners, deletes existing bank accounts first, then writes new records\n\n3. The subroutine for bank validation (SR_BANK):\n\n- Tries to determine country code from IBAN if available\n- Calls external program ADW0010 to validate and enrich bank details\n- Populates output parameters with validated bank data\n\nSo in summary, this program:\n\n- Syncs bank account info from payment terms to bank account file\n- Validates and enriches bank account details \n- Handles logic differently for German vs non-German partners\n\nIt interacts with these files:\n\n- CSPASL2 - Payment terms file\n- CSCOHF - Header file for payment terms\n- HSBNKL1 - Bank account file\n- HSKUIPF - Partner file\n- KUDSTAM - Partner master file\n\nAnd calls external program ADW0010 for bank validation.\n\nThe program runs daily via a scheduled job to keep bank data in sync.",
"HS0239ALT":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program appears to be for customer search functionality, allowing users to search for customers based on criteria entered in multiple search fields.\n\nIt contains the following key procedures:\n\n1. Initialization:\n   - Retrieve user profile (ALGUSR) to check authorization \n   - Initialize work fields, search criteria fields, etc\n\n2. Build search criteria:\n   - Allow user to enter search values into 5 fields (FLD1-FLD5)\n   - Move search values into substring fields (SUBEG1-SUBEG5) for comparison\n\n3. Search customers:\n   - Read customer records (KUDSTLx files) \n   - For each customer record, compare search substrings to customer fields\n   - If substring matches a field, select that customer\n   - Search can be limited to only the user's own customers\n\n4. Display results:\n   - Selected customers are displayed in a subfile\n   - User can page through results\n   - User can select a customer record to retrieve details\n\n5. Retrieve customer details:\n   - When user selects a customer in the subfile, pass customer number to retrieve full details\n   - Lookup customer in customer master file (HSKUILF2)\n\n6. Sorting:\n   - Allow user to toggle sort order of results between alphabetical and numerical\n\n7. Special character handling:\n   - Convert umlaut characters to normal characters for comparison\n\nThe code interacts with the following files:\n- KUDSTLx - Customer subfiles\n- HSKUILF2 - Customer master file\n- HSBSTL1 - User profile file  \n\nIt uses a display file HS0239 for the screen I/O.",
"HS0239":"Here is the business logic extracted from the provided RPG code:\n\nOverall Functionality:\n- This RPG program allows maintaining bank details for a given customer. It provides functions to view, add, change and delete bank accounts.\n\nParameters:\n- DEBLIF (Input): Customer number \n- KZL (Input): Central key of customer's home location\n- KONTO (Input): Account number of customer's home location  \n- BEREICH (Input): Bank detail type (e.g. payments, loans etc.)\n- ANZ (Input): Number of bank details to maintain\n- ParmIban (I/O): IBAN number\n- ParmBic (I/O): BIC code \n- ParmBN (I/O): Bank name\n\nAdditional Inputs: \n- FIRMA: Company name\n- UMGEBUNG: Company code  \n\nProcessing:\n1. Validate input parameters\n\n2. If home partner, set indicator *IN80 to '1'\n\n3. Get central key KZLZEN and account number KontoZen for customer's home location\n\n4. Get description BERBEZ for input bank detail type BEREICH\n\n5. Repeat until F3 or F12 is pressed:\n   - Call SFL1LOE to clear detail screen\n   - Call SFL1LAD to load bank details into subfile\n   - Call SFL1ANZ to display number of records in subfile\n   - Case of user action:\n      - F3 or F12 pressed - exit loop\n      - F6 pressed - call SR06 to add new bank detail\n      - Selection from subfile - call SFL1AUSW to process user action\n\n6. Set indicator *INLR to '1' to prevent re-display of screen\n\nSubroutines:\n\nSFL1LOE: Clear detail screen\nSFL1LAD: Read bank details from file HSBNKF into subfile HS0239S1 based on selection criteria\nSFL1ANZ: Count and display number of records in subfile\nSFL1AUSW: Process user action on subfile record\n   - F1 - Call SR_BANK to validate IBAN\n   - F2 - Allow change of bank detail \n         - Call PLAUSISR to validate input  \n         - If valid, update file HSBNKR\n         - If bank detail type changed, update sort order in HSBNKL1\n   - F4 - Allow delete of bank detail\n         - If confirmed, delete record from HSBNKR\nSR06: Allow user to add new bank detail\n   - Initialize fields  \n   - Loop until F12 pressed to exit without add:\n     - Display add screen HS023902\n     - Call PLAUSISR to validate input\n     - If valid:\n       - Determine next sort number\n       - Write new record to HSBNKR\nPLAUSISR: Validate input fields for add/change\n   - Check required fields  \n   - Validate IBAN \n   - Check for duplicate bank detail\n   - Validate country code\n   - Validate bank detail type\nSR04: Provide F4 search help\nSR_BANK: Call program ADW0010 to validate IBAN\n\nFiles Used:\nHSBNKF: File containing customer bank details\nHSBNKR/HSBNKL1: Files updated when adding/changing bank details\n\nIn summary, this RPG program provides maintenance of bank details for a customer by allowing users to view, add, change and delete records through an interactive subfile. It validates all user input and updates associated files.",
"HS0238C":"Here is the business logic extracted from the provided RPG code:\n\nThis code appears to be a main program that calls another program HS0238 to perform some functionality related to customers.\n\nThe key points are:\n\n- Purpose: Main program that calls HS0238 to search/check duplicate customer master records\n\n- Modules Called: \n  - HS0238 (with 4 parameters passed):\n    - Param 1: Blank space \n    - Param 2: Blank space\n    - Param 3: 'ZGANZ' (seems to indicate full/complete search)\n    - Param 4: Blank space\n\n- Functionality:\n  - The main program doesn't contain much logic, it simply calls HS0238 while passing some parameters\n  - The purpose seems to be searching and checking for duplicate customer master records\n  - HS0238 likely contains the core logic for searching and deduplicating \n  - The parameters passed indicate some kind of full or complete search is desired\n\n- Other Details:\n  - This program is called HS0238C\n  - It's part of an application called SDPS-ZENTRAL\n  - The application area is customers\n  - Created by P.Wehn on 06.12.2004\n\nIn summary, this main RPG program calls another program HS0238 to perform customer master search and deduplication functions by passing it some parameters. The core logic resides within HS0238 which gets called from this main program.",
"HS0238":"Here is the business logic extracted from the provided RPG code:\n\n1. Program Purpose:\n- This program is for customer master search and duplicate check. It allows searching for customers by various criteria like name, address, postcode etc. and shows search results in a subfile for selection.\n\n2. Input Parameters:\n- KZL (char 3): Branch number \n- KDNR (char 6): Customer number\n- KDMC (char 5): Program to call for details\n- RET (char 3): Return code \n\n3. Global Data Structures:\n- MATCHID (char 6): Matchcode value\n- DDUKPLE (char 5): Search criteria - postcode range\n- §RETURN (char 3): Return code\n\n4. Main Procedures:\n\n4.1 Initial Setup:\n- Initialize variables, subfile etc.\n- Read user profile for allowed branches\n- Set initial sort order and search criteria\n\n4.2 Search:\n- Based on input criteria, search by postcode range or matchcode\n- For postcode: Read postcode file, find matching addresses\n- For matchcode: Find matching customer numbers \n\n4.3 Selection Display:\n- Show results in subfile\n- Allow changing sort order and search criteria\n- On selection, return customer number and branch \n\n4.4 Subroutines:\n\n- SFLLOE: Clear subfile\n- PLZ: Build subfile by postcode\n- MATCH_KUD: Build subfile by matchcode on customer number\n- MATCH_KUI: Build subfile by matchcode on alternative customer number\n- FUELS1: Fill subfile with address details\n- SR16: Change sort order\n- TRIMBL: Remove blanks from search fields\n\n5. Called Programs/Files:\n- KUDSTAM: Customer master file\n- KUDSTLFF: Postcode file\n- HSKUILF1: Alternative customer number file\n- HSBTSLF1: User profile file\n\nSo in summary, this is an interactive search program for the customer master file allowing flexible search criteria and subfile display of results.",
"HS0237":"Here is the business logic extracted from the provided RPG code:\n\nThe code is for a customer master duplicate check program that gets called when creating a new customer in the system.\n\nIt does the following:\n\n1. Clears the work file C__RD1A which will hold the duplicate check results.\n\n2. Checks if this is called from program ESW230 for duplicate check during address conflict handling. If yes, skip postal check.\n\n3. Performs postal check validation on the address by calling program L00764. Checks for errors.\n\n4. If no errors, calls program L00764 again to find duplicate addresses. \n\n5. If duplicates found, displays them in a subfile for the user to select the correct address.\n\n6. Allows user to select one of the duplicate addresses.\n\n7. Saves the selected customer number and sets no error if user selected an address.\n\n8. The calling program will use the selected customer number for creating the new customer record.\n\nThe subroutines do the following:\n\n- SFL1LOE: Clears the subfile\n- SFL1LAD: Loads duplicate addresses into subfile\n- SFL1ANZ: Displays number of records in subfile\n- SFL1AUSW: Gets user selected customer number\n\nFiles used:\n\n- C__RD1A: Work file for duplicate check\n- KUDSTAM: Customer master file\n- HSKUILF1: Unknown\n\nPrograms called: \n\n- L00764: Called for postal check and finding duplicates\n\nThe code interacts with the user by displaying a subfile for address selection. It reads/writes to files to load and save data.",
"HS0236":"Here is the extracted business logic from the provided RPG code:\n\nThe code appears to be processing customer and vehicle data from multiple input files and updating several output files.\n\nMain steps:\n\n1. Read dealer data from FISTAM file and update dealer master file HSDEAPF\n\n2. Read customer data from KUDSTAR file and update customer master file HSCUSPF\n\n3. Read payment guarantee data from KUDSTAR file and update payment guarantee file HSGOPPF\n\n4. Read contact person data from HSKUAPF file and update contact person file HSCONPF\n\n5. Read vehicle data from FARSTAR and HSKUIPF files and update vehicle master file HSVEHPF\n\n6. The code handles mapping data between input and output files, applying business rules, validating values, deriving new values etc. \n\nKey files used:\n\n- Input\n    - FISTAM: Dealer master data\n    - KUDSTAR: Customer master data \n    - FARSTAR: Vehicle master data\n    - HSKUIPF: Customer-Vehicle linkage info\n    - HSKUAPF: Contact person data\n\n- Output\n    - HSDEAPF: Dealer master file\n    - HSCUSPF: Customer master file\n    - HSGOPPF: Payment guarantee file\n    - HSCONPF: Contact person file \n    - HSVEHPF: Vehicle master file\n\nThe code interacts with these files, reads input data, applies various transformations and business logic, and updates the output master files.\n\nLet me know if you need any clarification or have additional questions!",
"HS0235C":"Here is the extracted business logic from the provided RPG code:\n\nOverview:\n- This RPG program appears to be handling data transfers and file processing related to vehicle/customer information for Scania Deutschland.\n\nMain logic:\n- Declares a file HS0235D with record format HS0235W0 to read input data.\n- Retrieves a 3-character variable &KZL from a data area UMGEBUNG.\n- Calls another program HS0235.\n- Clears output files HSDEAPF, HSCUSPF, HSVEHPF, HSGOPPF, HSCONPF.\n- Reads next record from input file HS0235D into format HS0235W0.\n- Checks if &KZL is not equal to 'SDE'.\n  - If true:\n    - Copies file PIPPMST to temporary file QTEMP/PIPPMST with add option.\n    - Monitors for errors.\n- Calls program HS0236. \n- Deletes temporary file QTEMP/PIPPMST.\n- Monitors for errors.\n- Returns.\n\nSummary:\n- This program seems to process vehicle/customer data from an input file. \n- It conditionally copies a master file PIPPMST to a temp file based on a code value.\n- It calls other programs before and after this copy operation.\n- The temp file copy of PIPPMST is deleted after processing.\n\nRelated files:\n- Input file HS0235D (possibly vehicle/customer data) \n- Output files HSDEAPF, HSCUSPF, HSVEHPF, HSGOPPF, HSCONPF (likely different entity outputs)\n- Master file PIPPMST (possibly product/pricing data)\n- Temporary file QTEMP/PIPPMST\n\nNo database interactions are indicated in this code.",
"HS0235":"Here is the extracted business logic from the provided RPG code:\n\n**Overview:**\nThe code implements functionality to maintain payment guarantees for customers in the system. Key aspects include:\n\n- Displaying and editing payment guarantee details for customers\n- Adding new payment guarantees for customers\n- Restrictions on editing and adding payment guarantees based on user rights, customer status etc.  \n- Writing change flags and history records when payment guarantee details are modified\n\n**Procedures/Functions:**\n\n1. `CheckAuthority`: \n   - Purpose: Check if user has authority to edit/add payment guarantees. If not, exit program.\n   - Parameters:  \n     - `§PGMNAM`: Program name \n     - `§PGMTXT`: Program title\n     - `§PGMOPT`: Program option\n   - Logic:\n     - Call `CheckAuthority` API to validate authority\n     - If no authority, exit program\n\n2. `SR06N`: \n   - Purpose: Add new payment guarantee for a customer\n   - Parameters: \n     - `NEUKUD`: Customer number for new guarantee\n     - `NEUMAT`: Material number  \n     - `NEUNAM`: Name\n     - `NEUZAN`: Payment guarantee amount  \n     - `NEUDAT`: Valid to date\n     - `NEUUST`: VAT ID\n     - `NEULKZ`: VAT ID status\n     - `NEUOK`: VAT ID OK\n   - Logic:\n     - Validate if customer can have payment guarantee added\n       - Not an Axapta participant, not blocked, not cash payer\n       - Not a duplicate customer ID\n     - Default new payment guarantee values\n     - Allow editing based on user authority\n     - Validate maximum guarantee amount \n     - Write change flags and history records\n     - Add new payment guarantee to customer\n\n3. `SRHISF`:\n   - Purpose: Populate history record with current customer and payment guarantee header details\n   - Logic: \n     - Move current customer/payment guarantee header fields to history record format\n\n4. `SRHISS`:\n   - Purpose: Write history record to file\n   - Logic:\n     - Open history file\n     - Write history record\n     - Close history file\n\n5. `AENHIS`:\n   - Purpose: Write full record change history on update\n   - Logic:  \n     - Get current date and user\n     - Write to last change date, user in history format\n\n6. `SRAKT`:\n   - Purpose: Get current date and time\n   - Logic:\n     - Move current date to `AKTDAT` \n     - Move current time to `AKTTIM`\n     \n7. `WriteKui260SR`:\n   - Purpose: Write change flag KUI260\n   - Logic:\n     - Based on user type (Axapta or free) and customer type (Axapta or free), determine if change flag should be written and for which customer IDs.\n\n**Key Files**\n\n- `KUDSTAM`: Customer master file\n- `HSKUIPF`: Customer master index file\n- `HSKUDPF`: Customer history file\n\nThe code handles loading and interacting with these files to retrieve, update and store customer and payment guarantee details.\n\n**User Interface**\n\nThere appears to be user interface screens defined that allow:\n\n- Display and editing of existing payment guarantees \n- Adding new payment guarantees\n- Searching/filtering payment guarantees\n\nThese include:\n\n- `HS0235W6`: Add/edit payment guarantee screen\n- `HS0235C1`: Payment guarantee subfile 1\n- `HS0235C2`: Payment guarantee subfile 2 \n- `HS0235W9`: Search screen\n\nThe RPG code handles loading these screens, responding to user actions on the screens, and updating the display.\n\nLet me know if you need any clarification or have additional questions!",
"HS0234":"Here is the business logic extracted from the provided RPG code:\n\nThe code is for maintaining customer master data - specifically contact persons. It allows adding, changing, deleting, and displaying contact person records.\n\nMain functions:\n\n1. Display contact persons subfile (SRSFL1)\n\n- Reads contact person records (KUA file) and displays them in a subfile\n- Handles subfile paging\n- Checks if there are records to display\n\n2. Add new contact person (SR06)  \n\n- Validates required fields \n- Gets next free internal number (LFDNR)\n- Writes new record to KUA file\n- Saves entry date, time and user\n\n3. Change contact person (SR102)\n\n- Allows changing all fields\n- Validates required Name field  \n- Writes changed record to KUA file\n- Saves changed date, time and user\n\n4. Delete contact person (SR104) \n\n- Deletes record from KUA file after confirmation \n\n5. Display contact person details (SR105)\n\n- Shows all fields of a selected record in display format\n\nAdditional functions:\n\n- SR04: Field help - retrieves field description\n- SRFAV: Maintain position default values\n\nThe code interacts with these files:\n\n- KUDSTAM: Customer master file\n- HSKUAPF: Contact person file (physical file) \n- HSKUAPR: Contact person records (logical file)\n- HSFAVPF: Position default values file\n\nIt uses a display file HS0234D and subfile HS0234S1.\n\nIn summary, the business logic covers maintenance transactions for customer contact persons, validating input, saving to database files, and interacting with the user through displays and subfiles. The RPG code implements this logic through file I/O, calculations, branching, and modularity using subroutines.",
"HS0232":"Here is the extracted business logic from the provided RPG code:\n\nThis code appears to be for a customer management system for an automotive company.\n\nThe main purpose is to generate an Excel report of large customers.\n\nKey aspects:\n\n- It checks if indicator 12 on the calling screen is 1. If yes, it exits the program. This allows the user to cancel report generation.\n\n- It retrieves the transfer command string from a data area called TTOGRK into a variable &TTOGRX. \n\n- It checks if &TTOGRX is blank. If yes, it exits the program. This prevents running the report if the command string is not set.\n\n- It sends a message that the transfer command to start the report is: &TTOGRX\n\n- It calls the transfer command using STRPCCMD, passing &TTOGRX. This runs the actual report generation process.\n\n- It sends a completion message.\n\nSo in summary, this program provides a simple interface to trigger the execution of a larger reporting process by passing a transfer command string.\n\nIt validates input, retrieves the needed command, executes the command, and provides status messages.\n\nThe key external dependencies appear to be:\n\n- TTOGRK data area - contains the transfer command string\n\n- Transfer command program - generates the Excel report \n\n- Calling screen - allows user to cancel processing via indicator 12\n\nLet me know if you need any clarification or have additional questions!",
"HS0231":"Here is the extracted business logic from the provided RPG code:\n\nOverall functionality:\n- This RPG program prints a customer master list filtered by various selection criteria. It allows selecting customers by customer number, zip code, discount codes, number of vehicles, payment guarantee flag, print suppression flag, credit rating, and last sales date.\n\nMain processing steps:\n\n1. Initialize variables, tables, and files. Define data structures, tables, arrays, variables needed. Open files for input and output.\n\n2. Validate input parameters. Check for errors in input selection criteria values.\n\n3. Determine fiscal year code (FISJJJ) from company code (KURZEL). Read company master file (FISTAR) to get fiscal year.\n\n4. Get total sales amounts for fiscal year:\n   - Read customer sales file (HSBKULF1) and accumulate sales amounts for workshop (KUD22N) and counter (KUD23N). \n   - Get first and last sales month/year (UMSENDE).\n\n5. Read customer master file (KUDSTAR) and select customers meeting criteria:\n   - Check customer number range\n   - Check zip code range \n   - Check discount code ranges\n   - Check number of vehicles range\n   - Check payment guarantee flag\n   - Check print suppression flag\n   - Check credit rating\n   - Check last sales date after input criteria\n\n6. For selected customers:\n   - Write page header\n   - Write detail line with customer data\n   - Accumulate counters\n\n7. Print final page footer and totals.\n\n8. Close files.\n\nRelated files used:\n- FISTAM - Company master file\n- HSBTSLF1 - Company/Site file\n- HSBKULF1 - Customer sales file \n- KUDSTAR - Customer master file\n- HSKUIPF - Customer master by customer number\n- HSPSTLF2 - Customer price change file\n\nOutput files:\n- FHS0231P - Printer file\n\nInput fields:\n- Selection criteria fields (customer number, zip code, discount codes, etc.)\n\nRelevant output fields:\n- Customer data fields from KUDSTAR\n- Sales totals for fiscal year\n\nIn summary, this program generates a filtered customer list report by reading the customer master file and selecting customers based on several criteria provided as input. It also prints sales totals for the selected customers.",
"HS0230C1":"Here is the business logic extracted from the provided RPG code:\n\nThe code appears to be retrieving customer data from a temporary table called QTEMP/HS0230. \n\nIt takes in three input parameters:\n- &KDNR - A 6 character field, likely the customer number\n- &KZL - A 3 character field, possibly an indicator or key field\n- &RETURN - A 3 character return code\n\nIt then calls another program QTEMP/HS0230, passing the input parameters. Based on the name, this program likely retrieves the customer details from QTEMP.\n\nThe called program returns a value in &RETURN, which is then returned by this main program.\n\nSo in summary, the business logic is:\n\n1. This code is part of a customer maintenance application.\n\n2. It accepts a customer number and other identifier as input. \n\n3. It calls another program which retrieves customer details from a temporary table QTEMP/HS0230.\n\n4. The called program returns a status code which is checked.\n\n5. Any errors are handled appropriately. \n\n6. The customer data is presented back to the user or calling program.\n\nIn terms of files and interactions:\n\n- Input comes from parameters passed to the program\n\n- Customer data is retrieved from temporary table QTEMP/HS0230\n\n- Output is returned back to calling program via parameters\n\n- No specific UI or database interactions are coded here.\n\nPlease let me know if you need any clarification or have additional details to add! I'm happy to explain or expand on this breakdown of the business logic.",
"HS0230C":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program is designed to duplicate an existing program called HS0230 from the library list into the QTEMP library.\n\nThe key steps are:\n\n1. Delete the program QTEMP/HS0230 if it already exists. This avoids errors when trying to create a duplicate program with the same name.\n\n2. Create a duplicate of the program HS0230 from the library list into the QTEMP library. \n\n3. Monitor for any errors in the delete and duplicate operations.\n\nThe purpose of this program seems to be creating a temporary copy of the HS0230 program for testing or other purposes. \n\nSome details:\n\n- The original program being duplicated is HS0230\n- It exists somewhere in the library list \n- The duplicate will be created in library QTEMP\n- The duplicate will have the same name HS0230\n\nNo other files, databases or UI interactions are indicated in this code. It is a simple standalone RPG program to duplicate another RPG program into a temporary library.",
"HS0230ALT1":"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- The code implements functionality for maintaining customer master data. It allows viewing, adding, changing, deleting customers and viewing customer transaction history.\n\nKey Procedures:\n\n1. Customer Search/Selection (P018):\n- Allows searching for customers by various criteria like customer number, name, sales office etc. \n- Displays list of matching customers in a subfile.\n- Handles selection of a customer from the list for further processing.\n\n2. Add New Customer (P001): \n- Adds a new customer by initializing a new customer master record and individual customer data record.\n- Generates next free customer number, sets initial values.\n\n3. Change Existing Customer (P002):\n- Loads customer master and individual customer data records.\n- Allows changing customer details like name, sales office etc. \n- Handles updates to both records.\n\n4. Delete Existing Customer (P004):\n- Checks if customer can be deleted. \n- Deletes customer master and individual customer data records.\n\n5. Display Customer Details (P005):\n- Loads customer master and individual customer data records.\n- Displays customer details in screen fields.\n\n6. Change Home Country (P007): \n- Changes the home country (associated sales office) for a customer.\n- Handles updates to customer master and individual customer data.\n\n7. Maintain Customer History (SRHIS, SRHISS etc):\n- Displays historical changes to customer details.\n- Writes change entries to customer history file.\n\nRelated Files:\n- KUDSTAM - Customer Master File\n- HSKUIPF - Individual Customer Data File \n- HSKUILF2 - Work File\n- HSKUKPF - Customer Comments File\n- HSKUDPF - Customer History File\n- HSKBTSPF - Sales Offices File\n\nThe program handles all core customer maintenance processes like add, change, delete, display, search etc. It maintains customer data across multiple related files like master data, individual data, comments, history etc. The search functionality allows flexible customer selection using various criteria.",
"HS0230ALT":"Here is the business logic extracted from the provided RPG code:\n\n1. Customer Master File Maintenance\n\n- Add New Customer (P001)\n  - Prompts for customer data entry \n  - Validates required fields \n  - Generates next available customer number\n  - Writes new customer record to master file\n  - Writes new individual customer data record\n\n- Change Existing Customer (P002)\n  - Loads customer and individual data records\n  - Validates required fields\n  - Checks for price determination changes\n  - Updates customer and individual data records\n  - Writes change history record\n\n- Delete Existing Customer (P004)\n  - Validates customer is not linked to other records\n  - Deletes customer, individual data, and change history records\n\n- Display Customer (P005)\n  - Loads customer and individual data records\n  - Displays customer details\n  \n- Change Home Branch (P007)\n  - Loads customer and individual data records\n  - Changes home branch on records\n  - Updates related records\n\n2. Search and Select Customers (P018)\n\n- Search by various criteria\n  - Customer number\n  - Name\n  - Branch\n  - Sales rep code\n  - Matchcode\n- Select and display search results\n\n3. Customer Sales History (SRHIS)\n\n- Maintains and displays historical changes for each customer\n\n4. Customer Sales Analysis (UMSKUD) \n\n- Analyzes sales data by customer and branch\n- Displays sales summary info\n\n5. Validation and Error Handling\n\n- Validates required fields\n- Checks valid field contents \n- Displays error messages\n\n6. Files Used:\n\n- KUDSTAM - Customer Master File\n- HSKUILF2 - Individual Customer Data \n- HSKUIPF - Customer Sales Data\n- HSKUDPF - Customer Change History\n- HSKUKPF - Customer Comments\n\nThe key functionality covers customer maintenance, search and display, sales analysis, and history tracking. The code interacts with several physical files to store and retrieve customer data.",
"HS02309":"Here is the extracted business logic from the provided RPG code:\n\nOverall Purpose:\n- Update the payment term (Valuta) for existing customers in Axapta/Dynamics 365 Finance & Operations based on country.\n\nMain Processes:\n1. Select customers to change:\n   - Only active customers (KUD846 = 'A')\n   - Only customers with a single customer record (KUI260 = '1') \n   - Only customers with the old payment term value in KUD860 and KUI290\n   - Maximum 500 customers changed per program run\n\n2. Change payment term:\n   - Update KUD860 and KUI290 to the new payment term value based on country\n   - Germany (SDE): Change from 14 days (value '___2') to 8 days (value '__11')  \n   - Austria (SAT): Change from 14 days (value '1401') to 8 days (value '0801')\n\n3. Flag changed customers in KUI260 = '1' \n\n4. Write changed customers to tracking file HS02309F\n\n5. For Germany (SDE), call AXH030 to consolidate Retail-KUI records\n\n6. Send updated customer data to Axapta/D365FO using interface D_AX_KUI_L/O_AX_KUI_L\n\nRelated files:\n- HSKUIPF - Customer interface file\n- HSKUILF2 - Customer interface file with prefix hp_ \n- KUDSTAM - Customer master data file\n- HS02309F - Change tracking file\n- Axapta/D365FO files:\n  - AXD00, AXD40 - Customer data per legal entity\n  - AXSVA - Customer data consolidation\n  - INH440 - Customer change history\n  - HTKSHF - Timestamp file\n\nThe code locks the customer records in HSKUIPF/HSKUILF2 and KUDSTAM to prevent conflicts during processing.",
"HS02308":"Here is the business logic extracted from the provided RPG code:\n\nOverall Functionality:\n- This program synchronizes the customer master data between the home partner (HP) and sub-partner (SP) in an insurance system. \n- It ensures the customer number (KDNR) is consistent between HP and SP when there is a discrepancy.\n\nDetails:\n1. The program declares data structures to hold customer data records read from the database.\n\n2. It checks the runtime environment using the `umgebung` variable. If not 'SDE', it exits.\n\n3. It declares a cursor to select customer records where:\n   - HP customer number (KUI030) <> SP customer number (KUI010)  \n   - For the same customer (KUI000 = KUI020)\n\n4. It fetches and processes each customer record:\n   - Calls subroutine `sr_hpneu` to synchronize the HP and SP customer numbers \n\n5. `sr_hpneu` subroutine:\n   - Attempts to lock the customer record \n   - If lock succeeded:\n      - Calls program 'HS02304' to update the HP customer number (KUI030) with the SP customer number (KUI010)\n   - This synchronizes the customer numbers between HP and SP\n\n6. The main logic runs in a loop to process all fetched customer records.\n\nIn summary, this RPG program ensures consistency of customer numbers between home and sub partners in an insurance customer master database. It detects discrepancies and updates the home partner's customer number to match the sub partner's.\n\nThe program interacts with:\n- Customer master file (HSKUIPF) \n- Customer main file (KUDSTAM)\n- Update program HS02304\n\nNo specific UI or output handling logic. Appears to run in batch.",
"HS02307":"Here is the extracted business logic from the provided RPG code:\n\nThe code appears to be related to managing customer data and controlling document output for customers.\n\nKey functions:\n\n1. Read customer record:\n- Input parameter: Customer number \n- Read customer master record (KUIPR) and customer header record (KUDSTAR) using customer number as key\n\n2. Display customer document output rules:\n- Read document output rules (SMBEAR) for the customer using customer number as key\n- Display records in subfile\n\n3. Add document output rule:  \n- Allow user to specify new document output rule with:\n  - Billing area (BEAKRS)\n  - Output type - Mail/Fax (BEABER) \n  - Recipient - Email/Fax (BEAMAIL/BEAFAX)\n- Validate input fields\n- Add new record to SMBEAR file\n\n4. Change document output rule:\n- Allow user to change existing document output rule\n- Retrieve record from SMBEAR using key\n- Update changed fields in SMBEAR record\n\n5. Delete document output rule:\n- Allow user to delete existing document output rule \n- Retrieve record from SMBEAR using key\n- Delete record from SMBEAR\n\nRelated files:\n- KUIPR - Customer master file\n- KUDSTAR - Customer header file \n- SMBEAR - Customer document output rules\n- AXBRNR - Billing area file\n\nThe program interacts with the user through displays, accepting input and showing subfile records.",
"HS02306C1":"Here is the business logic extracted from the provided RPG code:\n\nThis appears to be an RPG program for managing customer master data duplicates in an application called SDPS.\n\nThe key points are:\n\n- Purpose: Manage duplicate customer groups in the SDPS customer master data.\n\n- Inputs:\n  - &USERP: 10-character user profile \n  - &USERN: 50-character user name\n\n- Processing:\n  - Retrieve the user profile (&USERP)\n  - Retrieve the user name (&USERN) corresponding to the user profile\n  - No other business logic is apparent from the code\n  \n- Outputs: None\n  \n- Interactions:\n  - Database:\n    - No database interactions are shown\n  - Other files: \n    - No file interactions are shown\n  - User interface:\n    - No UI interactions are shown\n    \nIn summary, this is an RPG program that retrieves the username for a given user profile. It appears to be designed to manage duplicate customer groups in an application called SDPS, but no specific business logic for that purpose is defined in the provided code. Only the username retrieval logic is shown.",
"HS02306":"Here is the extracted business logic from the provided RPG code:\n\n### Overview\nThis program allows manual management of duplicate customer groups in the customer master data system (SDPS). The key functions are:\n\n- Add a duplicate ID to a customer group\n- Remove a duplicate ID from a customer group  \n- Lock/unlock a duplicate customer\n- View and select duplicate customers for a group\n\n### Details \n\n1. The program first checks if a customer number is passed as a parameter. If so, it reads the customer record to check if it is a duplicate or master record.\n\n2. To add a duplicate ID:\n   - The master record must be displayed\n   - Enter the duplicate customer number \n   - The system validates it is not already a duplicate/master\n   - Press F24 to assign and lock the duplicate\n\n3. To manage duplicates for a group:\n   - The duplicate records for the group are loaded into a subfile\n   - Options:\n     - Lock/unlock a duplicate (Option 2)  \n     - Remove duplicate ID (Option 4)\n\n4. When removing or adding duplicates, a record is written to a logfile with the action details. \n\n5. The program ensures:\n   - Only users from Wholesale SDAT can access it\n   - Only via a personal user profile\n   - Duplicate actions are logged\n\n6. The subfile displays the duplicate records for a group\n   - Columns show duplicate data like customer number\n   - Interactive options to lock/remove duplicates\n\n7. Relevant files used:\n   - KUDSTAM - Customer master file\n   - KUDSTLFI - Duplicate customer group temp file\n   - HSKUIPF - Customer file\n   - CDDGPF - Change log file\n\nSo in summary, it provides an interactive interface to manually maintain duplicate customer groups, ensuring logging and restrictions. The core logic revolves around linking duplicates to groups, and providing options to view, lock, and remove them.",
"HS02305":"Here is the business logic extracted from the provided RPG code:\n\nThis code is part of an application called SDPS (Sales Data Processing System). It is meant to run in the SDE (Swiss Life Germany) environment.\n\nMain logic:\n\n- It retrieves data for SDE customers that have addresses belonging to inactive home partners (HP) from database tables. \n\n- For each customer, it calls another program HS02304 to change the home partner to the responsible branch, obtained from the SSP_HKZL field.\n\n- The new home partner is restricted to only Wholesale or Retail branches based on a check of the first character of BTS050.\n\n- The data retrieved includes:\n  - KUI010 - Customer number\n  - KUI020 - Old home partner number \n  - KUI030 - Customer address number\n  - SSP_HKZL - New responsible branch number\n\n- This program seems to be called by a scheduler job to periodically update home partners for customers of inactive branches.\n\nOther details:\n\n- The SQL cursor retrieves data by joining several database tables:\n  - HSKUIPF - Customer file\n  - KUDSTAM - Partner master data\n  - VKSSPF - Branch master data \n  - HSBTSPF - Branch status file\n\n- It calls program HS02304 to actually change the home partner, passing it the necessary data.\n\n- This appears to be an RPGLE program that uses embedded SQL and calls other programs.\n\n- It has some basic error handling through the use of SQL return codes.\n\n- Comments specify creation date, changelogs, and high-level purpose.\n\nIn summary, this RPGLE code handles retrieving customer data and calling another program to update inactive home partners, as part of a larger SDPS application. The key business logic revolves around identifying customers of inactive branches and changing their home partner through batch updates.",
"HS02304":"Here is the extracted business logic from the provided RPG code:\n\nPurpose:\n- This RPG program is used to change the home branch (HP) of a customer in the SDPS system. \n\nParameters:\n- Old HP branch number (HPA_KZL) \n- Old HP customer number (HPA_KDNR)\n- New HP branch number (HPN_KZL)\n- New HP customer number (HPN_KDNR)\n\nProcessing:\n1. Validate input parameters:\n   - Old and new HP must be valid, active branches\n   - Customer must be assigned to the old HP\n\n2. Get additional data:\n   - Country code (LAND)\n   - Used vehicle center branch (VBRN) \n   \n3. Lock records for old HP using record-level locks to prevent updates during processing\n\n4. Update the following files/tables for the customer:\n   - KUI (Customer data per branch) - Update HP branch/customer number\n   - KUD (Customer data per HP) - Update HP branch/customer number and used vehicle center\n   - KUK (Customer comments) - Update HP branch/customer number\n   - KUA (Customer contacts) - Update HP branch/customer number  \n   - BNK (Customer bank data) - Update HP branch/customer number\n   - BEA (Customer/contact email addresses) - Update HP branch/customer number\n   - ATT (File attachments) - Update HP branch/customer number\n   \nThe program interacts with the following files:\n\n- HSKUILF2 - Customer data file (KUI)\n- KUDSTAM - Customer data file (KUD) \n- HSKUKPF - Customer comments file (KUK)\n- HSKUAPF - Customer contacts file (KUA)\n- HSBNKF - Customer bank data file (BNK)\n- SMBEAF - Email addresses file (BEA)\n- HSBTSLF1 - Branch data file\n- AXAXTPF - Used vehicle center data file\n- CDATTF - File attachments file (ATT)\n\nThe core logic revolves around updating the customer's HP and propagating it to all associated records. Locking prevents data integrity issues.",
"HS02302":"Here is the business logic extracted from the provided RPG code:\n\nThis appears to be an RPG program that performs the following key functions:\n\n1. Updates customer master data (table KUDSTAR) from credit report data (table HSCRXF)\n\n- It first checks the environment value in DTAARA UMGEBUNG to determine the application identifier (KZLF).\n\n- It then reads the customer interface file HSKUIPR to get the customer number (KUI000/KUI010). \n\n- Using this, it chains to the customer master file KUDSTAR to retrieve the customer record.\n\n- It checks that the customer is a retail/wholesale partner based on value in BTS050.\n\n- It checks that no update from credit report has happened yet for this customer based on KUD831 value.\n\n- If above conditions are met, it retrieves the credit report data for that customer from HSCRXF using the CREFO number in KUD1020. \n\n- For each relevant field from the credit report (phone, fax, email etc.), it checks if the corresponding field in KUDSTAR is empty.\n\n- If yes, it moves the value from credit report to KUDSTAR and sets indicator KUIUPD to on.\n\n- After processing all fields, it updates KUDSTAR with the new values from credit report and sets KUD831 to indicate update done.\n\n- If any changes were made (KUIUPD = on), it also updates the interface file HSKUIPR.\n\n\n2. Related files:\n\n- KUDSTAR - Customer master file\n- HSCRXF - Credit report extract file \n- HSKUIPR - Customer interface file\n\nSo in summary, this program extracts relevant fields from credit reports and uses them to enrich empty fields in customer master records, while updating interface files to indicate changes made.",
"HS02301":"Here is the business logic extracted from the provided RPG code:\n\nPurpose:\n- This RPG program is designed to retrieve and display credit rating information for a customer from the Crefo credit agency. It is called from program HS0230 to manage customer master data.\n\nParameters:\n- §KUI010 (Input) - Customer number from Axapta\n- §CRF_PARM1 (Input/Output) - Display PDF credit report \n- §CRF_PARM2 (Output) - Credit rating score\n- §CRF_PARM3 (Output) - Option to request new credit report (disabled)\n\nMain logic:\n\n1. Validate input parameters\n\n2. Check user authorization to access Crefo website (HSCRUF file)\n\n3. Build URL link to retrieve Crefo credit report PDF or rating (crfLink variable)\n\n4. If customer has valid Crefo number (KUD1020):\n   - If §CRF_PARM1 requests PDF:\n      - Build URL to retrieve PDF report for this customer\n   - Else:  \n      - Lookup credit rating score and text in HSCRXF file using customer's Crefo number\n      - Set §CRF_PARM1 and §CRF_PARM2 output parameters with rating info\n\n5. If no valid Crefo number:\n   - Set §CRF_PARM2 to indicate rating not available\n\n6. Disable §CRF_PARM3 parameter to prevent requesting new credit report \n\nSubroutines:\n\nSR_CRF_LINK:\n- Opens web browser on IBM i and navigates to URL built in crfLink variable\n\nFiles Used:\n- HSKUIPF - Customer master file\n- KUDSTAM - Customer master file\n- HSCRUF - Crefo user authorization file\n- HSCRXF - Crefo credit rating data file\n\nThis RPG program handles retrieving credit reports and ratings from the Crefo system for customers in the SDPS application. The core logic revolves around building a dynamic URL to call Crefo APIs and mapping the rating data to output parameters. It also controls user access to Crefo.",
"HS0230":"Here is the extracted business logic from the provided RPG code:\n\n1. Customer Master File (KUDSTAM)\n\n- Stores customer header data like customer number (KUD000), name (KUD030), address (KUD060-KUD090), etc.\n\n- New customers can be added by writing a new record.\n\n- Existing customers can be updated by changing field values and rewriting the record.\n\n- Customers can be deleted by deleting the record.\n\n2. Individual Customer Data File (HSKUIPF) \n\n- Stores additional customer data like payment terms (KUI060), credit status (KUI070), payment method (KUI080), etc.\n\n- A record exists for each relationship between a customer and a branch (KUI000). \n\n- New customer-branch relationships are added by writing a new record.\n\n- Existing records are updated by changing field values and rewriting.\n\n- Allows assigning multiple customer numbers (KUI010) to the same customer master record.\n\n3. Customer Search and Selection\n\n- Customers can be searched and selected using:\n  - Customer number (KUI010)\n  - Branch key (KUI000) \n  - Matchcode (KUD050)\n  - Salesperson (KUD310)\n  - Mailing indiciator (KUI140)\n\n- Selection results are displayed in a subfile for viewing and updating.\n\n4. Maintaining Customer History\n\n- All changes to customer master and customer-branch records are logged.\n\n- Complete change history can be displayed. \n\n5. Customer Statistics\n\n- Sales statistics per customer per branch can be displayed in a subfile.\n\n6. Integration with SAP AX\n\n- Special routines to interface with SAP AX for validation, default values, updating AX records, etc.\n\n7. Address Verification\n\n- Customer addresses are verified against postal database.\n\n- Duplicate checking is performed to find potential duplicate customers.\n\n8. User Authorization\n\n- Users must be authorized to add, change or delete customers.\n\n- Password checking for sensitive fields like credit status, payment terms, etc.\n\n9. ERP Integration\n\n- Interfaces with finance system (FIBU) for account validation, check for existing accounts, etc.\n\nThe key files used are KUDSTAM for customer master data, HSKUIPF for customer-branch specific data, and HSKUDPF for change history. The program allows maintaining customer records, relationship records, statistics, histories, integration with SAP AX and FIBU, address verification, and security.",
}

def process_folder_023(parent_folder_id):    
    
    folder_name = "Customer"
    folder_business_logic = ""
    folder_structure={"files":["HS023V","HS023S","HS023L","HS023I","HS023H","HS0239_2","HS0239ALT","HS0239","HS0238C","HS0238","HS0237","HS0236","HS0235C","HS0235","HS0234","HS0232","HS0231","HS0230C1","HS0230C1","HS0230C","HS0230ALT1","HS0230ALT","HS02309","HS02308","HS02307","HS0236C1","HS0236","HS02305","HS02304","HS02302","HS02301","HS0230"]}
    files=["HS023V","HS023S","HS023L","HS023I","HS023H","HS0239_2","HS0239ALT","HS0239","HS0238C","HS0238","HS0237","HS0236",
           "HS0235C","HS0235","HS0234","HS0232","HS0231","HS0230C1","HS0230C1","HS0230C","HS0230ALT1",
           "HS0230ALT","HS02309","HS02308","HS02307","HS02306C1","HS0236","HS02305","HS02304","HS02302","HS02301","HS0230"]
    files_name=[]
    for file in files:
        if(folder_business_logic==""):
            folder_business_logic=business_023[file]
            files_name.append(file)
        else:
            folder_business_logic = combine_business_logic(folder_name,folder_structure,files_name,folder_business_logic,file,business[file])
            files_name.append(file)
    
    logic = folder_business_logic
    return logic

class HigherLevelBL023(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        folder_id = request.data.get('id') 
        # business_logic = process_folder_023(folder_id)
        return Response({"response":business_logic}, status=200)






# HS06 Files Higher Level Business Logic

business_06=[
{ "logic":"Here is the extracted business logic from the provided RPG code:\n\nThis RPG program appears to handle the positioning/assignment of components to position numbers in a workshop job/work order. The key functions include:\n\n1. Positioning various component types to position numbers:\n- Work order texts (TYP#100) \n- AGA texts (TYP#200)\n- Multi labor times (TYP#300)\n- New labor times (TYP#350)\n- Workshop/hours (TYP#400) \n- Machine hours (TYP#430)\n- Campaigns (TYP#450)\n- AGA calculations (TYP#500)\n- AGA fixed prices (TYP#600) \n- External services (TYP#700)\n- Kits (TYP#800)\n- New kits (TYP#850) \n- Parts (TYP#900)\n\n2. Displaying components in a subfile for selection/update\n\n3. Allowing mass update of selected components to a single position\n\n4. Integration with new workshop route logic (when WKO280='AV') to also position new labor times\n\n5. Integration with new external services to also position those (when FLNEU='F') \n\n6. Additional logic to:\n- Fetch and position job header/description info if called from job order processing \n- Suppress positioning if certain splits (like EPS)\n- Handle parts packaging and text\n- Display parts/kits components in kits/packages\n- Link components to workshop damage coding\n- Protect position numbers linked to jobs\n- Allow job change for certain component types\n- Filter display based on F10 option\n\nThe file I/O includes chain/reads on various externally described files like AUFWRZ, AUFWKK, AUFWTE.\n\nSo in summary, this program's business logic centers around positioning/linking various work order and job components to position numbers, supporting new functions like labor routes, external services, etc. The output subfile provides a consolidated view for selection and update.","file_name":"HS0649.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code implements functionality to manage work orders (Arbeitsaufträge/Jobs) in an auto repair shop software system (SDPS - Servicemanagement und Dienstleistung für den Kfz-Service und -Handel).\n\nKey functionality includes:\n\n- Work Order Selection Screen (Selektion Arbeitsauftrag/Job):\n  - Allows selecting and viewing details of a work order\n  - Options to add, delete work orders\n  - Retrieves work order details by joining on WO-UUID and SPL-UUID\n  - Displays work order alias, description\n  - Validates if work order is not invoiced or closed\n  \n- Work Order Management (Verwaltung Arbeitsaufträge/Jobs):\n  - Menu options to add, delete, edit work orders\n  - Add work order: Generates next alias number, copies text lines from vehicle job, writes new work order record\n  - Delete work order: Validates no invoice items exist for work order\n  - Edit work order: Allows editing description text\n  - Sub-options to view/edit Parts, Packages, Operations, Hours, Times, Positions, Outside Services for work order\n  \n- Copy Job Text Lines (Auftragstextzeilen übernehmen):\n  - Fetches text lines for vehicle job \n  - Allows selecting and copying lines into work order description\n  \n- Add Outside Services (Fremdleistungen):\n  - Validates work order is not a warranty job\n  - Calls outside services processing, passes work order details\n  \nThe code interacts with these files:\n\n- Work Order Header (AUFWKO) \n- Work Order Details (AUFJOB)\n- Job Text Lines (AUFWAW) \n- Parts (AUFWTE)\n- Packages (AUFPKO)\n- Operations (AUFWAW)\n- Times (AUFWRZ)\n- Positions (HSPOSPF)\n- Outside Services (HSFLAPF)\n\nIt uses these tables:\n\n- Location (HSBTSLF1)\n- Customer Master (FISTAM) \n\nAnd these *DTAARA:\n\n- Company (FIRMA)\n- User (ALGUSR)\n- Selected Job UUID (S_JOB_UUID)\n\nIn summary, the code provides work order management capabilities for an auto shop system, focused on selection, creation, editing, and associating information with a work order. The extracted business logic provides key details on the processing and data interactions.","file_name":"HS06210.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis program performs plausibility checking for full service contracts when creating or changing a workshop order. \n\nIt first retrieves some key variables:\n- KZLB: User group \n- KZLF: Order type\n- AUFTXT: Order text\n\nIt then does the following:\n\n1. Checks if this is a full service contract order (order type starts with F1). If not, exits.\n\n2. Retrieves the order header record based on the order number.\n\n3. Retrieves the customer master record based on the customer number. \n\n4. Performs plausibility check:\n   - Checks if the customer is allowed to have a full service contract order by looking up a validation table.\n   - If not allowed, sets an error code and displays an error message that this customer is not permitted for this order type.\n\n5. If no errors, retrieves the order text for a full service contract order and assigns it to AUFTXT.\n\nSo in summary, this program validates full service contract orders against permitted customers before allowing the order to be created or changed.\n\nIt interacts with the following files:\n\n- Order header file (AUFSTAR) \n- Customer master file (KUDSTAR)\n- Full service contract validation file (HSFSPR)\n- Order text message file (HS06006D) \n\nThe core logic is focused on ensuring full service contract orders are only permitted for certain customers. This likely prevents misuse of these special order types.","file_name":"HS06006.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program performs a plausibility check for Split N2 Scania additional equipment orders. The key steps are:\n\n1. Get current user ID from data area (ALGUSR) to determine company code (KZLB).\n\n2. Only check orders for SDAT subsidiaries. \n\n3. Check if order is for Split N2 Scania additional equipment (AUFART starts with N2). If not, exit.\n\n4. Get sales order header (VSP) and line item (VSA) records for the order from the sales module files using the shop order number (FGSTNR). \n\n5. Check sales order status (VSP200):\n   - If status is 91, 95, or 99, the order is closed in the sales module. \n   - If line item VSA090=N, it is an additional equipment order.\n\n6. If closed additional equipment order found, set order lock flag (SPERRE=*ON).\n\n7. If order locked, retrieve order details:\n   - Customer details from customer file (KUD)\n   - Vehicle details from vehicle file (FAR)\n   - Sales order date (VSA030)\n   - Sales status description (VSS040)\n\n8. Write order lock error message with details to display file HS06007D.\n\nKey files used:\n- VKVSPLF3 - Sales order header file\n- VKVSALF8 - Sales order line item file \n- VKVSSPF - Sales status descriptions file\n- HSKUIPF - Customer file\n- FFARSTAM - Vehicle file\n\nUser interface:\n- HS06007D - Display file for error messages\n\nThis program prevents booking additional equipment sales for orders that are already closed in the sales module. The plausibility check helps enforce business rules and data consistency across the sales and workshop systems.","file_name":"HS06007.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code interacts with a database table called AUFJOB to retrieve job details. It also prints the job details to the screen.\n\n1. Database Interaction:\n\n- The code executes a SQL select statement to retrieve data from the AUFJOB table where the JOB020 column matches the input parameter §JOB_UUID.\n\n- It selects two columns - JOB030 and JOB040. JOB030 contains the job alias and JOB040 contains multiline job details text. \n\n- The job details text is retrieved into the maxtext variable, which can store up to 4096 characters.\n\n2. Data Manipulation:\n\n- The multiline job details text in maxtext is split into separate variables jobbz1 to jobbz12 using the %subst built-in function. Each variable contains 40 characters of text.\n\n3. User Interface Interaction: \n\n- The job details stored in the 12 jobbz variables are printed to the screen using an EXFMT operation with the HS06211W1 screen format.\n\n- This screen format handles displaying the multiline text across 12 lines on the screen, with each variable jobbz1 to jobbz12 mapped to a specific screen line.\n\nSo in summary, the key business functionality is:\n\n- Retrieve job details from database\n- Store details in variables \n- Print job details to screen\n\nRelated files:\n\n- Database table: AUFJOB\n- Screen format: HS06211W1","file_name":"HS06211.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- This is an RPG program named HS0660 for cancelling a workshop order. \n\nMain functionality:\n- A workshop order can only be cancelled if WKO300 is 00 or blank, and there are no assigned external services (WKO830=0) to the order.\n\n- After cancellation, WKO260 gets cancellation flag '1'. \n\n- A cancellation record is written for each order item. \n\n- All order items are deleted.\n\n- Order header (AUFSTAM) is read to get the account key.\n\n- After cancellation:\n  - Transaction records are written to reduce stock levels. \n  - Wage records are deleted to reset technician statistics.\n  - Purchase order items are deleted.\n  - Campaign data is deleted.\n  - Customer outstanding data is updated.\n  - Import interface data is deleted.\n\n- Additional checks:\n  - No open clock times for the order.\n  - Cancellation only allowed if order net value is zero.\n  - No unfinished external services linked to the order.\n  - User authority check via CZM for processing external workshops.\n  - Send cancellation data to Vehicle History Information system (WHI).\n\n- Special handling: \n  - Status update for connected FTM modules/packages.\n  - EPS split orders.\n  - Job/work orders.\n  \nRelated files:\n\n- FISTAM - Customer file\n- AUFPKO - Order packages file  \n- AUFSTAM - Order header file\n- AUFWSKF - Order GWL file\n- AUFWRZ - Order standard times file \n- AUFWAW - Order wages file\n- AUFWKO - Order header file\n- AUFWTE - Order items file\n- AUFWTLF3 - Order items file\n- AUFWPK - Order packages file\n- AUFWPT - Order package items file \n- AUFWPL - Order package wages file\n- AUFWKK - Order text lines per package\n- AUFWKT - Order package campaign items\n- AUFWKL - Order package campaign wages\n- FFISTAM - Item file\n- FHSAKTLF1 - Activity file \n- FHSBTSLF1 - Operating unit file\n- FHSEPKPF - Access keys file\n- FHSKAMLF1 - Campaign file\n- FHSMONPF - Tech times file\n- FHSOBKLF1 - Customer outstanding header file \n- FHSOBKLF2 - Customer outstanding items file\n- FHSOBKLF8 - Customer outstanding per order file\n- FHSKRUPF - Customer outstanding new file\n- FHSFLALF1 - External services file\n- FHSPWDPF - Access passwords file\n- FMONSTAM - Tech master file\n- FTEISTAM - Stock file\n- FTRANSAKT - Transaction file\n- FHSMADPF - Change documentation file\n- FHSMPAF - Import parts file\n- FHSMAWPF - Import wages file \n- FHSMTEPF - Import items file\n\nThe program interacts with the database to read, update, delete and write records to perform the order cancellation functions.","file_name":"HS0660.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis program is used to check if a work order has job assignments before allowing edits. It is called from other programs like HS06400.\n\nIt receives the following input parameters:\n- §AUFNR - Work order number \n- §BEREI - Plant \n- §WETE - Confirmation counter\n- §SPLITT - Split indicator\n- §IJOB - Output parameter indicating if jobs exist\n\nThe logic is:\n\n1. Fetch the work order details into DS_WKO by joining the AUFWKO file using the input parameters.\n\n2. If the work order processing status (WKO295) is blank, exit. \n\n3. Concatenate the key fields of the work order into AUFNR9.\n\n4. Count the number of job details records for this work order in MAW (planned times) and MTE (parts list) tables. \n\n5. If the counts are zero, set §IJOB = 'N' and exit.\n\n6. If the counts are not zero, set §IJOB = 'J' \n\n7. Display error message HS06213W1 indicating jobs exist.\n\nIn summary, this program prevents editing a work order if it already has job plans or parts lists assigned. It interacts with the AUFWKO file and MAW/MTE database tables. The key output is §IJOB which indicates if jobs exist.","file_name":"HS06213.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis RPG program appears to be for printing corrected invoices (Korrekturbelege) in an automotive dealer management system (SDPS).\n\nIt does the following:\n\n1. Validates the input invoice number and date against the invoice header file (HSAHKPR).\n\n2. If there is a link to a corrected invoice (Korrekturbezug), it retrieves the header details of the referenced corrected invoice.\n\n3. Determines if the original invoice is a credit memo (Gutschrift) based on the net amount. \n\n4. Sums the net amounts of all invoices linked to the original invoice to identify consolidated invoices (Sammelrechnungen).\n\n5. Checks if the original invoice has been cancelled (storno) by looping through the invoice history file (HSAHKLR3) and looking for a cancellation document linked to the original invoice.\n\n6. Clears the subfile (SFL) with invoice corrections.\n\n7. Populates the subfile by reading the corrected invoice file (HSAHKLRP) and adding records. If no corrections exist, adds an informational record.\n\n8. Displays the subfile page-by-page, with reference information at top.\n\nThis program interacts with the following files:\n\n- HSAHKPR - Invoice header file\n- HSAHKLR3 - Invoice history file \n- HSAHKLRP - Corrected invoice file\n- HS06005S1 - Work file for subfile page\n- HS06005C1 - Subfile control record\n\nIt appears to be called from invoice printing programs like HS0650 and HS0520 to display corrections.","file_name":"HS06005.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis code is part of a larger order creation application called SDPS. It sets the discount code on the order based on certain rules.\n\nThe key logic is:\n\n1. Determine who created the order (AUF_KZLB) by looking up the user ID in a file.\n\n2. Check if the order was created by a subsidiary (Tochter), parent company (P) or shared service center (SP). This is done by looking at a field in the user record.\n\n3. Based on the order splitter type (#SPLITT), assign a default discount code (#RABCOD) by looking it up in a file (AUFSTAR). The splitter indicates the type of order.\n\n4. If the order is a certain type (R&W or W), additional logic is run to check active contracts and assign discount codes based on the contract partner. This calls a subroutine (SR_VER_CS).\n\n5. The subroutine first converts the order creation date to a date field (DAT_ANA).\n\n6. It reads through a contract file (CSCOHLR1) to find active contracts valid on the order date.\n\n7. It checks the partner type on the contract (COH_VINH) and sets flags indicating if they are an own company (VER_EIGENER), subsidiary (VER_TOCHTER), branch (VER_FILIALE), parent (VER_P), shared service center (VER_SP) or external partner (VER_EXTERN).\n\n8. Based on combinations of who created the order, which contracts are active and what type of partner is on the contract, specific discount codes are assigned.\n\n9. After running this logic, a discount code is set on the order.\n\nIn summary, this code determines a discount code by looking up default values based on order type, then overriding those where specific contract rules apply. The key external interactions are looking up data in multiple database files.","file_name":"HS06004.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nPurpose:\nThis program checks if there are any work order contents without job assignments and displays an error message if so. It is called from other programs like SDPS print program and SDPS change order program.\n\nParameters:\n- §AUFNR (Input) - Work order number\n- §BEREI (Input) - Area \n- §WETE (Input) - Work type\n- §SPLITT (Input) - Split\n- §OJOB (Output) - Flag indicating if there are contents without job ('J' or 'N')\n\nMain Logic:\n1. Load work order details (DS_WKO) by work order number, area, work type and split\n2. Check if work order has job assignments (WKO295 not blank)\n   - If no job assignments, exit with §OJOB='N' \n3. Count work order operations (WRZ) and parts (WTE) without job assignment\n   - WRZ: Richtzeiten without job package and job\n   - WTE: Parts without job package and job\n4. If count > 0, set §OJOB='J' and display error message\n5. Else set §OJOB='N'\n\nFiles Used:\n- AUFWKO (Input) - Work Order Header File\n- AUFWRZ (Input) - Work Order Operations File \n- AUFWTE (Input) - Work Order Parts File\n\nAdditional Details:\n- Called from SDPS programs like print program, change order program\n- Checks only if active work orders have contents without job assignments\n- Displays error message if contents exist without job assignment\n- Sets output parameter §OJOB to 'J' or 'N' based on validation\n- No database update or insert operations\n\nIn summary, the program validates active work orders to ensure all contents are assigned jobs before further processing. This prevents errors in subsequent processes. The key validations, error handling and output flag setting represent the core business logic.","file_name":"HS06212.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code contains several procedures, each serving a specific purpose:\n\n1. toUppercase:  \n- Purpose: Convert a given input string to uppercase.\n- Parameters: \n  - string (Input): A varchar containing the string to convert to uppercase.  \n- Logic: \n  - Uses the `%xlate` built-in function to replace lowercase letters with their uppercase counterparts in the input string.\n  - Returns the result string converted to uppercase.\n\n2. toLowercase:\n- Purpose: Convert a given input string to lowercase.  \n- Parameters:\n  - string (Input): A varchar containing the string to convert to lowercase.\n- Logic:\n  - Uses the `%xlate` built-in function to replace uppercase letters with their lowercase counterparts in the input string.\n  - Returns the result string converted to lowercase.\n\n3. allocSpace:\n- Purpose: Allocate memory space for a pointer variable.\n- Parameters:\n  - ptr (Input/Output): A pointer variable that may be allocated or reallocated.\n  - bytes (Input): An unsigned 10-byte integer specifying the amount of memory to allocate or reallocate.  \n- Logic:\n  - Checks if the ptr is null (unallocated).\n  - If ptr is null, allocates memory space of the specified size (bytes) and assigns it to the ptr.\n  - If ptr is not null, reallocates memory space to the ptr with the new size (bytes).\n  - Memory allocation and reallocation are common operations in low-level programming.\n\n4. deallocSpace:  \n- Purpose: Deallocate memory space for a pointer variable if it's not null.\n- Parameters:\n  - ptr (Input): A pointer variable that may be deallocated.\n- Logic:\n  - Checks if the ptr is not null (allocated).\n  - If ptr is not null, it deallocates the memory associated with the ptr.\n\nThe business logic extracted encompasses these four procedures, each with its specific functionality. These procedures can be used in various applications to manipulate strings, allocate and deallocate memory, and perform text case conversions.\n\nThe code interacts with files like AUFWKR, AUFTKR, HSKUIPR etc which seem to be database files for things like work orders, sales orders etc. It also calls other programs like HS06003, HS0618 etc which likely contain more business logic related to things like validating customer data, calculating pricing etc. \n\nSo in summary, the key aspects of the business logic are:\n\n- String manipulation procedures\n- Memory allocation procedures\n- Interaction with order data like work orders and sales orders\n- Validation of customer data\n- Pricing calculations and validations\n- Overall handling of work order and sales order data and processes","file_name":"HS06400.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code is for splitting sales order lines based on various conditions. \n\nIt first determines the sales order creator (AUF_KZLB) and recipient (REC_*) information.\n\nThen it checks for applicable contract conditions for the sales order by:\n\n- Opening the CSCOHL1 file and reading active contracts (COH_STATUS 4,3,5)\n- Checking the contract partner (COH_VINH) to set flags for contract with own company (VER_EIGENER), subsidiary (VER_TOCHTER) or branch (VER_FILIALE)\n- Setting flags for contract types - Repair & Warranty (VER_RW), Workshop (VER_W), Parts Deliveries (VER_PDR), Repair (VER_REP)\n\nIt also checks for active contracts in the RWVRIL file and does similar processing to set the VER_* flags\n\nNext, it validates split conditions specified in the AUFSTAR file against various rules:\n\n- Checks that sales order plant and product type match entry in AUFSTAR\n- Validates split type code (A,E,R,W) and partner (1,2,3) based on REC_* flags and contract VER_* flags\n  - E.g. Split type R3 (Repair contract, external partner) requires VER_RW/W flag but no VER_EIGENER/TOCHTER/FILIALE flag\n- Additional checks for special cases like EU recipient, intercompany orders, SP/CAS warranty, etc.\n\nIf a split condition matches, a record is written to the HS06001R output file.\n\nFinally, it reads the next entry from AUFSTAR and repeats the validation process.\n\nSo in summary, it splits sales order lines based on combinations of recipient type, contract conditions, and special split codes defined in the system.\n\nThe key files used are:\n\n- AUFSTAR: Split condition master data\n- CSCOHL1: Contracts\n- RWVRIL: Repair and warranty contracts\n- Various other files for recipient master data\n\nThe output is written to a temporary file HS06001R.","file_name":"HS06001.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nOverall Purpose:\n- Convert an existing repair order (KV) into a workshop order by specifying a target split (internal account). This involves validating the target split, transferring relevant data from the KV, and recalculating pricing.\n\nKey Steps:\n1. Get required input parameters - Order number, Area, \"From split\", \"To split\".\n\n2. Validate that the order exists and the target split is valid. If not, show error.\n\n3. Read customer master data to get country, customer discount code, subsidiary status.\n\n4. Read accounting data to get booking date. \n\n5. Validate VAT ID for EU/Non-EU split 55/65.\n\n6. Check if target split is already open:\n   - If yes, transfer data like customer number, dates, texts, pricing etc. Recalculate discount if needed.\n   - If no:\n      - Get default accounts for internal splits from DTAARA. \n      - For AXAPTA, get accounts from custom tables.\n      - Validate accounts.\n      - Create new split header record with new split.\n      \n7. Labor:\n   - Read existing labor lines.\n   - Recalculate pricing with new split. \n   - Write new labor lines with new split.\n   - Update labor statistics.\n   \n8. Parts:\n   - Delete all existing parts lines for old split.\n   - Read parts data from selection screen.\n   - Write new parts lines for each line using new split.\n   - Recalculate pricing.\n   - Update stock statistics.\n   \n9. Packages:\n   - Split package components like labor and parts.\n   - Recalculate pricing.\n   \n10. Check credit limits in AXAPTA on submit.\n\n11. Write split change data to audit trail.\n\n12. End program.\n\nKey Files Used:\n- KV Repair Orders (FAUFSTAM) \n- Pricing Conditions (FHRAZPF)\n- Accounting Master Data (FFISTAM) \n- Labor Statistics (FHSMONPF)\n- Stock Statistics (FTEISTAM)\n- AXAPTA Customer Master (FAXAXTPF)\n- AXAPTA Config Tables (FAXVOIPF)\n- Repair Order Audit Trail (FTRANSAKT)\n\nInterfaces:\n- User screen I/O\n- Database I/O \n- Call to AXAPTA credit limit check\n- Writing to audit trail\n\nIn summary, the code handles validation, data transfer, and repricing to convert a repair order to a workshop order by changing the internal split. It interacts with pricing conditions, statistics, AXAPTA and audit trail.\n\nPlease let me know if you need any clarification or have additional questions!","file_name":"HS0670.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program is used to determine the product code (#PRD) and contract number (#SPZ) to use based on the input contract type (#SPLITT), date (#ANATAG), and active contracts.\n\nIt first validates if the input contract type (#SPLITT) is valid (R, W, A, E). \n\nIt then validates the input date (#ANATAG) if provided, converting it to an internal date format (DAT_ANA).\n\nIt checks if a product code (#PRD) and contract number (#SPZ) were passed as input parameters. If not, it will determine them based on active contracts.\n\nThe program checks if processing should use the CS (customer system) or RW (Scania system) by looking at a flag (CSAKT).\n\nIt calls subroutines to check active contracts and determine the #PRD and #SPZ:\n\n- SR_VER_CS - Checks active contracts in the CS system (CSCOHL1 file)\n- SR_VER_RW - Checks active contracts in the RW system (RWVRILF4 file)\n\nFor each active contract found with the passed contract type (#SPLITT), it determines:\n\n- #PRD based on contract type (RAM, MAIN, PDR, REP) and contract service type\n- #SPZ as the contract ID/number \n\nAdditional logic:\n\n- Sets on LR indicator on end\n- CSCOHL1 and RWVRILF4 files are used\n- Contract status values indicate active, preliminarily terminated, fulfilled contracts\n- #SPZ is appended with RW, AV, or RE based on contract type\n\nSo in summary, this program's core logic is to map active contracts to product codes and contract numbers based on some input criteria. It interacts with the CSCOHL1 and RWVRILF4 files.","file_name":"HS06003.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverall Purpose:\n- This RPG program checks if a sales order split is valid based on the sales contract data. It validates if the sales order partner (sold-to party) matches the contract partner as per the split type.\n\nParameters:\n- #FGST17: Sales contract number (input)  \n- #SPLITT: Sales order split type (input)   \n- #CSOK: Output parameter - 'J' if split is valid, 'N' if invalid (output)\n- #ANATAG: Order acceptance date (input)\n- #AUFNR9: Sales order number, 9-digit (input)\n\nFiles Used:\n- CSCOHL1: Sales contracts file\n- RWVRILF4: Sales contracts file (for contract types RW and W)  \n- HSBTSLF1: Partner master data file\n- HSKUIPF: Customer master data file\n- KUDSTAR: Customer master address data file\n- AUFWKO: Sales order file\n- HSFILPF: Branch office master data file\n\nMain Logic:\n1. Get sales order creator country code and partner type code\n2. Check if order creator is a subsidiary partner\n3. If updating recipient in sales order is allowed, set indicator ON\n4. Get order acceptance date\n5. Validate EPC for Q4 split (call external procedure) \n6. If split type is R, W, A or E\n   - Call validation subroutine for CS contracts or RW contracts \n   - If required contract number is blank, set invalid\n   - If split type doesn't match contract partner type, set invalid\n7. If split type is A4 (ARV GWL) but user not allowed, set invalid \n8. If split is valid, set output indicator valid, else invalid\n9. If invalid:\n   - Display error message\n   - Get sales order partner details\n   - Get sales contract partner details\n   - Display sales contract number\n10. If subsidiary order and split is valid: \n   - Validate sales order recipient = sales contract partner\n   - If recipient needs updating:\n      - Get sales contract partner\n      - Update sales order recipient from customer master file\n      - Set output indicator valid or invalid\n   - If invalid:\n      - Display error message\n      - Get sales order partner details\n      - Get sales contract partner details\n      - Display sales contract number\n      \nSubroutines:\n- SR_FEHLER: Displays general error message\n- SR_VER_CS: Validates CS contracts\n- SR_VER_RW: Validates RW contracts\n- SR_KDRECH: Validates and updates sales order recipient \n\nSo in summary, this program validates sales order splits against the sales contract data to ensure data integrity.","file_name":"HS06002.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code is for maintaining burden codes (BC) which are used for processing standard times.\n\nKey functions:\n\n1. Add new BC record\n\n- Allowed range is 20-59\n- Validate BC is not blank or duplicate\n- Write new record to BC file (HSBCVPR) \n\n2. Update existing BC record\n\n- Move user input fields to BC record\n- Update BC file (HSBCVPR)\n\n3. Delete existing BC record \n\n- Validate BC not used in other records (HSBCSPR)\n- Protect records 01-19 and 9A-9Z \n- Delete BC record from BC file (HSBCVPR)\n\n4. Display BC records in subfile\n\n- Clear then fill subfile with BC records \n- Protect records 01-19 and 9A-9Z\n\nRelated files:\n\n- HSBCVPR - BC master file\n- HSBCSPR - Stores BC usage in other records \n\nThe code allows maintaining burden codes which are used in standard time processing. Key functions include add, update, delete and display of BC records while validating values and protecting certain ranges.","file_name":"HS0602.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code implements customer credit limit checking functionality by interacting with the AXAPTA ERP system.\n\nMain steps:\n\n1. Check if user is authorized for SDPS access (KZLB)\n\n2. Check if AXAPTA is active (AXAPTA variable) \n\n3. Check if credit limit functionality is active (AXAKLA variable)\n\n4. Retrieve customer data from SDPS (HSKUIPR) and AXAPTA (KUDSTAR) files\n\n5. Get additional customer info from AXAPTA (AXAXTLR5/AXAXTLR2) \n\n6. Get customer credit limit data from AXKLKR file\n\n7. Check if customer has temporary credit limit (KLK_TKL field)\n\n8. Validate if current date is within temporary credit limit validity period (KLK_TKLV, KLK_TKLB)\n\n9. Calculate customer turnover over past years by retrieving data from HSBKULR2 file\n\n10. Check if turnover meets specified minimum (F_UMS field) \n\n11. Write filtered customer data to output file HS0616PR\n\n12. Allow downloading of output file (HS0616C2 call)\n\nThe code interacts with the following files:\n- SDPS files: HSBTSLR1, HSKUIPR, KUDSTAR \n- AXAPTA files: AXAXTLR5, AXAXTLR2, AXKLKR\n- Turnover file: HSBKULR2\n- Output file: HS0616PR\n\nAdditional details:\n- Uses selection criteria entered in screen fields (F_AXG, F_AXV etc) to filter data\n- Converts identifying codes (AXG, AXV etc) into descriptive values\n- Stores workflow status and messages in INFO45 field\n- Cursor positioning logic present \n\nIn summary, this program implements credit limit validation for customers by retrieving data from multiple systems and applying complex selection rules.","file_name":"HS0616.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverall Program Purpose:\n- This program implements claim handling functionality and integration with the workshop process in an ERP system. It allows creating, updating, closing, and deleting claims associated with workshop orders.\n\nKey Actions:\n- WRITE - Create/update a claim when printing invoice/credit note for workshop order\n- DLTCL - Delete a claim when cancelling a workshop order  \n- RSTO - Check claim when cancelling a workshop invoice\n- CHKD - Validate claim when changing workshop order (interactive mode)\n- CHKB - Validate claim when changing workshop order (batch mode)\n- CHKS - Validate site for claim handling (batch) \n- CHKSP - Validate site/split for claim handling (batch)\n\nClaim Status Values:\n- -1 - Invalid site, no claim handling \n- -2 - Invalid split, no claim handling\n- 0 - Valid split, initial claim request still open\n- 1 - Open, under review\n- 2 - Revision, under review\n- 5 - Rejected\n- 7 - Released, ready for invoicing\n- 9 - Closed, invoiced\n\nKey Validation Logic:\n- If claim status is -1 or -2, return 'EXIT', no claim handling allowed\n- If claim status is 0 or 5, return 'GO' to allow processing\n- For other statuses, return 'EXIT' to prevent changes\n\n- On WRITE action (invoice/credit note):\n  - If status 0 or 5, create/update claim and return 'EXIT'\n  - If status 7, close claim and return 'GO'\n- On DLTCL action (order cancellation):\n  - If status 5, delete claim\n- On RSTO action (invoice cancellation):\n  - If status 0, prompt user and return 'EXIT'\n- On CHKDS action (status display):\n  - Always prompt user and return 'EXIT' \n- On CHKD action (interactive change):\n  - Always prompt user\n- On CHKB action (batch change):\n  - No prompting\n\nAdditional functions:\n- Get claim details\n- Validate input data\n- Retrieve contact info\n- Generate prompts with claim status and comments\n\nThe code interacts with the CHRQHF table to create, read, update, and delete claims.\n\nSo in summary, it enables integration of claim handling with the standard workshop process through validation, prompting, and posting of claims.","file_name":"HS06501.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis program is used to print invoices/receipts either via email (as PDF) or to a printer. \n\nIt is called from programs HS0651 and HS0520 for printing invoices for workshop and counter respectively.\n\nIt handles the following invoice types (SSP_KEN1):\n- Retail (T) \n- Wholesale (Z)\n\nAnd the following split types (SPLITT):  \n- X2 Internal\n- X3 Subsidiary\n\nThe logic is:\n\n1. Get user ID to determine location code (KZLB)\n2. Based on invoice type (WETE), get customer number (KDRECH) and branch (BRANCH) for email from file AUFWKO/AUFTKO\n\n3. For internal split (X2):\n   - Only allow SD* branches  \n   - Get email recipient from file VKSSPLR7 based on org code\n\n4. For subsidiary split (X3): \n   - Only allow external customer numbers starting with 6\n   - Use customer number as email recipient\n\n5. Special handling for claim types AX, EX, RX, WX:\n   - Print invoice after release by accounting\n   - Archive invoice\n   - No printing\n   - No email\n\nFiles used:\n- VKSSPLR4 - Location file\n- VKSSPLR7 - Branch file\n- AUFWKO - Workshop order file\n- AUFTKO - Counter order file\n\nIn summary, it determines the correct email recipient based on invoice type, split, branch etc. and prints or emails the invoice accordingly. Special handling is done for certain claim types.","file_name":"HS06515.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverall Program Purpose:\n- This program is designed to duplicate shop order documents with different spool file names and output queues.\n\nMain Logic:\n- It first checks if the spool master is active by checking a flag in the CTLHS7 data area. \n- It gets the user ID from the ALGUSR data area to use as a key.\n- It reads records from the CDBSKR file by key, checking for records that have:\n  - Original spool file name (KSPLFO)\n  - Duplicate spool file name (KSPLFK) \n  - Different original and duplicate output queue names (KOUTQK vs BELPRT)\n- For records meeting above criteria, it calls subroutine SR_KOPIE to duplicate the spool file.\n- The duplicate spool job command is built dynamically using the file names and queues. \n- The number of duplicate copies is based on field KANZK.\n- Error handling is in place to monitor the duplicate command.\n\nFile Interactions:\n- CDBSKR File\n  - Input file, read by key\n  - Contains original and duplicate spool file names and output queues\n- No database or UI interactions\n\nSo in summary, this program facilitates customized spool file duplication for shop order documents, allowing the duplicates to be sent to different output queues than the originals. The duplication criteria and parameters come from the CDBSKR file.","file_name":"HS06514.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis RPG program appears to be for validating and selecting account and cost center values in some kind of order entry system.\n\nThe key procedures and logic are:\n\n1. PLAUSI - Validation logic\n- Validates passed in account number (AXKTO) and cost center (AXKST)\n- Looks up account and cost center values in HSAXIF file\n- If not found, sets error messages \n- If found, sets description and explanation text\n- Sets OK flag if both account and cost center are valid\n\n2. BEDF - Interactive selection logic\n- Allows user to select account or cost center from list\n- Builds selection list by:\n  - If account selected, retrieves valid accounts from HSAXIL1\n  - If cost center selected:\n    - If account not already selected, retrieves all cost centers\n    - If account selected, gets valid cost centers for that account from HSAXDL1\n- Allows user to page through selection list and pick value\n- Returns selected account or cost center value\n\n3. SFL1* - Selection list display logic\n- Clears (SFL1LOE)\n- Loads (SFL1LAD) \n  - Calls KSTSTSSR to check if filtering cost centers by account\n- Displays number of records (SFL1ANZ)\n- Handles selection and return to caller (SFL1AUSW)\n\n4. KSTSTSSR - Cost center filtering logic\n- If account passed, checks HSAXDL1 if only certain cost centers allowed for account\n- Sets indicator if all cost centers allowed or just certain ones\n\nThe program interacts with the following files:\n\n- HSAXIF - Main account and cost center file\n- HSAXIL1 - Account extract from HSAXIF \n- HSAXDL1 - Account/valid cost center relationship file\n\nAnd the following screens:\n\n- HS0617W1 - Main order entry screen\n- HS0617W2 - Selection list display\n- HS0617C1 - Selection list format\n\nIn summary, the key business logic is to validate account and cost center entries, optionally allow interactive selection, and restrict cost center selection by account if defined.","file_name":"HS0617.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code is for controlling the default workload codes (Belastungscode, BC) used for processing job times. The BC defaults are defined by categories:\n\n- Category A: Order \n- Category K: Customer\n- Category L: Service\n\nThe logic is:\n\n1. Category A overrides Categories K and L\n2. Category K overrides Category L \n3. Category L overrides the default BC (BCV010)\n\nAdditional logic:\n\n- If BC (BCS010) = K, then use customer-specific defaults --> No discount on wages\n- If BC (BCV050) = J, then billing rate can be changed + No discount on wages \n\nThe code contains procedures for:\n\n1. Converting strings to uppercase and lowercase\n\n2. Allocating and deallocating memory for a pointer variable\n\n3. Controlling BC default values:\n   - Adding a new BC default\n   - Changing an existing BC default\n   - Deleting a BC default\n   \n4. Checking if the job involves R&W split billing\n\n5. Protecting entries from central price control system (BC 9A-9Z) from being changed\n\nThe BC default values are stored in a file called HSBCSLR1.\n\nOther relevant files:\n- HSKUIPR: Customer master data\n- HSRZNPR: Service master data \n- HSBCSLR1: BC default values\n- HSBCSLR1: Central price control entries\n\nThe code interacts with these files to retrieve data for lookups and maintain the BC default values.\n\nNo specific UI or database interactions are coded. The lookups leverage built-in RPG functions for file I/O.\n\nIn summary, the key business logic is setting workload code defaults by category, with a hierarchy that allows higher categories to override lower ones. The code facilitates maintaining these defaults.","file_name":"HS0603.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code contains several procedures serving different purposes:\n\n1. Credit Limit Check for Sales Order\n\n- The program is called when creating or changing a sales order in Axapta. \n\n- It checks if the customer has a credit limit defined in Axapta.\n\n- It calculates the total outstanding invoices and open sales orders for the customer.\n\n- It retrieves any temporary credit limit overrides defined for the customer.\n\n- It calculates if the total outstanding amount exceeds the credit limit.\n\n- If the limit is exceeded, a warning is displayed to the user.\n\n- The program blocks creation of new sales orders that exceed the credit limit, if credit limit lock is activated in Axapta.\n\n- Exceptions can be defined per sales order to allow exceeding the limit.\n\n2. Credit Limit Monitoring\n\n- This procedure is called from a batch program HS06157.\n\n- It periodically checks for customers exceeding credit limits.\n\n- If limits are exceeded, warnings are logged and displayed to users entering new sales orders.\n\n- Warnings are only displayed once per user per sales order to avoid repetitive alerts.\n\n3. Credit Limit Warning Log\n\n- Warnings are logged to a file HSKLPF for audit purposes.\n\n- Log entries contain customer data, limit info, user, date/time etc.\n\n- The log provides a history of credit limit warnings.\n\n4. Temporary Credit Limit Extensions\n\n- Additional credit limit amounts can be defined in Axapta on a temporary basis.\n\n- If a temporary limit exists for the customer, it is used instead of the permanent limit.\n\n- This allows overriding the standard limit for a defined period.\n\n5. Credit Limit Exceptions\n\n- Exceptions can be defined per sales order to allow exceeding the credit limit. \n\n- They are checked before blocking sales orders exceeding the limit.\n\n- If an exception exists, the order can be created despite exceeding the limit.\n\nIn summary, the program implements comprehensive credit limit checking integrated with Axapta order processing. It provides warnings, blocking, logging and overrides to manage credit limits.\n\nThe code interacts with the Axapta database for:\n\n- Customer master data\n- Sales orders\n- Invoices\n- Credit limits and exceptions\n\nAnd additionally uses these files: \n\n- HSKLPF for logging warnings\n- Temporary tables HS0615S1, HSKLOF for calculations\n\nThe user interface consists of a display file HS0615D to show the warnings.","file_name":"HS0615.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis program checks if there is an active maintenance agreement (R&W-Vertrag) or an upcoming due date for a vehicle service. Based on the input parameters, it either displays an alert on the screen (HS0600) or calls the due date monitoring program (HS0650).\n\nKey steps:\n\n1. Check if a maintenance agreement record (RWVRILF4) exists for the vehicle (FGNR).\n   - If yes, set indicator 50 to show the alert on screen.\n   - If the agreement has expired, show additional alert text.\n\n2. Check the due date monitoring data (CTLHS3, CTLHS4):\n   - Get the due date interval (TAGEA) and convert it to days (TAGE). Default is 30 days if no interval.\n   - Get the current odometer reading (KM_AKT) from the vehicle master data (DG_KM). \n   - Add tolerance kilometers (KM_TOL) to the current reading.\n\n3. Read the upcoming due dates file (HSFZTPF):\n   - For each record, check if the due date or the odometer limit has been reached and the service is not marked completed.\n   - If yes, set indicator 51 to show the alert.\n   - Get the due date (FZT020) and description (FZT030) to display.\n   - Exit loop once first upcoming due date is found.\n\n4. Based on the parameters:\n   - If PGM called, start due date monitoring program HS0051.\n   - If ANZ called, display the alert screen HS0601W1 if R&W or due date exists.\n   - If RUE called, return indicator if a due date is approaching.\n\nFiles used:\n- RWVRILF4 - Maintenance agreement master data\n- CTLHS3, CTLHS4 - Due date monitoring control data\n- HSFZTPF - Upcoming due dates\n- Vehicle master data (FGNR)\n\nUI interaction:\n- HS0600 - Display alert screen\n- HS0650 - Due date monitoring program\n\nThis summarizes the key business logic extracted from the provided RPG code. It checks for due dates and maintenance agreements, retrieves the necessary data, and displays alerts or starts monitoring based on defined parameters. The code interacts with master data, control data, and transaction files as well as UI programs.","file_name":"HS0601.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code is for processing workshop orders and their work steps.\n\nMain functions:\n\n1. Load and display workshop order details like order number, department, supervisor etc.\n\n2. Load associated work steps for the workshop order from database table AUFWAW. \n\n3. Allow adding, changing and deleting work steps.\n\n4. When adding a work step:\n\n   - Validate if work step number exists in AGAASTAR table  \n   - Check if work step already exists for the order\n   - Call external program HS0615 to check credit limit\n   - Write new work step records to AUFWAW table\n\n5. When changing a work step:\n\n   - Update description and amounts for the work step in AUFWAW\n\n6. When deleting a work step:\n   - Delete the work step records from AUFWAW\n\n7. Recalculate amounts for a work step when changed\n\n8. Maintain totals for the order like gross total \n\n9. Interface with external system:\n\n   - Call HS0212 program to sync with central work step database\n   - Call HS0615 program to check credit limits\n\nRelevant files:\n\n- AUFWKO: Contains workshop order header records \n- AUFWAW: Contains workshop order work step records\n- AGAASTAR: Contains valid work step numbers\n\nThe program allows maintaining workshop orders and their work steps in an interactive mode through a display file.","file_name":"HS06270.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nPurpose:\n- This RPG program is designed to generate invoices for open workshop orders that have a claim status of 'released' (status 7). \n- It runs as a batch job to process and invoice the selected open claims.\n\nMain Steps:\n1. Select open workshop orders with claim status 7 that need invoicing.\n2. For each order:\n   - Validate if order exists in order header file (AUFWKO).\n   - Delete any existing invoice records for the order from invoice file (HSAKTPR).\n   - Determine invoice type - normal or correction invoice.\n   - Call program HS0650 to print invoice document.\n   - Update claim status to 9 (closed) after invoicing.\n   - Write invoice number and date to claim record.\n\nDatabase Files Used:\n- CHRQHF - Claim Header File \n- AUFWKO - Order Header File\n- HSAKTPR - Invoice File\n\nInput Files:\n- None\n\nOutput Files: \n- Spool file (invoice printout)\n\nProcedures Used:\n- SR_SEL - Builds SQL select statement to retrieve open claims for invoicing \n- SR_SEL_QRY - Executes SQL statement and processes result set\n- SR_WKO - Validates order, deletes existing invoices, determines invoice type, calls print program\n- SR_WRITE - Updates claim with invoice details \n- SR_CLOSE - Closes claim by updating status to 9\n\nCalled Programs: \n- HS0650 - Used to print invoice document for order\n\nAdditional Details:\n- Runs in batch mode using specific output queue\n- Output queue archives PDF invoices, no printing \n- Invoked by job CLAIM_FAK in program HS0796C\n\nIn summary, this RPG program handles the invoicing process for released workshop order claims by retrieving the open claims, processing each order, printing invoices, updating claims with invoice details, and closing the claims.","file_name":"HS06502.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code implements functionality to generate XML invoices and credit notes in the XRechnung format based on input data.\n\nIt contains the following key procedures:\n\ninit:\n- Initializes variables, creates temp table, gets input parameters\n\ndisplayWindow: \n- If invoice number not provided, prompts user for input\n- Gets invoice header data from database based on invoice number\n- Determines invoice type, id, date etc. \n\nprocess:\n- Main processing routine\n- Calls other procedures to build XML\n- Writes XML to file\n\ngetHeader:\n- Builds XML header section with invoice metadata\n- Includes customization ID, invoice ID, dates etc.\n\ngetParty: \n- Builds XML party section for supplier and customer \n\ngetDetails:\n- Builds XML invoice line section by looping through invoice records\n\ngetPayment:\n- Builds XML payment info section\n\ngetDelivery:\n- Builds XML delivery section with delivery address and date\n\ninsertRecord:  \n- Inserts a record into the temp work file\n\ndeleteRecords:\n- Deletes all records from the temp work file\n\nOther procedures:\n- Retrieve and build various sections of the XML file: line items, descriptions, packages, payment terms etc.\n\nThe code interacts with the database to retrieve header info, party data, invoice lines etc.\n\nIt generates an XML file containing the full XRechnung invoice and writes it out to the IFS.\n\nSo in summary, this is an RPG program that takes invoice data, builds a compliant XRechnung XML file and outputs it. The key steps are data retrieval, structure building and XML generation.","file_name":"HS0654_ORG.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverall Program Logic:\n- This program generates an XML invoice file conforming to the Austrian eInvoice standard based on input invoice header (AXMRKPF/AHKPF) and detail (AXMRPPF/HSAHTPF/HSAHWPF/HSAHPPF) records.\n\n- It first initializes based on input parameters p_rnr (invoice number) and p_rdat (invoice date). If parameters are missing, it prompts user to enter them.\n\n- It then processes the invoice by:\n  - Retrieving header/detail records\n  - Generating XML output\n  - Writing payment info\n  - Exporting XML file\n\nKey Procedures:\n\n1. init:\n  - Initializes required fields like invoice number, date etc.\n  - Prompts for input if parameters are missing.\n  - Determines invoice type based on number.\n  \n2. process: \n  - Main processing routine.\n  - Retrieves invoice header and detail records.\n  - Generates XML document structure.\n  - Writes invoice header fields.\n  - Calls procedures to write details and payment info.\n  - Exports XML file.\n\n3. getDetails/getDetails00:\n  - Retrieves and writes invoice detail lines (parts, labor, packages).\n  - Generates XML for each detail line item.\n  - Writes tax and total amounts.\n\n4. getParts/getLabour/getPackages:\n  - Fetches parts/labor/packages records and calls insertRecord to add to invoice.\n\n5. insertRecord:\n  - Inserts a record into temporary table for invoice details.\n\n6. writePayment:\n  - Writes payment method and account details in XML.\n\n7. checkCustomer:\n  - Checks if customer accepts eInvoices based on configuration.\n\nKey Files:\n- Input files:\n  - AXMRKPF/AXMRPPF: Manual invoice header/details\n  - AHKPF/HSAHTPF/HSAHWPF/HSAHPPF: Workshop invoice header/details \n  \n- Temporary work file: \n  - HS0653PF: Used to accumulate invoice details\n\n- Output file:\n  - XML file in format required by Austrian eInvoice standard\n  \n- Configuration files: \n  - FISTAM: Biller info\n  - HSANSPF: Contact info\n  - VKSSPF: Org config\n  - HSKUIPF: Customer eInvoice flag\n  \n- Other files:\n  - HSBNKF: Bank info\n  \n\nSo in summary, the program's overall logic is to gather data from various sources, assemble it into the proper XML document structure, and then export as an eInvoice file. The key steps are data retrieval, XML generation, and output formatting based on a standard.","file_name":"HS0653_V40.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program is designed to print an invoice for a workshop order as part of the Digital Vehicle Return (DFR) process in the WebSDPS application.\n\nThe key steps are:\n\n1. Validate that this program is only called for the DFR process.\n\n2. Set the library list for WebSDPS.\n\n3. Open required files - HSAKTPF and AUFWKO.\n\n4. Retrieve the workshop order details - AUFNR9, WKO020, WKO030, WKO040, WKO050.\n\n5. Validate that:\n   - The workshop order exists.\n   - It has not already been invoiced.\n   - It has not been cancelled.\n   - It is not locked by another user.\n   - There is no open job card time logged. \n   - The required SR000001 scan package exists.\n   - There are no zero value standard times.\n   - Standard times and technician times are consistent.\n\n6. Update the invoice creator in the order - WKO772. \n\n7. Call program HS0650 to print the workshop order invoice, passing the order details.\n\n8. Check for errors and provide confirmation or error message.\n\n9. Close files.\n\nThe program interacts with these database files:\n\n- HSAKTPF - Active user file\n- AUFWKO - Workshop order file\n\nAnd calls this other program:\n\n- HS0650 - Print workshop order invoice\n\nThe key data items used are:\n\n- AUFNR9 - Workshop order number \n- WKO020/030/040/050 - Order details\n- WKO300 - Invoice status\n- WKO260 - Cancellation flag\n- WKO772 - Invoice creator\n\nSo in summary, it validates a workshop order and then generates the invoice by calling another program. The focus is workshop order processing for DFR.","file_name":"HS06503.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\n1. Customer Order Opening\n\n- Allows opening a customer order by entering vehicle data or customer number. \n\n- Validates and retrieves vehicle data like registration number, chassis number, vehicle type etc from the vehicle master data file (FARSTAM).\n\n- Validates and retrieves customer data like name, address etc from the customer master data file (KUDSTAM).\n\n- Performs checks for duplicate customer numbers, valid dates, allowed order types based on customer etc.\n\n- Default values are populated for various fields like order type, dates, advisor etc.\n\n- Special logic for Scania vehicles to retrieve additional details from SCAS.\n\n2. Order Split Selection\n\n- Allows selecting the order split type like warranty, repair contract, campaign etc.\n\n- Checks if active vehicle contracts like R&W, ARV, REP are present and shows messages. \n\n- For contracted services, prompts to select the appropriate CS split based on active contracts.\n\n- Default split values set based on customer type, vehicle type etc.\n\n3. Validation and Defaults\n\n- Various validations on dates, vehicle details, customer info, order types etc.\n\n- Default values populated for fields like dates, times, order accounts etc based on configs.\n\n4. Updates\n\n- Updates the customer, vehicle and order files with the new order data.\n\n- Maintains change history for customer and vehicle master data.\n\n5. Integration\n\n- Integration with SCAS system to retrieve vehicle details.\n\n- Integration with AXAPTA ERP system for additional validations.\n\n- Integration with other systems like DKV, UTA etc.\n\n6. Miscellaneous\n\n- Displays vehicle comments, campaign info etc based on configs.\n\n- Email address management routine.\n\n- Other features like credit limit check, technician calendar, job management etc.\n\nThe key files used are KUDSTAM for customer master, FARSTAM for vehicle master and AUFWKO for order document. The program allows creating and maintaining customer vehicle orders in an automobile dealer scenario.","file_name":"HS0600.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- This code is for damage coding on work orders in a workshop management system. It allows entering damage codes by customer and workshop.\n\nKey Files:\n- AUFWKO: Work order header file\n- AUFWSK: Work order damage coding file\n- AUFWSKF: Damage coding file layout \n- CWPMSGF: CWP message file \n- CWPMSRF: CWP message relations file\n\nProcedures:\n\n1. SR_WSK: Displays and maintains damage coding screen\n- Clears damage coding subfile \n- Reads work order damage codes into subfile\n- Allows adding, changing and deleting damage codes\n- Validates codes against CWP message file\n- Displays related CWP messages as search help for codes\n- Writes changed codes back to AUFWSK file\n\n2. SR_HINZU: Adds new damage code\n- Validates code against CWP message file\n- Writes new code to AUFWSK file\n\n3. SR_AENDERN_K: Changes existing customer damage code\n- Validates changed code against CWP message file  \n- Updates code in AUFWSK file\n\n4. SR_AENDERN_W: Changes existing workshop damage code\n- Validates changed code against CWP message file\n- Updates code in AUFWSK file\n\n5. SR_LOESCHEN: Deletes existing damage code\n- Deletes code from AUFWSK file\n\n6. SR_MSG_ID_K: Validates customer damage code against CWP message file\n\n7. SR_MSG_ID_W: Validates workshop damage code against CWP message file\n\n8. SR_AUFPOS: Checks if damage code is assigned to a valid work order position\n\n9. SR_COD_POS: Checks for damage codes without positions\n\n10. SR_POS_COD: Checks for positions without damage codes\n\n11. SR_CODW_OK: Checks if workshop damage coding is complete\n\n12. SR_EPA_I: Displays related extended prices (EPS)\n\n13. SR_EPA_DEL: Deletes related EPS when damage code is deleted\n\n14. SR_JOB: Retrieves related work order job UUID \n\nIn summary, the code provides maintenance of damage coding on work orders, validating codes and related positions, with integration to CWP message file.","file_name":"HS0614.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe program allows managing workshop orders and contains the following key functionality:\n\n1. Check if a workshop order already exists and is active before allowing edits (SRACT routine). Prevent simultaneous editing by multiple users.\n\n2. Validate and update customer master data (KDUPD routine) including name, address, payment info etc. Write change history. \n\n3. Validate and update vehicle master data (FZUPD routine) including registration number, vehicle type, manufacture year etc. Update mileage history.\n\n4. Check for open campaigns related to the order and vehicle (SRKAM routine). \n\n5. Validate order header details like dates, times, vehicle info. Check date sequences are valid.\n\n6. Allow editing order text lines, inserting blank lines, positioning text etc. (ADTEXT routine).\n\n7. Allow entry of standard jobs/service items, checking validity, prices, discounts etc. (ADFEST routine).\n\n8. Calculate totals and taxes for jobs. Check credit limits. \n\n9. Allow entry of parts/accessories, checking stock levels and prices (SRPAK routine).\n\n10. Check if parts are under warranty (SR07 routine).\n\n11. Check upcoming maintenance appointments (SR08 routine).  \n\n12. Retrieve and display vehicle info from 3rd party system (SR20 routine).\n\n13. Print workshop orders and invoices (SRDRU routine).\n\n14. Interact with other systems: ERP (AXAPTA), Contracts (RWVRIPF), Campaigns (HS06090), Rental (MULTI.EXE) etc.\n\nThe program interacts with these files:\nHSFAIPF, FARSTAM, AUFWKO, AUFWAW, HSAKTLF1, HSBONPF, HSBSTL1, HSEPKPF, HSKAMPF, HSKUIPF etc.\n\nIt uses these keyed lists: \nKEYWKO, KEYWAW, KEYAGA, KEYEPK, KEYKEN, KEYKDR, KEYKDA etc. \n\nAnd contains these other notable routines:\nKOMMEN, KDUPD, FZUPD, SR05, SR14, SR19, INTPLAUSI, INTPLAUSIAX, SR_TEILE etc.\n\nIn summary, the core logic revolves around workshop order management and integration with surrounding systems. The code ensures data validity across the order lifecycle.","file_name":"HS0610.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program is designed to calculate and print wage supplements for mechanics on work orders when certain conditions are met.\n\nThe key steps are:\n\n1. Read work order header (AUFWKO) and wage supplement (AUFWAW) files by work order number (AUFNR), branch (BEREI), date (WETE), split (SPLITT).\n\n2. If work order status (WKO280) is not 'AV' (completed), skip processing. Also skip if work order is still open (WKO300 <> '00').\n\n3. Initialize wage supplement record (WAW) for each mechanic (WAWEGR='01') with default values.\n\n4. Zero out wage fields WAW160, WAW190, WAW110 for all mechanics to reset totals. \n\n5. Calculate total hours for all mechanics on work order (SUMME_H).\n\n6. For each mechanic, if wage code (WAW060) is labor (>'01') and supplement indicator (WAW230) is '1', check if supplement percentage (WAW170) > 0. \n\n7. Calculate supplement amount (ZUSCHLAG) by multiplying hours (WAW150) by supplement percentage (WAW170).\n\n8. Write wage supplement record (WAW) for each mechanic with supplement code (WAWZUS), hours (WAW100), amounts (WAW160, WAW190). \n\n9. Optionally calculate overtime wage supplement based on total PE hours.\n\n10. Delete any wage records (WAW) where net amount (WAW190) = 0.\n\n11. Write wage supplement report (AUFWAW).\n\nFiles used:\n- AUFWKO - Work order header\n- AUFWAW - Wage supplement \n- AUFWRZ - Wage line items\n\nThis program calculates wage supplements for mechanics on completed work orders based on hours worked and designated supplement percentage. The results are written to the wage supplement file and report.","file_name":"HS0604.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program is designed to print vehicle comments on the workshop order confirmation.\n\nIt performs the following key functions:\n\n1. Checks if vehicle info should be printed on order confirmation:\n\n- Checks if a flag is set to print vehicle info on confirmations \n- Checks if it's a branch office or central workshop order\n- Sets a flag to print vehicle info if conditions are met\n\n2. Loads comments from work file:\n\n- Opens work file HS06512F\n- Chains to vehicle master record using vehicle number input parameter\n- Gets vehicle number, type and registration number \n- Calls subroutines to clear and fill the SFL comments display file\n\n3. Displays comments: \n\n- Writes records to display comments on a window\n- Allows adding/changing/deleting comments interactively\n\n4. Prints comments:\n\n- Option to print with or without comments \n- Deletes comment records if printing without\n- Closes and reopens work file to rebuild with vehicle info\n- Calls program to rebuild work file with vehicle info\n\nKey files used:\n\n- HS06512F - Work file with comments\n- HS06513S1 - SFL display file \n- FARSTLR4 - Vehicle master file\n- HS06512R - Comment records file\n\nThis program interacts with the user by displaying comments on a window and allowing edits before printing on the order confirmation.","file_name":"HS06513.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code contains procedures to print vehicle workshop information on a document.\n\nMain logic:\n\n1. Get current user profile information from data area ALGUSR.\n\n2. Get vehicle master data by chaining on file HSBTSLF1 using vehicle number (FGNR17).\n\n3. Call procedure SRCS to print contracted services information. This retrieves and prints information on various service contracts associated with the vehicle like warranty, maintenance, repair contracts etc. It checks contract status and prints remarks if found.\n\n4. Call procedure SRTERMIN to print upcoming due vehicle appointments from the vehicle monitoring file HSFZTPF. It prints open appointments within 4 weeks into the future or missed appointments within last 6/12 months depending on type. \n\n5. Call procedure SRFZK to print important vehicle comments from the vehicle comment file HSFZKLF1.\n\n6. The procedures SR_WRITE and GET_CS_ID are utilities to write information records and get contract service ids respectively.\n\nRelated files:\n\n- HSBTSLF1 - Vehicle master file\n- HSFZTPF - Vehicle monitoring file with appointments\n- HSFZKLF1 - Vehicle comments file \n- CSCOHF - Contract services header file\n- CSOPTL1 - Contract services options file\n\nThe printed output containing vehicle workshop information is written to file HS06512F.\n\nIn summary, the code prints a shop document containing vehicle service contract details, upcoming appointments, and important comments by retrieving and formatting data from various master files.","file_name":"HS06512.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis code appears to be related to determining the last order number for a workshop manager in some kind of dealership system.\n\nThe main logic is:\n\n1. Open the FISTAM file for input.\n\n2. Read a record (FISTAR) from FISTAM into memory. \n\n3. Move the workshop manager ID (WERKME) into a field in memory (FIS250).\n\n4. Subtract 1 from another field in memory (FIS320).\n\n5. Move the result of the subtraction into the output parameter AUFNRL. This contains the last order number for the workshop manager.\n\n6. Close the FISTAM file.\n\n7. Set on the LR indicator.\n\nSo in summary, this code looks up the last used order number for a given workshop manager by:\n- Opening an order file \n- Reading a record\n- Extracting the workshop manager ID \n- Calculating the last order number by subtracting 1 from another field\n- Returning the last order number \n\nThe FISTAM file appears to be some kind of order file. The workshop manager ID and last order number are stored in fields in the records in this file.\n\nNo database interactions are indicated.\n\nThe only output is the last order number passed back in the AUFNRL parameter.\n\nLet me know if any part of the logic needs further explanation!","file_name":"HS0605.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program appears to be related to displaying blocked customer information in a workshop order management system.\n\nThe key steps are:\n\n1. Initialize variables and open files\n\n- DATEDIT(*YMD) sets date format to YYYYMMDD\n- Opens files FKUDSTAM, FHSKUILF1, FHSBTSPF, FHSBTSLF1 for input \n- Opens file FHS0611D for output\n\n2. Read customer master data (FKUDSTAM)\n\n- Chains to file FKUDSTAM using keys KZLZEN (customer number) and NUMZEN (sequential number)\n- Reads customer name into field HEINAM from file FHSBTSPF\n\n3. Read workshop order header data (FHSKUILF1) \n\n- Chains to file FHSKUILF1 using keys KZLZEN and NUMZEN\n- Reads blocking indicator KUI000\n\n4. Check blocking indicator\n\n- If KUI000 is not blank:\n   - Copy KUI000 to KUI000A\n   - Set indicator SPERRE_JA/SPERRE_NEIN based on blocking code in KUI070\n   - Write blocked customer data to output file FHS0611D\n\n5. Display results\n\n- If any records were written to FHS0611D:\n   - Set indicators to allow screen output\n   - Write output screen FHS0611C1\n   - Write printer output\n\nIn summary, this program reads customer and order data, checks for blocking codes, and writes any blocked customer records to an output file and screen. The focus is on identifying and reporting blocked customers.\n\nFiles used:\n\n- Input\n   - FKUDSTAM - Customer master file\n   - FHSKUILF1 - Workshop order header file \n   - FHSBTSPF - Name file\n- Output\n   - FHS0611D - Output file with blocked customers\n   - FHS0611C1 - Output screen\n\nLet me know if you need any clarification or have additional questions!","file_name":"HS0611.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis program is designed to adjust the productivity of technicians for actual billable hours when a new standard times routine is used. It is called by program HS0650 when BEL01B='03' or '05'.\n\nIt receives the following input parameters:\n- AUFNR: Order number \n- BEREI: Area (SC/SAAB)\n- WETE: Workshop counter\n- SPLITT: Split indicator\n- BEL01B: Transaction type \n\nThe program does the following:\n\n1. Checks if new standard times routine is active based on WKO280 value. If not, exits.\n\n2. Sums the standard times values (hours and amount) for the order from AUFWRZR file. \n   Validates that the totals are > 0.\n\n3. Sums the initially calculated productivities (hours and amount) for each technician from AUFWAR file. \n   Validates that the totals are > 0.\n\n4. Calculates the productivity percentages of each technician based on their share of the total initial hours and amounts.\n\n5. Calculates the share of the total standard times hours and amounts for each technician based on their productivity percentages.\n\n6. Adjusts the productivity statistics for each technician in HSMONPR and MONSTAR files by:\n   - Subtracting initial productivity values \n   - Adding the corresponding standard times values\n   - Based on the transaction type:\n     - BEL01B='03' (Invoice): Subtracts initial values, adds standard times values\n     - BEL01B='05' (Cancellation): Adds initial values, subtracts standard times values\n\nThis achieves the goal of adjusting the productivity values based on actual billable standard times, while retaining the share of each technician.\n\nThe program interacts with the following files:\n- AUFWKO: Order header file\n- AUFWRZ: Order standard times file \n- FISTAM: Date file\n- AUFWAW: Order initial productivity file\n- FMONSTAM: Technician date file\n- HSMONPF: Technician statistics header file\n- MONSTAR: Technician statistics detail file\n\nThe output of the program is the adjusted productivity statistics in HSMONPF and MONSTAR.","file_name":"HS0607.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis RPG program appears to be related to workshop orders and time tracking.\n\nThe main logic flow is:\n\n1. Check if worker hours are recorded for the order (variable EC = '01'):\n   - Read order details from file AUFWAR\n   - If hours exist (AGAMON > 0), set indicator ANTWH = 'J'\n\n2. Check if time stamps exist for the order (variable ZEF = 'J'):\n   - Build order key ABANUM from input parameters\n   - Read time stamp records from file LZABF0\n   - If records exist:\n     - Save start date/time (ABDATE/ABANFZ) \n     - Save end date/time (ABDATE/ABENDZ)\n\n3. Convert industry minutes to normal minutes:\n   - Call subroutine SRTIEF to convert start/end times\n   - Subroutine logic:\n     - Move input time to temp field\n     - Multiply minutes by 60 \n     - Divide seconds by 100 to get minutes\n     - Move result to output field\n\nThe program interacts with these files:\n\n- AUFWAR - Contains order details\n- LZABF0 - Contains time stamp records\n\nIt accepts these input parameters:\n- AUFNR - Order number\n- BEREI - Order section \n- WETE - Order type\n- SPLITT - Order split\n- AUFDAT - Order date\n- ANTWH - Indicator for worker hours\n- ZEFDATA - Time stamp start date\n- ZEFUHRA - Time stamp start time\n- ZEFDATE - Time stamp end date\n- ZEFUHRE - Time stamp end time\n\nAnd sets these output parameters:\n- ANTWH - Indicates if worker hours exist\n- ZEFDATA - Populated if time stamps exist\n- ZEFUHRA - Populated if time stamps exist \n- ZEFDATE - Populated if time stamps exist\n- ZEFUHRE - Populated if time stamps exist\n\nThe overall business purpose seems to be retrieving time details for a workshop order.","file_name":"HS0613.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis code is part of a program named HS06504 which is used for printing work order documents in a workshop management system.\n\nIt receives the following input parameters:\n- §AUFNR (Work Order Number) \n- §BEREI (Work Order Area)\n- §WETE (Work Type)\n- §SPLITT (Work Order Split)\n- §AFLA (Error Flag)\n\nThe main logic is:\n\n1. Load work order details into data structure DS_WKO by selecting from database table AUFWKO based on input parameters. \n\n2. Check if work order split (§SPLITT) is '4' which indicates warranty/guarantee.\n\n3. If warranty, retrieve count of records from database table HSFLAPF where foreign service amount (FLA150) is greater than purchase amount (FLA130). This checks if foreign service has been marked up.\n\n4. If count > 0, it indicates markup was applied on foreign service which violates warranty guidelines.\n\n5. Set error flag §AFLA = 'J' \n\n6. Display error message HS06504W1 to notify that work order cannot be invoiced due to invalid foreign service markup.\n\n7. Call program HS0646 to adjust the invalid foreign service details. Input parameters passed:\n- Work Order ID (concatenated keys) \n- Purchase Order Number \n- Vendor ID\n- Status Flag\n\nIn summary, this program validates foreign services for warranty work orders and prevents invoicing if markup is detected. It calls another program to fix the invalid foreign services.\n\nThe code interacts with two database files:\n- AUFWKO - Work Order Header\n- HSFLAPF - Work Order Foreign Services\n\nAnd calls one other program:\n- HS0646 - Adjust Foreign Services","file_name":"HS06504.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program is designed to format text into fixed length lines. The key steps are:\n\n1. Initialize variables\n\n- TEXTT: Will hold the formatted text \n- TEXTV: Text variable for string manipulation\n- TLEN: Length of input text\n- ZLEN: Length of each line \n- ZVON/ZBIS: Start/end positions for current line\n- FVON/FBIS: Start/end positions for next line\n- SVON/SBIS: Start/end positions for scan overflow\n- PSCAN: Position of space in overflow\n- PZEIL: Position of last space in line\n- INS: Position to insert space\n- INSERT: Flag if space needs insertion\n- IS_FMT: Flag if text is already formatted\n\n2. Check if formatting is needed\n\n- If text length TLEN is less than or equal to line length ZLEN, no formatting is needed\n\n3. Check if text is already formatted\n\n- If text is from formatted screen, skip formatting\n- Just trim text and return line count\n\n4. Start formatting\n\n- Loop through text to build lines\n- Scan each line for last space and overflow\n- If space needed, insert space and shift text\n- Build next line from overflow\n\n5. Trim formatted text  \n\n- Trim each line\n- Update line count\n\n6. Return formatted text and line count\n\nThe program formats the input text into fixed length lines suitable for printing.\n\nKey files used:\n\n- No files are used directly in this program. \n\n- It seems to be called by program HS0651 which may handle report printing.\n\n- So input text is likely passed in from that program. \n\n- Formatted text is returned back to that program for printing.\n\nNo UI interaction in this program.\n\nLet me know if you need any clarification or have additional questions!","file_name":"HS06511.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis code appears to be validating payment guarantee and block indicators for a customer order in a workshop management system.\n\nIt does the following:\n\n1. Retrieves customer master data (KUIPF) and order header data (KUDSTAM)\n\n2. Validates the following business rules:\n\n- Check if payment guarantee indicator (KUI070) is set to 'S' \n\n- Check if payment guarantee valid to date (KUD470) and payment guarantee from date (KUD460) are not blank\n\n- Check if payment guarantee valid to date (KUD470) is less than or equal to today's date\n\n3. If any of the validations fail:\n\n- Call program HS0612W1 to display an error message\n\n- Set on the error indicator (LR)\n\nSo in summary, this code encapsulates business logic to validate payment guarantee data on a customer order, including:\n\n- Fetching relevant data from customer master and order header files\n- Checking if guarantee indicator is set  \n- Validating guarantee date range\n- Displaying error message if validations fail\n\nIt interacts with the following files:\n\n- KUIPF - Customer master file\n- KUDSTAM - Order header file\n\nAnd displays errors via program HS0612W1, which likely contains UI/messaging logic.\n\nThe core purpose is to enforce correct payment guarantee data on customer workshop orders before further processing.","file_name":"HS0612.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\n1. String Conversion Procedures\n\n- toUppercase: Converts a given input string to uppercase using the `%xlate` built-in function.\n\n- toLowercase: Converts a given input string to lowercase using the `%xlate` built-in function. \n\n2. Memory Management Procedures \n\n- allocSpace: Allocates or reallocates memory for a pointer variable based on the given size. Checks if pointer is null, allocates new space if so, else reallocates existing space.\n\n- deallocSpace: Deallocates memory for a given pointer if not null.\n\n3. Work Order Processing\n\n- Reads work order details like customer number, work order number etc from database files. \n\n- Calculates package totals, discount amounts etc and writes them to output files.\n\n- Reads parts data, calculates totals, updates parts inventory files.\n\n- Reads labor data, calculates totals, assigns technicians, updates technician files.\n\n4. Transaction Logging\n\n- Logs parts transactions like issues, returns etc to transaction file with details like date, customer, part no, quantity etc.\n\n5. Date/Time Utilities\n\n- Procedures to retrieve current date and time and format it.\n\nThe code interacts with various database and interface files like work orders, inventory, labor, transactions etc. It contains procedures to perform business functions like work order costing, parts management, labor assignment and logging.","file_name":"HS0606.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nOverall purpose:\n- This program allows maintaining workshop hours and standard times for vehicles. It handles adding/updating technicians' hours, multi-purpose hours, assigning standard times to jobs, applying discounts etc.\n\nKey functions:\n1. Add/update technicians' hours (P001)\n- Allows adding a new technician to the job by entering details like name, hours, billing rate etc. \n- Updates the technician hours data (AUFWAR, HSMONPR, MONSTAR files).\n- Applies wage group based discounts if defined.\n\n2. Add/update multi-purpose hours (P002)  \n- Handles adding new standard time codes and hours under multi-purpose.\n- Saves the standard times in a temporary file (HSRZAPF).\n- Retrieves the descriptions etc. from standard time code files. \n- Updates the multi-purpose hours in AUFWAR file.\n\n3. Assign standard times (P008, P048)\n- Displays list of unassigned standard times.\n- Allows assigning them to technicians.\n- Updates AUFWAR, MONSTAR and HSMONPR files.\n\n4. Edit/delete technician and multi-purpose hours (P004, MONDLT)\n- Marks the records for deletion.\n- Handles deleting hours from AUFWAR and updating MONSTAR, HSMONPR files.\n\n5. Apply discounts:\n- Based on wage groups (HS0095)\n- Special discounts like for daughter companies (SR_WRZ160) \n- EPS discounts (WRZ200/210)\n\n6. Validation and controls:\n- Credit limit check (SR_LIMIT)  \n- Validation for hours entered (PRUEF)\n- Checking if technician exists etc.\n\n7. User interface:\n- Multiple subfile views for hours (SRSFL5)\n- Switching between workshops/technicians and standard times screens (VIEW)\n- Guiding user through screens (SR04)\n\nFiles used:\n- AUFWAR, AUFWAW, AUFWKO etc - Work order files\n- HSMONPR, MONSTAR - Technician master files\n- HSRZIPF, HSRZTPF etc - Standard time master files\n\nSo in summary, it allows maintaining the time and billing related data for jobs, applying discounts, guiding the user through the process and doing necessary validations.","file_name":"HS0608.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nOverview:\n- The code handles campaigns for vehicles/work orders in the Scania workshop system. It allows viewing open campaigns for a vehicle, adding campaigns to a work order, and maintaining campaign details like parts, labor times, texts etc.\n\nMain Procedures:\n\n1. SR_KAM_FZ:\n   - Purpose: Display open campaigns for a vehicle.\n   - Logic:\n     - Read open campaigns for the vehicle from WPCAMR/WPCACR files.\n     - Show campaign number, title and selection option in SFL for user to pick.\n\n2. SR_KAM_AUF: \n   - Purpose: Manage campaigns for a work order.\n   - Logic:  \n     - Read associated campaigns from AUFWKKR file.\n     - Show campaign number and title in SFL for user to select an action like delete/view parts/labor etc.\n     - Allow adding a new campaign from the open campaigns.\n\n3. SR_HINZU:\n   - Purpose: Add a campaign to a work order.\n   - Logic:\n     - Validate campaign details like parts, operations.\n     - Write campaign header, parts, operations to AUFWKKR, AUFWKTR, AUFWRZR files.\n     - Update stock file TEISTAR, write transactions to TRANSPR.\n     - Link campaign to work order in HSKAMPR.\n\n4. SR_LOESCHEN:\n   - Purpose: Delete a campaign from a work order.\n   - Logic:  \n     - Delete campaign parts from AUFWKTR, operations from AUFWRZR.\n     - Delete campaign header from AUFWKKR and unlink from HSKAMPR.\n     - Update parts stock and transactions.\n\nKey Files Used:\n- WPCACR/WPCAMR: Campaign definitions \n- HSKAMPR: Link between campaigns and vehicles/work orders\n- AUFWKKR: Campaign header/details at order level\n- AUFWKTR: Campaign parts at order level \n- AUFWRZR: Campaign operations at order level\n- TEISTAR: Parts stock file\n- TRANSPR: Parts transactions\n\nThe code handles core campaign processes in a Scania workshop system involving vehicles, work orders and links to the central campaign definitions.","file_name":"HS06090.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program appears to be related to managing workshop orders, campaigns, and timesheets. The key functions include:\n\n1. Processing workshop orders (AUFWKR)\n- Read order details like customer, date, etc\n- Calculate billing rate based on order type \n- Add records to output files/subfiles for display\n\n2. Managing campaigns (HSKAMPR, S7F001)\n- Check for open campaigns for a workshop order \n- Allow adding/deleting campaigns \n\n3. Managing timesheet data (AUFWKLR, AUFWKTR, HSMONPR)\n- Read and display timesheet records per order \n- Allow assigning technicians and hours to campaigns\n- Validate hours entered against technician capacity\n- Update technician capacity totals\n- Calculate billing amounts\n\n4. Updating inventory (TEISTAR, TRANSPR)\n- When parts used on a campaign, update inventory transactions\n\n5. Reporting \n- Multiple subfile displays for orders, campaigns, timesheets\n- Allow updating of campaign details and technician notes\n\nThe code interacts with these files:\n- FISTAM: Customer master file\n- AUFWKR/AUFWKLR/AUFWKTR: Order/timesheet/parts usage details\n- HSKAMPR: Campaign master file \n- HSMONPR: Technician master file\n- TEISTAR: Inventory master file\n- TRANSPR: Inventory transactions file\n\nThe subfile displays and file I/O indicate this is an interactive green-screen application, likely for use in a workshop office.\n\nPlease let me know if any additional information on the business logic would be helpful!","file_name":"HS0609.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- The code is for an application called SDPS-ZENTRAL used in the workshop area of SCANIA DEUTSCHLAND.  \n- It allows changing the parts prices and discounts on stored workshop orders.\n- Changes are only possible if the order status (WKO300) is blank, 00 or 02 (KV).\n\nMain logic:\n1. Check user authority to change prices/discounts based on user ID.\n2. Initialize variables, open files, clear screens.\n3. Retrieve open workshop orders and display in subfile.\n4. Allow changing part prices, discounts, positions, descriptions on orders via subfile.\n5. Protect part descriptions for SDE/subsidiaries. \n6. Protect positions for EPS orders.\n7. Update prices/discounts in database if changed in subfile.\n8. Write changed order data back to database.\n9. Log changes made to orders. \n\nInterfaces:\n- Database files:\n  - AUFWKO - Workshop orders\n  - AUFWTE - Parts on workshop orders\n  - HSAKTLF1 - Change log\n  - HSEPKPF - User IDs\n  - Other pricing/discount files\n  \n- Screens:\n  - HS063501 - Main screen \n  - HS0635C1 - Parts subfile\n\nThe code interacts with the database to retrieve, update and log changes to workshop order pricing data based on user input on the screens. It contains authorization checks, file I/O, calculations, screen handling and logging. The core tasks are order price/discount updates and protecting key data fields.","file_name":"HS0635.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code appears to perform validation on sales order dimensions entered by a user when creating a sales order in the SDPS-2000 system. \n\nIt checks the following:\n\n1. Branch (BRANCH)\n- Ensure a branch is entered\n- Validate the entered branch code against a branch master data table (AXAXTLF2)\n\n2. Account (KTO) \n- Ensure an account is entered\n- Validate the account against a split account master data table (HSAXIF) to ensure it is allowed for the sales order split\n\n3. Cost Center (KST)\n- Ensure a cost center is entered  \n- Validate cost center against master data (HSAXIF)\n- Validate combination of account + cost center against account/cost center split mapping table (HSAXDL1) \n\n4. Individual Number (KTR)\n- Validate based on whether system is configured to require (CTLHS6 indicator)\n- Check for blanks if required\n\n5. Product Code (PRDCODE)\n- Validate based on whether system is configured to require (AXD_PRD indicator) \n- If entered, validate against product master data table (AXDIMPF)\n\n6. Special Code (SPZCODE)\n- Validate based on whether system is configured to require (AXD_SPEC indicator)\n- Special case to allow blank for a specific account + cost center + split + special code combination\n\nIf any validation fails, a return code (FEHLCODE) is set that can be used by the calling program to determine which dimension validation failed.\n\nThis program validates sales order dimensions against master data to ensure splits are mapped to valid account/cost center combinations. It is likely called when a sales order is created or changed in SDPS-2000.\n\nThe code interacts with these files:\n- AXAXTPF: Branch file\n- AXAXTLF2: Branch/Plant file\n- HSAXIF: Split mapping file\n- HSAXDL1: Account/Cost Center split mapping file \n- AXDIMPF: Product master data file\n- CTLHS6: Configuration/Control file","file_name":"HS0618.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis code appears to be related to retrieving credit limit history information from an Axapta system.\n\nThe main logic is:\n\n1. It defines some date variables to represent a date range:\n\n- DAT_VON - Start date\n- DAT_BIS - End date \n\n2. It checks if start and end date parameters were passed:\n\n- If yes, it sets DAT_VON and DAT_BIS to the passed parameter values\n- If no, it defaults DAT_VON to '2010-01-01' and DAT_BIS to yesterday's date\n\n3. It converts the start and end dates to character strings and stores them in DATVON and DATBIS.\n\n4. It calls another program 'HS06154HC', passing the start and end dates.\n\nSo in summary, this code allows retrieving credit limit history for a date range, defaulting to all history from 2010-01-01 if no parameters are passed.\n\nThe called program 'HS06154HC' likely contains the main business logic for querying the history data.\n\nSome other notes:\n\n- This appears to be an RPG program meant to run in an IBM i environment.\n\n- It uses some RPG-specific features like data structures, EVAL, CALL, etc.\n\n- There are no obvious database or UI interactions in this code snippet.\n\n- The comments indicate it is part of an application called SDPS-ZENTRAL for a company called SCANIA DEUTSCHLAND.\n\nPlease let me know if you need any clarification or have additional questions! I'm happy to explain further.","file_name":"HS06154HS.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverall Purpose:\n- This RPG program handles credit limit exceptions and approvals for orders. It allows managing credit limit exceptions and approvals for a customer order.\n\nKey Functions:\n1. Get order details \n   - Based on input parameters, fetch order details like order number, order date, customer number, names, etc.\n   - Details are fetched from order files AUFWKO/AUFTKO based on input for sales order or delivery order.\n\n2. Get credit limit info\n   - Fetch credit limit info for the customer using customer number.\n   - Details like credit limit, outstanding orders, available credit limit are retrieved.\n   - Exception details like exception id and text are also fetched if exists.\n\n3. Check user authorities\n   - Based on transaction type, validate if user has authority to maintain credit limit exceptions or approvals.\n   - Different authorization checks done for sales orders and delivery orders.\n\n4. Display order and customer details\n   - Order details, customer details, credit limit info is formatted and displayed on screen.\n\n5. Allow entry of exception or approval\n   - User can enter a new exception id and text to override credit limit.\n   - User can also enter a new credit limit approval amount.\n\n6. Confirm and update exception \n   - Added logic to confirm before updating a new credit limit exception.\n   - Exception id and text gets updated on order file if confirmed.\n\n7. Update credit limit approval\n   - Updated credit limit approval amount gets stored in order file. \n\n8. Log changes\n   - Any changes to exception or approval are logged with user details for audit purpose.\n\n9. Email notification\n   - On change in approval amount, email notification is sent out.\n\nRelated files:\n- AUFWKO/AUFTKO - Order files\n- HSKLPF - Credit limit approval file\n- HSKLAF - Credit limit exception file \n- HSKUIPF - Customer master file\n- HSKUDSTAM - Customer statistics file\n\nLet me know if you need any clarification or have additional questions!","file_name":"HS06153.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverall Program Functionality:\n- Allows changing various details of an existing work order, including split, invoice recipient, discount code.\n- Validates changes and updates work order header record (AUFWKR). \n- Propagates changes to related detail records like work steps (AUFWAR), parts (AUFWTR), etc.\n- Records change history for auditing.\n\nSplit Change:\n- Input required: Work order number, Area, From Split, To Split\n- Validates work order exists and new split is allowed based on contract.\n- Validates no order blocks exist for new split and customer.\n- Updates work order header with new split.\n- Copies over work step and part records from old to new split.\n- Rates new split based on customer/contract. \n- Records change history.\n\nInvoice Recipient Change: \n- Input required: Work order number, Area, Split, New Customer Number\n- Validates work order exists and new customer is valid.\n- Validates split alignment between existing order and new customer.\n- Updates work order header with new customer details.\n- Rerates order based on new customer/contract.\n- Records change history.\n\nDiscount Code Change:\n- Input required: Work order number, Area, Split, New Discount Code\n- Validates work order exists and new code is valid.\n- Updates work order header and rerates all work steps and parts using new code. \n- Records change history.\n\nThe program interacts with these files:\n- AUFWKO: Work Order Header\n- AUFWAR: Work Steps\n- AUFWTR: Parts\n- AUFWKR: Work Order Contract\n- KUDSTAM: Customer Master\n- HSAKTLF1: Change History\n\nAdditional functionality exists for:\n- Viewing open orders\n- Splitting based on packages\n- Updating technician statistics\n- Validation against AXAPTA","file_name":"HS0640.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code implements functionality to generate electronic invoices in XRechnung XML format. \n\nKey aspects:\n\n1. It can generate invoices from different sources:\n- Service invoices (SPAS) based on data from ITPINVH table\n- Repair shop invoices (WT) based on data from HSAHKPF/HSAHTPF/HSAHWPF/HSAHPPF tables  \n- Manual invoices based on data from AXMRKPF table\n\n2. It retrieves all relevant data like customer info, addresses, payment terms etc. from various tables.\n\n3. It dynamically builds the XRechnung XML structure and populates it with the invoice details.\n\n4. The XML generation involves:\n- Setting up the XML header with metadata like invoice date, type etc.\n- Adding billing and shipping address details under Party nodes\n- Adding invoice lines for parts, labor etc. under InvoiceLine nodes  \n- Calculating totals like line amounts, taxes etc. under TaxTotal and LegalMonetaryTotal nodes\n\n5. The generated XML file is then exported and optionally sent to the customer.\n\n6. There is also dialog functionality to enter invoice details manually.\n\n7. Additional procedures handle utility tasks like data retrieval, string formatting, date calculations etc.\n\nSo in summary, it is an invoice generation application focused on creating XRechnung compliant XMLs from various data sources and business contexts. The core functionality is the flexible and dynamic construction of the XML structure using RPG code.\n\nRelevant files:\n- ITPINVH - Service invoice header\n- HSAHKPF - Repair shop invoice header \n- AXMRKPF - Manual invoice header\n- BSPCUST - Customer master data\n- FISTAM - Biller master data\n\nThe application interacts with these files and DB2 tables to generate the end XML document.","file_name":"HS0654.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- The code implements credit limit approval functionality for orders in an ERP system. It allows approving credit limit extensions and removing exceptions for orders.\n\nMain functions:\n1. Check option validity:\n   - Validate input parameters like branch, customer etc.\n   - Check user authorization.\n   - Verify valid order.\n\n2. Extend credit limit:\n   - Get order details like current limit. \n   - Allow user to enter new extended limit.\n   - Update limit in order.\n   - Write change log.\n\n3. Remove exception:\n   - Get order details.\n   - Clear exception fields in order.\n   - Write change log. \n\n4. Display order information:\n   - Show 2 screens - change logs and order details.\n   - Allow changing screens.\n   - Apply filters set by user.\n\nKey objects:\n- KUDSTAR - Customer master file\n- AUFWKO - Workshop order file \n- AUFTKO - Counter order file\n- HSKLPR - Change log file\n\nThe code interacts with these files to retrieve order details, update limits, and log changes.\n\nIt contains procedures for core functions like option checking, order validation, writing logs etc. These are called from the main logic.\n\nThere is also code to handle user interactions - screens, filters etc.\n\nIn summary, the RPG code encapsulates the key business logic to manage credit limit exceptions and extensions for orders in this ERP system. The main steps are validating input, retrieving order details, updating limits, logging changes and interacting with the user.","file_name":"HS06152.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis appears to be an RPG program for displaying workshop orders. The key functions include:\n\n1. Displaying workshop orders\n- Allows displaying all workshop orders, only open orders, or orders for the current date\n- Displays details like order number, customer number, vehicle number, status etc in a subfile\n- Handles pagination and navigation of the subfile\n\n2. Lookup by customer number\n- Allows searching for orders by customer number using a matchcode\n- Displays matching orders in a subfile\n- Allows selecting a customer to filter orders\n\n3. Lookup by vehicle number  \n- Allows searching for orders by vehicle/chassis number\n- Displays matching orders in a subfile\n- Allows selecting a vehicle number to filter orders\n\n4. Lookup by repair code\n- Allows searching for orders by repair code \n- Displays matching orders in a subfile\n- Allows selecting a repair code to filter orders\n\n5. Display order details\n- Shows additional details for a selected order in subfiles\n- Displays order header, parts, labor, packages etc.\n- Calculates net values for parts and labor\n\n6. Integration with other programs/files\n- Reads data from workshop order (AUFWKR), customer (KUDSTAR), vehicle (HSFAILR), and other files\n- Calls other programs like HS0062C to retrieve archived data\n\nThe code interacts with display files like HS068000 for user interface. It handles subfile operations for output display. There is also some logic for handling pricing and totals.\n\nOverall, this program allows users to search, view and analyze workshop orders in an interactive manner by integrating with other programs and data files in the system. The business logic centers around order inquiry, lookup and display functions.","file_name":"HS0680.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\n**Overview:**\n\nThe code calculates the total open order value (gross) for workshop and counter orders to check against the credit limit. It considers only open orders, skips certain order types, and excludes cancelled orders.\n\n**Key steps:**\n\n1. Initialize total open order value (KLO_OAUF) to 0 \n\n2. Loop through workshop orders (AUFWKLRC file)\n- Read order details \n- Skip if order status not open \n- Skip certain order types (internal, service, complaints)\n- Skip cancelled orders\n- Skip orders not yet invoiced \n- Skip orders excluded from credit limit check\n- Calculate order net value\n  - Add value of small parts/materials if applicable\n  - Add value of labor hours and operations\n  - Add value of external services \n  - Add value of parts\n  - Add value of kits\n- Write order net value to temp file (HSKLOR)\n- Calculate order gross value: multiply net value by VAT factor if VAT applicable\n- Add order gross value to total open order value (KLO_OAUF)\n\n3. Repeat process for counter orders (AUFTKLR1 file) \n\n4. Write total open order value (KLO_OAUF) to temp file (HSKLOR) if > 0\n\n**Related files:**\n\n- AUFWKLRC - Workshop orders file\n- AUFTKLR1 - Counter orders file \n- RE1SULR2 - Invoiced orders file\n- HSKLAR - Orders excluded from credit limit file\n- AUFWAR - Order labor details file  \n- HSFLALR1 - Order external services file\n- AUFWTR - Order parts file\n- AUFTTR - Order parts file\n- AUFPKOR - Order kits file\n- HSKLOR - Temp file for open order values\n\nIn summary, the code loops through the order files, calculates net and gross order values, excludes certain order types, and sums the total open order value across workshop and counter to check against the customer credit limit. The logic filters out non-relevant orders and writes the result to a temporary file.","file_name":"HS06151.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code appears to be interacting with a database file called HSKLPR. Based on the comments, this seems to be a credit limit file. \n\nThe main logic is:\n\n1. Get the current date into DAT_AKT.\n\n2. Convert DAT_AKT to character format and store in DATAKT.\n\n3. Read the HSKLPR file sequentially starting from the high end (*HIVAL).\n\n4. Loop while the record format is 80 bytes (*IN80).\n\n5. Inside the loop:\n\n- Check if the date field KLP_DATUM is not equal to DATAKT. This seems to avoid collisions/duplicates.\n\n- Check if the warehouse field KLP_WHT is blank. The comment indicates this is to only process calculation records. \n\n- If both checks pass, delete the HSKLPR record.\n\n6. Read the next record and loop back. \n\n7. After looping through the file, set the last record read lock on (SETON LR).\n\nIn summary, this code loops through a credit limit file and deletes records based on date and warehouse criteria.\n\nThe HSKLPR file appears to be a physical database file. There is no explicit UI or other program interaction specified in the code.","file_name":"HS06155.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code is for printing a repair order document.\n\nDatabase Files:\n- HSAHWPF - Header work order file\n- HSAHTPF - Header parts file \n- HSAHPPF - Header package file\n- HSBTSLF1 - Form file\n- HSFZTLF4 - Inspection deadline file\n- HSLAEPF - Country file\n- HSKUIPF - Customer master file  \n- KUDSTAM - Dealer master file\n\n1. Main logic:\n- Read input parameters - repair order details like order number, date etc\n- Open output spooled file for printing\n- Call procedure to print document header \n- Call procedure to print order lines\n- Call procedure to print parts\n- Call procedure to print packages\n- Close output file\n\n2. Print document header:\n- Initialize printer page count\n- Get customer details by chaining on order header record\n- Build customer address strings\n- Get order date details \n- Get inspection deadline details by chaining\n- Get UID/tax ID details by chaining to customer and dealer master records\n- Write header details to output file  \n\n3. Print order lines:\n- Declare cursor on order lines file\n- Fetch order line records \n- Check for new position number \n- If new position, print position total for previous position\n- Print line details for each order line record fetched\n\n4. Print parts:\n- Declare cursor on parts file\n- Fetch part records for current position\n- Print each part record details\n\n5. Print packages:\n- Declare cursor on packages file \n- Fetch package records for current position\n- Print each package record details\n\n6. Utility logic:\n- Format customer address strings\n- Increment line counter and check page overflow\n- Print document header on new page\n\nThe code handles printing of the work order document by retrieving and formatting data from the related database files.","file_name":"HS0652.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverall Program Logic:\n- The program allows managing purchase orders and related services/items. It interfaces with AXAPTA for some validations.\n\nMain Procedures:\n\n1. CheckAuthority: Checks if the user has authority to access the program functions.\n\n2. SFLLOE: Clears the display files. \n\n3. SFLFUE: Populates the display files with data from database files for initial display. Filters data based on date range.\n\n4. VIEW_C1: Writes service description details to display file in C1 format. \n\n5. VIEW_C3: Writes purchase order header details to display file in C3 format.\n\n6. AUFKUD: Retrieves purchase order and customer details for a service. Checks if purchase order is open, invoiced or cancelled.\n\n7. STATUS_FL: Determines service line item status based on conditions.\n\n8. STORNO_FL: Performs cancelation of service line item.\n\n9. AUFRECH: Displays purchase order or invoice details. \n\n10. BESNEU: Allows creation of new purchase order or editing existing one. Retrieves supplier details. Interfaces with AXAPTA for validations.\n\n11. LEISNEU: Allows creation of new service line item. Interfaces with AXAPTA for credit limit check.\n\n12. ANSCHRIFT: Builds address blocks for supplier and delivery addresses.\n\n13. SR_EINKAUF: Builds text blocks for terms and conditions.\n\n14. DRUCKBS: Prints purchase order.\n\n15. TXTZEILEN: Allows maintaining number of text lines per service.\n\n16. DETAILS: Displays and allows editing service line details like pricing and invoice details.\n\n17. RWCHEK: Checks if service is R&W split type. \n\n18. STATUS_KL: Determines service and purchase order status text. \n\n19. WRITE_FLB: Writes new or updated purchase order to file.\n\n20. WRITE_FLA: Writes new or updated service line item to file.\n\n21. UPDATE_FLB: Updates existing purchase order header record.\n\n22. PLAUSI: Performs various validity checks.\n\n23. PLAUSI_AXA: Does additional validity checks by interfacing with AXAPTA. \n\n24. BEDIENER: Allows input prompts and lookups via F4 function key.\n\n25. SR_SPERRE_L: Checks for supplier blocking.\n\n\nDatabase Files Used:\n\n- HSBTSLF1: Company file\n- AXAXTPF: AXAPTA company file\n- AXAXTLF2: AXAPTA company branch file \n- FAXDIMPF: AXAPTA dimensions file\n- HSBNDDIR: Binding directory\n- HSFLBPF: Purchase order file\n- HSFLAPF: Purchase order line file \n- HSFLTPF: Purchase order line text file\n- HSFLLLF1: Service codes file\n- HSANSPF: Consultants file\n- LIFSTAM: Supplier master file \n- FHSLAEPF: Country codes file\n- FKUDSTAM: Customer master file\n- FHSKUIPF: Customer alternate delivery addresses\n- FHSNRKPF: Purchase order number range file\n- FHSAHKLF3: Invoice file\n- FAUFWKO: Shop order file \n- FRWVRILF5: R&W contracts file\n- FFLBEST: Print file purchase order\n- HS0646S1: Display file 1 \n- HS0646S3: Display file 3\n\nThe program contains extensive validation logic, interactions with AXAPTA as well as printing functions related to managing purchase orders and related services/items.","file_name":"HS0646.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nOverall purpose: This RPG program interacts with the Service Delivery Planning System (SDPS) to retrieve and display draft vehicle work orders for selection and further processing in SDPS.\n\nKey steps:\n\n1. Initialize\n   - Set date format to ISO\n   - Get site ID (kzlb) and description (kzlf)\n   - Define temporary storage for work order data (#sel1, Rec_#d) \n   \n2. Get draft work orders\n   - Build SQL statement to select draft work orders (#sel1)\n   - Execute SQL to populate work order details (Rec_#d)\n   \n3. Display work orders\n   - Write work order details from SQL to display file (HS06009S1)\n   - Allow searching/filtering records\n   - Page through results\n   \n4. Select work order\n   - When option 1 chosen, pass work order ID and other details to SDPS using parameter list\n   - This triggers subsequent processing of selected work order in SDPS\n   \n5. Additional logic\n   - Customer name lookup using multiple files (HSFAIPF, FARSTAM, HSKUIPF, KUDSTAM)\n   - Search logic:\n      - Convert input to uppercase\n      - Remove spaces\n      - Match against multiple fields\n   \n\nKey files:\n\nInput: \n- WOPWOF - Work order file\n- HSFAIPF - Partner file\n- FARSTAM - Partner role file \n- HSKUIPF - Customer file\n- KUDSTAM - Customer role file\n\nOutput:\n- HS06009S1 - Display file for work order selection\n- DD§PWO - Parameter list passed to SDPS\n\nThe program facilitates work order selection from Digital Dealer and transfer to SDPS for further processing. Key steps include SQL retrieval of open work orders, interactive search/select, and passing of selected order details to SDPS. Additional logic handles lookup of customer data from various source files.","file_name":"HS06009.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code is for processing work orders in a vehicle workshop management system. It has the following key functions:\n\n1. Validate work order appointment or vehicle inspection report:\n\n- Check if work order already exists for the appointment ID or inspection report ID. Return error if it does.\n\n- Retrieve appointment/inspection details like customer number, vehicle ID, appointment times etc. Validate required details are present.\n\n- Validate dealer location code. \n\n- Check if customer is valid and not blocked.\n\n- Validate vehicle ID exists in vehicle master data.\n\n- Determine work order type, workshop, split etc based on rules and master data validation. \n\n- Generate next work order number from counter file.\n\n- Set work order header details like dealer, dates, vehicle info, customer info etc.\n\n2. Create work order text (lines 00-99):\n\n- Add pre-defined text lines based on work order type. E.g. for vehicle inspection, add header text. \n\n- Copy over appointment description text (if available) to work order text lines.\n\n3. Link packages:\n\n- Based on work order type rules, link any relevant packages to the work order.\n\n4. Update FTM (vehicle feature configuration): \n\n- When work order is created for an appointment, update the FTM modules status to link them to the work order number.\n\n5. Update appointment or inspection report with generated work order number.\n\nThe code interacts with the following files:\n\n- Work order header (AUFWKO) \n\n- Work order text (AUFWAW)\n\n- Appointment calendar (HSWKTF) \n\n- Vehicle inspection reports (CDPCHF)\n\n- Vehicle feature configuration (HSFTMR4)\n\n- Packages (HSPAKF) \n\n- Dealer master data (VKSSPL4, HSBTSLF1)\n\n- Customer master data (HSKUIPF, KUDSTAM) \n\n- Vehicle master data (HSFAIPF, FARSTAM)\n\n- Pricing master data (HSRAZPF)\n\n- Number ranges (FISTAR)\n\n- Work order type rules (AUFSTAR)\n\nIn summary, the RPG code handles validation, master data lookups, business logic for work order creation and updating related data files for the vehicle workshop management process. The key steps are data validation, determining work order type and details, creating work order document, and updating vehicle data with work order reference.","file_name":"HS06008.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- This program generates an XML e-invoice file for a given invoice number based on data from various database files.\n\nMain functions:\n1. Initialization\n   - Get invoice number and date from input parameters or by looking up based on user id.\n   - Determine invoice type based on invoice number prefix.\n   - Initialize filename, timestamp etc.\n\n2. Get invoice header details\n   - Get invoice header record based on invoice number/date.\n   - Get customer data from invoice header.\n   - Determine document type (Invoice/Credit Memo).\n   - Get contact and address info for biller based on dealer id.\n\n3. Get invoice line details\n   - For workshop and counter invoices, get parts, labor, packages from related database files. \n   - For manual invoices, get details from invoice item file.\n\n4. Generate XML \n   - Output XML header with invoice metadata.\n   - Add invoice recipient, biller, line items, totals etc. as XML elements.\n\n5. Write payment info\n   - If blank direct debit, output bank details for biller.\n   - If direct debit info present, add direct debit XML element.\n\n6. Export XML file\n\nDatabase interactions:\n- Read invoice header (AHK) and related detail records (AHT, AHW, AHP)\n- Read manual invoice header (MRK) and detail (MRP) records  \n- Read dealer contact info (ANS)\n- Read customer direct debit preference (KUI) \n- Write generated XML to IFS file\n\nUI interactions:\n- Prompt for missing invoice number if not passed as parameter\n\nThe program generates an e-invoice XML file by extracting data from the database based on a given invoice number. The core logic involves assembling XML elements by pulling data from various sources like invoice header, line items, customer info etc.","file_name":"HS0653.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis RPG program appears to be for processing active work orders in a workshop management system.\n\nMain logic:\n\n1. Call program HS0013 to check for inactive jobs and automatically delete them from the HSAKTPF file. This keeps only active jobs.\n\n2. Clear the subfile (SFL) S1. \n\n3. Read records from the HSAKTLR1 file into the SFL S1 to display active work orders.\n   - The key fields for HSAKTLR1 are AKT01X and AKT02X.\n   - Loop through HSAKTLR1 records with AKT013='1' (active flag). \n   - Move work order number (AKT010) to AKT01X and work order description (AKT020) to AKT02X.\n   - Write records to the SFL S1.\n\n4. If no records found, add a blank record to SFL S1 indicating 'NO ENTRIES'.\n\n5. Display the SFL S1 subfile on the screen.\n\n6. Allow option to refresh subfile or exit program based on user input.\n\nFiles used:\n\n- HSAKTLF1 - Main file for active work orders\n- HSAKTLR1 - Read format of HSAKTLF1 for subfile\n- HS0690S1 - Subfile for display (SFL)\n\nAdditional details:\n\n- Program is designed to run interactively on a workstation.\n- Allows viewing and working with active workshop work orders.\n- Appears to be part of an ERP or workshop management system.\n- Includes header comments indicating it is for SCANIA Deutschland.\n\nIn summary, the key business logic revolves around displaying active work orders in a subfile for a workshop management system. Let me know if any part needs further explanation or clarification.","file_name":"HS0690.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\n**Overview:**\nThis RPG program generates a credit limit report by reading data from multiple files and writing the report to a printer file.\n\n**Input Files:**\n- HSKLPR: Contains credit limit approval (KLF) and exception (KLA) records\n- HSKUIPR: Contains customer master data \n- KUDSTAR: Customer master file\n- HTKSHR1: Contains trigger history records for credit limit changes\n\n**Output File:** \n- PRT6154P: Printer file for credit limit report \n\n**Main logic:**\n\n1. Initialize report parameters based on input (date range, filter values etc)\n\n2. Call SR_KLP to read KLF and KLA records from HSKLPR and write qualifying records to temp file HS06154PAR\n\n3. Call SR_KUD to read customer master records, retrieve credit limit change history using SR_TRG and write records to HS06154PAR\n\n4. Write page header with report dates \n\n5. Read HS06154PAR and print KLF records \n\n6. Read HS06154PAR and print KLA records\n\n7. Read HS06154PAR and print credit limit change records\n\n8. Print message if no records selected\n\n**Subroutines:**\n\nSR_KLP:\n- Reads HSKLPR in reverse date order \n- Writes KLF/KLA records within date range and optional filter value to HS06154PAR\n\nSR_KUD:\n- Reads customer master records \n- Calls SR_TRG to retrieve credit limit history\n- Writes records to HS06154PAR\n\nSR_TRG:\n- Gets credit limit change history from HTKSHR1 within report date range\n- Writes records with old and new limit to HS06154PAR\n\n**Files and Interactions:**\n\n- **Input Files:**\n    - HSKLPR - Contains credit limit approval and exception records\n    - HSKUIPR - Customer master file\n    - KUDSTAR - Customer master file\n    - HTKSHR1 - Trigger history file for credit limit changes\n\n- **Output File:**\n    - PRT6154P - Printer file for report output \n\n- **Database Interactions:**\n    - none\n\n- **Other Interactions:** \n    - Calls to built-in RPG functions for date conversions, character manipulation etc\n\n- **User Interface:**\n    - Report output is printed, no other UI interaction\n\nSo in summary, this RPG program generates a credit limit report by extracting data from various input files, processing it, and outputting a report with credit limit approvals, exceptions and changes. The core logic revolves around reading the input files, filtering and processing records, and generating the final report output.","file_name":"HS06154.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nOverall Purpose:\n- This RPG program handles automatic credit limit setting for new vehicle sales (NFZ) customers and related notifications.\n\nKey Procedures:\n\n1. PR_NfzKud:\n- Purpose: Selects NFZ customers from the sales module based on certain criteria.  \n- Logic: \n  - Selects distinct customer and order numbers from sales order header/lines joins with customer/order org, credit limit header/lines and customer master files.\n  - Filters for country, order date within last N days, order status (50=order placed), payment term (B=cash payment).\n  - Result set contains distinct NFZ customers.\n\n2. PR_Crefo:  \n- Purpose: Retrieves credit agency data for the customer and checks for issues preventing automatic credit limit.\n- Logic:\n  - Checks if customer has Credo no. \n  - Retrieves monitoring, credit index, credit score, company name from Credo file for customer.\n  - Sets flags if data is missing or score too high to prevent automatic limit.\n  - Checks if Credo company name matches SDPS company name.\n  \n3. PR_Limit:\n- Purpose: Sets the automatic credit limit amount based on criteria.\n- Logic:\n  - Sets credit limit amount to 4000.\n  - Updates credit limit flag and risk class on customer.\n  - Performs credit limit consolidation for SDE.\n  - Documents credit limit changes.\n  \n4. PR_MailFVD:\n- Purpose: Sends email notification to credit dept. if no automatic limit set. \n- Logic:\n  - Builds email to notify credit dept. of issues found preventing automatic limit.\n  - Email includes customer/order details, reason code based on missing data flags.\n  \nRelated files:\n- Database files:\n  - VKVSPPF - Sales order header\n  - VKVSAPF - Sales order line\n  - HSKUIPF - Credit limit header \n  - KUDSTAM - Customer master\n  - AXKLKF - Credit limit changes\n  - HSKLPF - Credit limit change log\n- External files:\n  - FHSKUIPF - Credit limit header\n  - FKUDSTAM - Customer master \n  - FAXKLKF - Credit limit changes\n  - FHSKLPF - Credit limit change log\n- Other:\n  - Email notification via SNDEMLF\n\nSo in summary, it handles the entire process from retrieving NFZ customers, validating credit data, setting limits, and generating notifications for missing limit info.","file_name":"HS06156.txt"},

{"logic":"Here are the key points extracted from the RPG code provided:\n\n1. This program is for managing external services (Fremdleistungen) for the workshop. It allows capturing, displaying, printing, and invoicing external services.\n\n2. An external service can be ordered at full tax rate or reduced tax rate. Mixed tax rate orders are not allowed. \n\n3. An external service order can have 3 statuses:\n   - Blank = Order placed with supplier\n   - 1 = Released for invoicing to customer\n   - 2 = Not yet invoiced to customer and cancelled. Data is retained.\n\n4. The program allows searching for external services based on various criteria like vehicle number, order number, order date etc.\n\n5. For a new external service order:\n   - The supplier master data is selected first\n   - Required details like customer order no, item text, prices etc. are entered\n   - System generates an external service order number\n   - The order can be printed\n   - The order is saved in the external service header (HSFLKPF) and item (HSFLPPF) files\n   - The status is updated in customer order header file (AUFWKO)\n   \n6. To invoice an external service:\n   - The status is changed to 1 in HSFLKPF file\n   - The counters are updated in AUFWKO file\n   - The price is moved to the WAW file\n   \n7. To cancel an external service:\n   - The status is changed to 2 in HSFLKPF\n   - Corresponding entries in WAW file are deleted\n   - Counters in AUFWKO are decremented\n   \n8. The program interacts with the following files:\n   - HSFLKPF - External service header file\n   - HSFLPPF - External service item file \n   - AUFWKO - Customer order header file\n   - AUFWAW - Customer order item file\n   - FISTAM - System settings file\n   - AGASTAM - Work order file\n   \nIn summary, the key functionality includes managing the entire lifecycle of an external service order - from creation to invoicing or cancellation. The status and counts are maintained across multiple files for consistency.","file_name":"HS0645.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code contains several procedures, each serving a specific purpose:\n\n1. Process invoice/credit note document\n   - Read order header (AUFWKO) and item details (AUFWAW, AUFWTE etc)\n   - Determine document type (invoice, credit note etc) and split\n   - Calculate totals like net amount, VAT etc.\n   - Print invoice/credit note with header, item details, totals\n   - Generate PDF and/or print document\n   - Email PDF based on customer email address\n   - Archive document\n\n2. Print job descriptions (AUFJOB)\n   - Read job header (job alias) and details\n   - Print job descriptions under separate item positions\n\n3. Determine VAT portion (SCAS)\n   - Read SCAS invoice header (HMSCSCPR) \n   - Read SCAS invoice lines with VAT details (SCAXOPR)\n   - Calculate VAT portion\n   - Consider reversal on credit notes\n   - Validate VAT percentage \n   - Add up applicable VAT amounts\n\n4. Lookup customer master data (KUDSTAM)\n   - Get customer name, address etc.\n   - Determine country, VAT ID\n   - Get email address for PDF sending\n\n5. Lookup text modules (TEXSTAR)\n   - Retrieve text lines for headers, footers etc. \n   - Format text lines to defined length\n\n6. Lookup campaigns (AUFWKKR)\n   - Retrieve campaign details \n   - Print as information on invoice\n\n7. Lookup appointments (HSFZTLR4)\n   - Get upcoming appointments of specific types\n   - Print on invoice\n   \n8. Lookup vehicle master data (FARSTLR4)\n   - Get phone numbers of vehicles\n   - Print on invoice\n   \n9. Direct debit details (AX1230)\n   - Provide invoice data\n   - Retrieve direct debit details like date, mandate reference etc.\n   - Print direct debit notice on invoice\n\n10. Tyre label data (HS03102)\n    - Pass invoice data \n    - Lookup tyre label details\n    - Print on invoice\n    \n11. Control invoice output\n    - Check if email PDF, print or both\n    - Consider batch/dialog mode\n    - Handle different document types\n    - Set PDF subject, recipient etc.\n\nThe code interacts with these files:\n\n- Work order files like AUFWKO, AUFWAW\n- Master data files like KUDSTAM, TEXSTAR  \n- EDI files like SCAS EDI invoice data\n- Appointment data HSFZTLR4\n- Vehicle data FARSTLR4 \n- Campaign data AUFWKKR\n- Tyre label data HS03102F\n- Direct debit data AX1230\n- Output control data like CTLHS7, email addresses etc.\n\nIt generates output in these forms:\n\n- Printed invoice/credit note\n- Email with PDF invoice/credit note attached\n- Direct debit notice printed on invoice\n- Archive copy of invoice/credit note\n\nThe business logic handles different document types like invoice, credit note, proforma etc. It also supports VAT handling for domestic, EU and non-EU transactions.","file_name":"HS0651.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code implements functionality related to credit limit monitoring for customers.\n\nMain functions:\n\n1. Load customer credit limit data into a display file (HS06157D) for interactive processing. Customer data is read from file CDKLMF.\n\n2. Allow adding, changing and deleting customer records in CDKLMF through the display file.\n\n3. Perform automatic credit limit monitoring by calling program HS0615. Results are written to HSKLPF. \n\n4. Automatically send emails to a specified address when credit limit status changes or on a scheduled basis. Emails are sent through SNDEMLF.\n\n5. Allow resetting credit limit data through the display file.\n\n6. Provide an option to display customer account statement (via AX1110) for interactive limit checking. \n\nKey files used:\n\n- CDKLMF - Holds customer credit limit data \n- HSKLPF - Stores credit limit monitoring protocol records\n- HSKUIPF - Customer master file\n- KUDSTAM - Customer address file\n\nThe program interacts with the user through display file HS06157D. Email notifications are sent to the address specified in DTAARA EM6157.\n\nThe main database interaction is with table CDKLMF to manage credit limit data. Monitoring results are written to HSKLPF. Customer data is read from HSKUIPF and KUDSTAM.\n\nIn summary, the RPG code implements a credit limit monitoring system focused on managing customer data in CDKLMF and sending notifications when limits change. Key external interfaces are the display file, email, and programs HS0615/AX1110.","file_name":"HS06157.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis code appears to be retrieving credit limit history data from an ERP system called AXAPTA and processing it.\n\nMain logic:\n\n1. It first checks if start and end dates are passed as parameters:\n   - If yes, it sets the start and end dates from the parameters.\n   - If not, it defaults the start date to '2010-01-01' and end date to yesterday's date.\n\n2. It then loops from the start date to the end date. \n\n3. For each date in the loop:\n   - It calls another program/procedure called 'HS06154HC', passing the current date as start and end date parameters.\n   - This program/procedure likely queries the AXAPTA system and retrieves credit limit history records for that date.\n\n4. After looping through all dates, the main logic ends.\n\nIn summary, this code extracts credit limit history from the AXAPTA ERP system one day at a time for a specified date range.\n\nThe called procedure 'HS06154HC' seems to handle querying AXAPTA and returning the results.\n\nThis program interacts with:\n- AXAPTA ERP system to retrieve credit limit history data. \n- No explicit database, but likely writes output to a file.\n- No UI interaction.\n\nLet me know if you need any clarification or have additional questions!","file_name":"HS06154H.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code is for printing shop orders in a workshop. It does the following main steps:\n\n1. Declares variables to hold input parameters like shop order number, date etc.\n\n2. Determines the library name to use based on shop code in input parameter.\n\n3. Adds required libraries to the library list.\n\n4. Calls program HS0652 to print the shop order document.\n\n5. Converts the printed spool file to PDF format. \n\n6. Calls program HSVBF01 to archive the PDF in a document management system. The PDF file name is constructed from shop code, order number etc.\n\n7. Removes the added libraries if they were not already present.\n\nSo in summary, it provides a procedure to print a shop order, convert it to PDF and archive it in a document management system.\n\nThe main input parameters are:\n- Shop code \n- Order number\n- Order date\n- Various flags \n\nThe output is a PDF file archived with a constructed file name containing shop code, order number etc.\n\nIt interacts with the following files/programs:\n\n- Print program HS0652 \n- Conversion program $CVTSPL\n- Archiving program HSVBF01\n- Shop order libraries based on shop code\n\nThe core business logic is printing, converting and archiving a shop order. The other logic handles set up like adding libraries and clean up like removing libraries.","file_name":"HS0652CS.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program appears to be related to a workshop management system for Scania in Germany. \n\nThe core logic is:\n\n1. Declare input parameters:\n- &WERKME: Workshop ID (char 20) \n- &AUFNRL: Work order number (char 5)\n\n2. Declare program name variable &PGM \n\n3. Call program HS0010, passing &PGM as parameter\n- HS0010 likely initializes/prepares the environment\n\n4. Check if &PGM is blank after call to HS0010\n- If yes, goto end of program\n- This indicates an error in initialization\n\n5. Override file KUDSTAM to avoid record locks\n- KUDSTAM likely contains customer data\n\n6. Call program HS0605, passing workshop ID &WERKME and work order number &AUFNRL\n- HS0605 may retrieve/validate the work order\n\n7. Call main processing program HS0600, passing &WERKME and &AUFNRL\n- HS0600 contains core business logic to process the work order\n\n8. Delete override on KUDSTAM file\n\n9. End program\n\nIn summary, this appears to be a standard RPG program that:\n1. Initializes \n2. Retrieves/validates work order\n3. Processes work order (core logic)\n4. Cleans up\n\nThe key files used are:\n- KUDSTAM - Customer data file\n\nThe core business logic for processing the work order is contained in program HS0600.","file_name":"HS0600C.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis code appears to be for a credit limit reorganization program within an ERP system called SDPS/AXAPTA. \n\nThe key details are:\n\nPurpose:\n- Reorganize the credit limit file (HSKLPF)\n\nFiles Used:\n- HSKLPF - The credit limit file that is being reorganized\n\nProcedures Called:\n- HS06155 - Another RPG program that likely contains the reorganization logic\n\nMain Logic:\n1. Monitor for errors with MONMSG\n2. Call program HS06155 to perform the actual reorganization \n3. Reorganize the HSKLPF file by passing it to the RGZPFM operation code\n\nSo in summary, this program calls another program HS06155 to reorganize the HSKLPF credit limit file within the SDPS/AXAPTA ERP system. No specific business logic is contained in this program, it simply sets up error monitoring and calls the other program to do the reorganization work.","file_name":"HS06155C.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis appears to be an RPG program that generates a credit limit report for Scania Deutschland.\n\nMain logic:\n\n1. It creates/clears the output file HS06154PA which will contain the credit limit report.\n\n2. It calls another RPG program HS06154 to generate the report. \n\n3. HS06154 likely contains the main report generation logic.\n\nKey points:\n\n- This program is named HS06154C and titled \"SDPS AXAPTA Credit Limit Report KLP\".\n\n- It was created on XX.03.2010 by a programmer named EL.  \n\n- The application is SDPS-2000 and module is SDPS/AXAPTA.\n\n- It creates an output file called HS06154PA to contain the report. \n\n- It calls RPG program HS06154 to generate the actual report.\n\n- If no parameters are passed, it generates the report for previous day's data.\n\n- This program handles initializing the output file and then invokes the report generation program.\n\nIn summary, this RPG program initializes the output file and calls the credit limit report program HS06154 to generate the report for Scania Deutschland. The key external dependency is the HS06154 program that contains the main report logic.","file_name":"HS06154C.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code appears to be for a program called HS06400C which is part of an application called SDPS (Sales Distribution and Purchasing System?). The specific functionality seems to be related to updating sales orders.\n\nBased on the comments, this program:\n\n- Creates a work file called HS06400F in library QTEMP\n\nSo in summary, the key business logic is:\n\n- This is an RPG program named HS06400C\n- It is part of an application called SDPS that deals with sales distribution and purchasing\n- The specific function is to update sales orders\n- It creates a temporary work file called HS06400F in library QTEMP\n\nThe program does not seem to contain any complex business logic beyond creating the work file. The comments provide useful context about the overall purpose and usage of the program.\n\nIn terms of files and interactions:\n\n- Input Files: None explicitly specified\n- Output Files: \n    - HS06400F (Physical File) - Work file created in library QTEMP\n- Database Interactions: None explicitly specified\n- UI Interactions: None explicitly specified \n\nIn summary, the key inputs, outputs and interactions are focused on creating the temporary work file that will be used for the sales order update process implemented in the larger SDPS application. Let me know if you need any clarification or have additional details to add!","file_name":"HS06400C.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis code is for an application called SDPS (Scania Deutschland) used in the workshop area. \n\nThe specific program is called HS06512C and is titled \"SDPS Print Confirmation Workshop Vehicle Info\". It was created by a programmer named EL on 06/05/2014.\n\nThe program's purpose is to print vehicle information on a workshop confirmation/receipt.\n\nIt utilizes two objects:\n\n1. File HS06512F - This is the work file containing the vehicle info to print\n\n2. DTAARA HS06512V - This data area contains variant info for the print output formatting (e.g. customer vs workshop copy)\n\nThe logic flow is:\n\n1. Create copies of the file and DTAARA objects from the library into QTEMP for temporary use \n\n2. Clear the printer file (HS06512F) to prepare for new output\n\n3. (Main logic would go here to extract data, move to printer file, and print)\n\n4. End of program\n\nIn summary, this RPG program leverages a work file and data area to extract vehicle info, format it, and print a workshop confirmation receipt for the customer and/or workshop copy. The core logic utilizes these objects to gather data and output the required document.","file_name":"HS06512C.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code appears to be calling and passing parameters to other programs/procedures, as well as overriding database files. Here is what I could infer:\n\n1. A character variable &PGM is declared with length 10.\n\n2. The variable &PGM is assigned the value 'HS0610C'. This seems to be the name of a program to call.\n\n3. The program HS0010 is called, passing &PGM as a parameter.\n\n4. After the call, &PGM is checked - if it is blank, the code jumps to the end.\n\n5. A database file KUDSTAM is overridden to itself, with the WAITRCD parameter indicating to not wait for a record lock. \n\n6. The program HS0610 is called.\n\n7. After the call, the override on KUDSTAM is deleted.\n\n8. The program ends.\n\nIn summary, this code is:\n\n1. Calling program HS0010, passing a program name.\n\n2. Checking the returned program name, and conditionally exiting.\n\n3. Overriding a database file KUDSTAM.\n\n4. Calling another program HS0610. \n\n5. Removing the database file override.\n\n6. Ending.\n\nThe key business logic revolves around:\n\n- Calling external programs/procedures (HS0010, HS0610)\n- Passing parameters (program name)\n- Conditionally exiting based on a return value\n- Overriding a database file (KUDSTAM)\n- Removing the override after processing\n\nSo in business terms, the code is:\n\n- Executing some initialization logic (HS0010) \n- Checking the result and early exiting if needed\n- Overriding settings for a database file \n- Performing some business processing (HS0610)\n- Restoring the database file settings\n- Ending\n\nThe database interaction implies this code is interacting with an underlying database file KUDSTAM. No other files or UI interactions are evident from the provided code.","file_name":"HS0610C.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis code appears to be related to credit limit checking functionality in an ERP system like Axapta.\n\nMain logic:\n- The program HS0616C1 is called from another program HS0616. \n- It seems to retrieve customer credit limit information from a physical file HS0616PF and perform some processing on it.\n\nKey files used:\n- HS0616PF - This is likely a physical file containing customer credit limit data. \n   - It is copied to QTEMP library for temporary usage.\n\nOther details:\n- The application is for Scania Deutschland (FVD)\n- It is part of the SDPS/Axapta system\n- Programmer initials are EL\n- Created on XX.07.2010\n\nIn summary, this RPG code is focused on retrieving customer credit limit information from a physical file, likely for further processing and validation in the overall credit check workflow. The core logic revolves around efficient fetching of this credit limit data for use in downstream processes.","file_name":"HS0616C1.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code is for printing shop orders in the automotive industry. \n\nMain functions:\n1. Retrieve order details like order number, department, workstation etc from input parameters\n2. Determine order status (T - released, P - partially released, SP - not released)\n3. Build print file name and path \n4. Call program HS0651 to print shop order\n5. Show prompt to print proforma invoice if shop order type is 06\n6. Archive printed shop orders based on shop order type and archiving settings\n7. Increment electronic archive counter after archiving\n8. Copy printed shop order based on settings\n9. Handle special cases like only archive, don't print etc\n\nThe code interacts with the following files/programs:\n\nInput Parameters:\n- Order details like number, department etc\n\nPrograms Called: \n- HS00STS - Determine order status \n- HS0077C - Prompt for printing proforma invoice\n- HS0651 - Print shop order\n- HS7810C - Print program for special handling\n- HS7820C - Print program for special handling  \n- HS0086 - Increment archive counter\n- HS06514 - Copy printed shop order\n\nFiles Used:\n- WERKST - Print file for shop orders\n- QTEMP/HS0651PF - Work file\n- WERKST_T - Archived print file \n- WERKKV_T - Archived print file\n\nThe print files WERKST, WERKST_T, WERKKV_T are spooled files on the IBM i.\n\nIn summary, the code handles printing and archiving shop orders based on various order details and settings. It calls other programs as needed and interacts with specific print files on the system.","file_name":"HS0651C.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code appears to be related to some financial/credit limit checking functionality in an ERP system called AXAPTA.\n\nMain functions:\n\n1. Copy file - A file called HS0616PF is copied from library QTEMP to library HSPGM. This seems to be a temporary work file that needs to be saved.\n\n2. Call Java class - A Java class called goExcel is called, passing the system name, file libraries, and file name as parameters. \n\n- This seems to transfer the HS0616PF file to an Excel file for reporting or download. \n\n- The Excel file path is hardcoded, indicating a specific network folder.\n\n3. Copy to PC - The Excel file is then copied to a local PC folder path to allow downloading via a browser.\n\nKey points:\n\n- The RPG code interacts with the file system and calls a Java class. \n\n- There is no database interaction directly in the code. \n\n- The Excel file generated is downloaded to allow financial report viewing/analysis.\n\n- File HS0616PF contains temporary data prepared in another program HS0616.\n\n- The code is for an ERP system called AXAPTA, specifically a credit limit checking module integrated with SCANIA.\n\n- Key external dependencies: \n  - Network folder for Excel file\n  - Java class to generate Excel file\n  - Browser access to download Excel file\n\nIn summary, this RPG code executes a financial report generation process by calling a Java program to convert an RPG temp file to Excel format, saving it to a shared folder, and allowing download via a web browser. The core logic centers around automating report generation and file handling.","file_name":"HS0616C2.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code appears to be calling another program HS0654 and passing parameters to it.\n\nPurpose:\n- Call program HS0654 with specific parameters to perform some processing related to \"SPAS\".\n\nParameters:\n- &RNR (Input): A 10-byte character field, initialized to blanks.\n- &RDAT (Input): An 8-byte character field, initialized to blanks. \n- &SYSTEM (Input): A 4-byte character field with value 'SPAS'.\n\nLogic:\n- The main logic is a single CALL operation to program HS0654, passing the 3 parameters.\n\nThe called program HS0654 and parameters imply some additional business context:\n\n- HS0654 is likely an existing program that performs some business logic related to \"SPAS\". \n- &RNR and &RDAT are likely meant to contain identifiers like record number and date that HS0654 uses.\n- &SYSTEM indicates this call is specific to the \"SPAS\" system/context.\n\nIn summary, this program serves as a wrapper to call HS0654 to perform some business processing for the \"SPAS\" system, passing record identifiers. The actual business logic is within the called program HS0654.\n\nNo files or databases are directly accessed in this code. The UI interaction depends on the called program HS0654.","file_name":"HS0654SPAS.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code appears to be for an application that allows managing load codes (pe-prices) for Scania service departments.\n\nMain logic:\n\n1. Declare variables for:\n   - Filter for editing all or only daughter companies (&FILTER) \n   - Service department code & company (&BTS010)\n   - Service department code & location (&BTS020)\n   - Flags to track added libraries (&LIBL1-4)\n   - Library name for service department (&HDLLIB)\n\n2. Add standard libraries\n\n3. Call program to select service department based on filter\n\n4. If filter is 'E' (all), go to end\n\n5. Build library name for selected service department\n\n6. Add service department library\n\n7. Call program to maintain load codes\n\n8. Remove service department library if it was added\n\n9. Loop back to select next service department\n\n10. At end, remove any added libraries\n\nKey points:\n\n- The program allows maintaining load codes per service department\n- Standard and service department specific libraries are added/removed\n- A selection screen filters for all or only daughter companies\n- Load code maintenance is performed by calling another program\n\nSo in summary, this is an RPG application to manage load codes in a modular way by dynamically adding/removing service department specific libraries.\n\nIt interacts with:\n\n- User interface for selection criteria\n- External program for load code maintenance (HS0602) \n- Database (most likely physical files) to store load codes\n- Library system to add/remove libraries\n\nLet me know if you need any clarification or have additional questions!","file_name":"HS0602SC1.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code is an RPG program that handles credit limit approvals in the SDPS AXAPTA system for Scania Deutschland. \n\nThe key steps are:\n\n1. Declare variables to hold input parameters and other data\n\nThe RPG code declares several variables including:\n- &AKTION - 3 character input parameter to indicate requested action (USR, OVR, DLT) \n- &KZLB - 3 character input parameter containing entity code  \n- &USER, &USERN - User profile name and text description\n- &HDLBIB - 10 character variable to hold file handlerbib ID\n- &UMGEBUNG - 3 character variable to hold environment (SAT or blank)\n\n2. Determine environment \n\nThe code retrieves the UMGEBUNG value from a data area and sets &HDLBIB based on environment.\n\n3. Handle request for user profile info\n\nIf &AKTION = 'USR', the code retrieves the user profile name and text description for the input &USER and stores it in &USERN.\n\n4. Handle override request \n\nIf &AKTION = 'OVR', the code overrides database files AUFWKO and AUFTKO to use the handlerbib file ID in &HDLBIB. This allows temporarily redirecting these files.\n\n5. Handle delete overrides request\n\nIf &AKTION = 'DLT', the code deletes any overrides for AUFWKO and AUFTKO.\n\n6. Return\n\nThe program ends after handling the requested action in &AKTION.\n\nIn summary, this code provides a way to lookup user profile information, override database file locations, and delete overrides based on input parameters. The core files used are AUFWKO and AUFTKO.\n\nNo UI or database interactions are coded directly. The RPG code calls other APIs to retrieve user profile data and override files.","file_name":"HS06152C.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis code appears to be for some kind of order/sales processing system for a company called Scania Deutschland. \n\nThe main functionality is:\n\n- Create a temporary work file called HS06001F in library QTEMP\n\nThe key points are:\n\n- This is an RPG program \n- It contains comment headers describing the program name, purpose, author etc.\n- The main logic is in the MONMSG and CRTDUPOBJ operations\n- MONMSG displays error messages\n- CRTDUPOBJ creates a duplicate of file HS06001F into library QTEMP\n- So the overall purpose is to create a temporary copy of the file HS06001F\n\nTo summarize:\n\n- This is an RPG program that duplicates file HS06001F into library QTEMP as a temporary work file for some order/sales processing system.\n\nThe program interacts with:\n\n- File HS06001F - this is the file being duplicated\n- Library QTEMP - this is where the duplicate file is created\n\nNo other interactions or context is provided in the code sample.","file_name":"HS06001C.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program is designed to check credit limits in the SCANIA ERP system (SDPS-2000) when creating sales orders in Axapta.\n\nIt takes several input parameters:\n- &KZLF: Company code \n- &KZLB: Operating concern code\n- &KDRECH: Currency code\n- &USER: User ID\n- &USERN: User name\n- &AKTION: Action code (CLR to clear temp file)\n\nThe main logic is:\n\n1. Determine environment (SAT or HDL) based on global variable value and set database file overrides accordingly. This allows it to run in both the production and test environments.\n\n2. If action code (&AKTION) is 'CLR':\n   - Clear out temporary file HSKLOF that will store order totals\n   - Get current user ID and name\n   - Set file overrides to point to the environment-specific libraries\n\n3. Call HS06151 program, passing operating concern code (&KZLB) and currency code (&KDRECH)\n   - This program likely retrieves open order totals for the operating concern and stores them in the temp file\n\n4. Reset file overrides \n\nSo in summary, this program prepares the environment, calls another program to calculate open order totals per operating concern, stores them temporarily, and resets the environment.\n\nThe temporary data file HSKLOF likely contains the open order totals used later to check credit limits when users create new sales orders in Axapta for that operating concern.\n\nThis program doesn't contain explicit business rules itself, but facilitates the credit limit checking process by preparing data in a temporary structure. The called program HS06151 likely contains more specific business logic for calculating open totals.\n\nLet me know if any part needs further explanation!","file_name":"HS06151C.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code appears to be for a credit limit evaluation program for Scania Deutschland. The key details are:\n\n1. Program name: HS06154HC\n\n2. Program title: SDPS AXAPTA credit limit evaluation history \n\n3. Programmer: EL\n\n4. Creation date: XX.03.2010\n\n5. Description: This program evaluates credit limits without parameters, defaulting to the previous day's data. It calls program HS06154 to perform the actual evaluation.\n\n6. Change date: XX.03.2010 - Initial creation\n\n7. Main logic:\n\n- Declare input parameters for start (&DATVON) and end (&DATBIS) dates\n\n- Monitor for errors\n\n- Create a temporary file (HS06154PA) to store results \n\n- Call HS06154 program, passing start and end dates\n   - This program likely contains the core logic to evaluate credit limits\n\n- On end, delete the temporary file\n\nIn summary, this program appears to be a simple wrapper that calls another program to evaluate credit limits between a start and end date, storing results in a temporary file. The core evaluation logic resides in the called HS06154 program.\n\nNo database or UI interactions are indicated in this code. It seems to be a batch process focused on the single task of evaluating credit limits over a date range.","file_name":"HS06154HC.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program appears to be related to controlling print output or screen display.\n\nThe main logic is:\n\n1. Declare input parameters:\n\n- &ANZDRU: 1-character parameter, seems to indicate number of copies to print \n\n- &KAMNRA: 6-character parameter, likely a customer or account number\n\n- &AUFNR: 5-character parameter, probably a work order number \n\n- &BEREI: 1-character parameter, maybe a department code\n\n- &WETE: 1-character parameter, could be a flag to enable/disable printing\n\n- &SPLITT: 2-character parameter, possibly indicates print layout \n\n2. Delete a temporary file QTEMP/HS0033A if it exists\n\n3. Create the temporary file QTEMP/HS0033A again \n\n4. Call program HS0033, passing the input parameters\n\n5. Call program HS0034, passing &ANZDRU and &KAMNRA\n\nSo in summary, this program prepares a temporary file, calls another program likely to generate print output using the input parameters, and then calls another program, probably to display information on screen.\n\nThe temporary file QTEMP/HS0033A is likely used to store generated print data. The input parameters control things like number of copies, customer number, work order number, etc. that would be printed.\n\nNo database files or other permanent files seem to be used directly in this program. It focuses on generating output through temp files and calling other programs.\n\nLet me know if any part of the logic needs further explanation! I'm happy to clarify or expand on any aspects.","file_name":"HS0609C.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code appears to be related to some kind of production or manufacturing operations.\n\nMain program logic:\n\n- Declares several character variables to hold input parameters. These seem to represent:\n  - Auftragsnummer (Order Number) \n  - Bereich (Area/Department)\n  - Wetter (Weather)\n  - Splitt (Split Shift)\n  - Auftragsdatum (Order Date)\n- Calls another program HS0613, passing the input parameters\n- Sends a message to the user WEHN, concatenating some of the parameters:\n  - Order Number\n  - Date\n  - Time\n\nSo the main program seems to take in some order/production data, call another program to process it, and notify the user of the order details.\n\nThe called program HS0613 is not shown, but likely contains the main business logic for processing the order/production data. \n\nOther notes:\n\n- This appears to be an IBM i/RPG program.\n\n- There are some German language comments indicating it is for the SDPS testing of MON/H.\n\n- The production date and last changed date indicate this code was written in 2008.\n\nSo in summary, this RPG code accepts order/production data, processes it by calling another program, and notifies the user of order details. The main business logic likely resides in the called HS0613 program which is not shown here. The program seems to be used for production monitoring and reporting purposes.","file_name":"HS0613C.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program appears to be for printing external service invoices (Fremdleistungen).\n\nIt declares two character variables:\n- &OVRPRTF_OK - A 1-byte variable that seems to control whether to override printing or not. Initialized to blank/empty.\n- &OUTQ - A 10-byte variable holding the output queue name.\n\nIt then does the following:\n\n- Checks if the specified output queue (&OUTQ) exists using CHKOBJ. \n- If the output queue does not exist, it sets &OVRPRTF_OK to 'N' to avoid printing.\n- Prints the external service invoices file (FLBEST) to the output queue (&OUTQ) using OVRPRTF, but only if &OVRPRTF_OK is not 'N'.\n- Monitors for errors using MONMSG during the output queue check and the printing.\n\nIn summary, the core logic is:\n\n1. Validate output queue \n2. Set override printing flag (&OVRPRTF_OK) based on output queue validation\n3. Print external service invoices if override flag not set to avoid printing\n4. Monitor for errors\n\nThe program interacts with:\n\n- An output queue (specified in &OUTQ) \n- The external service invoices file (FLBEST)\n\nSo in summary, this RPG program controls printing of external service invoices to a validated output queue while monitoring for errors.","file_name":"HS0646C1.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code is a program that submits a job to call another program HS0652CS and pass it various parameters.\n\nMain logic:\n\n1. Declare variables to hold parameters that will be passed to the called program:\n\n- &KZL - 3 character parameter \n- &RNR - 5 character parameter\n- &RDAT - 8 character parameter \n- &STORNO - 1 character parameter\n- &AUFNR - 5 character parameter\n- &AUFDAT - 8 character parameter\n- &BEREI - 1 character parameter\n- &WETE - 1 character parameter  \n- &SPLITT - 2 character parameter\n- &LORT - 1 character parameter\n- &LAND - 3 character parameter\n- &TEST - 1 character parameter\n\n2. Submit a batch job using SBMJOB command to call program HS0652CS, passing the declared parameters\n\n3. Receive message from submitted job using RCVMSG and extract submitted job name into &JOB variable\n\n4. Call program WAITFORJOB in a loop to wait for submitted job to finish, passing submitted job name and a delay\n\nThis program is submitting a batch job to call another program, likely to print some kind of document in batch mode based on the parameters passed. The submitting program waits for the called program to finish before ending.\n\nThe called program HS0652CS and its function is unknown without seeing its code. \n\nBut based on the parameters passed, it likely generates some kind of report or document print output related to workshop orders. Parameters like &AUFNR (order number), &RDAT (date) etc indicate it is printing order documents.\n\nNo file I/O is done in this code. It only submits a job and waits for completion.","file_name":"HS0652C.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis code appears to be for a credit limit evaluation program for a company called Scania Deutschland. The key details are:\n\nPurpose:\n- Evaluate credit limits and send credit limit information. This program is called from another program HS06154C.\n\nFunctions:\n- Override database files to point to production files rather than test files. The files overridden are:\n  - HSBTSLF1: Contains customer master data\n  - HSKUIPF: Contains credit limit data \n  - KUDSTAM: Contains customer master data\n  - HSKLPF: Contains credit limit data\n  - HTKSHL1: Contains history data\n- Override print file to send report to output queue rather than print.\n- Add library HSPGM to library list.\n- Call program HS06154C which likely contains the core credit limit evaluation logic.\n\nSo in summary, this program prepares the environment and then calls another program to do the actual credit limit evaluation.\n\nThe key files used are:\n- Customer master files (HSBTSLF1, KUDSTAM)\n- Credit limit files (HSKUIPF, HSKLPF) \n- History file (HTKSHL1)\n\nAnd the output is a print report sent to an output queue.\n\nThis setup allows reuse of the credit limit evaluation logic (HS06154C) while just changing this outer shell program to control the environment.","file_name":"HS06154C2.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code appears to be for a credit limit evaluation program in an ERP system called SDPS/AXAPTA.\n\nMain functionality:\n- Evaluate credit limits for customers\n- Print credit limit evaluation report (HS06154P)\n\nKey files used:\n- HSBTSLF1 - Probably contains customer master data\n- HSKUIPF - Likely has credit limit data \n- KUDSTAM - Could be customer master file\n- HSKLPF - May contain credit limit master data\n- HTKSHL1 - Possibly transaction/sales order data\n\nDatabase interactions:\n- The code overrides database files to point to files in a different library called HDLZENTRAL, indicating a database connection.\n\nMain program logic:\n1. Override database files\n2. Add RPGLE program library to library list\n3. Call HS06154C program to perform credit limit evaluation\n4. Override print report to output queue KONTINFO and hold the report\n\nIn summary, the code represents an RPG program that evaluates credit limits for customers by accessing various database files. The results are output to a print report that is held in a queue. The core logic is within the called HS06154C program which likely contains the credit limit calculation.","file_name":"HS06154C1.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code appears to be setting up an environment to call an external program that performs credit limit checking in an ERP system called AXAPTA. \n\nKey steps:\n\n1. Set up library list:\n- Check value of &HDLZENLIB parameter to determine which libraries to add\n- Add the following libraries to the library list if not already present:\n  - HSPGM \n  - Library named in &HDLZENLIB parameter (&HDLZENTRAL, &HDLZZZ_ZEN, etc)\n  - Library named in &AXZENLIB parameter (mapped from &HDLZENLIB)\n\n2. Call external credit limit checking program:\n- Set &PROTOKOLL to 'B' for batch mode \n- Call program HS0615, passing &KZL, &KDRECH, and &PROTOKOLL parameters\n\n3. Tear down library list:\n- Remove any libraries that were temporarily added\n\nBased on the library names, this code is:\n- Setting up an environment to call an AXAPTA/Microsoft Dynamics AX external program\n- The program being called (HS0615) performs credit limit checking, likely by integrating with AXAPTA\n- The program runs in batch mode\n\nSo in summary, the key business logic is:\n1. Initialize environment \n2. Call external credit limit checking program for AXAPTA, passing transaction details\n3. Clean up environment\n\nThe code interacts with the IBM i environment and likely an external AXAPTA system. No files or UI interaction is indicated in the provided code.","file_name":"HS0615C.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- This RPG program appears to handle cancellation/storno of workshop orders. \n\nKey Files:\n- FAUFWKO: Workshop order header file\n- FAUFWTE: Workshop order items file \n- FAUFWAW: Workshop order operations file\n- FTRANSAK: Transaction file for recording storno\n- FTEISTAM: Stock of workshop order items \n- FMONSTAM: Stock of workshop order operations \n- FAUFSTAM: Header file of workshop orders  \n- FISTAM: Customer master file\n- FAUFWPK: Workshop order package header file\n- FAUFWPT: Workshop order package items file\n- FAUFWPL: Workshop order package operations file\n- FHSOBKLF1: Order tracking - customer orders file\n- FHSOBKLF2: Order tracking - stock orders file\n- FHSOBKLF8: Order tracking - customer order items file\n- FHSKAMPF: Campaign file\n\nKey Processes:\n\n1. Read customer master record to get customer number and date\n\n2. Check if workshop order can be cancelled\n   - WKO300 must be 00 or blank \n   - WKO830 must be 0 (no external order services linked)\n\n3. If workshop order can be cancelled:\n   - Set cancellation indicator WKO260 = '1'\n   - Delete all items from order items file FAUFWTE\n   - Update order items stock file FTEISTAM (quantity, delivery year/month, change indicator)\n   - Delete all operations from order operations file FAUFWAW\n   - Update order operations stock FMONSTAM\n   - Update workshop order header FAUFWKO (delete BA key)\n   \n4. Record cancellation transactions for each order item and operation in FTRANSAK\n\n5. Recalculate and update order net value in workshop order header FAUFWKO\n\n6. Handle order tracking data in FHSOBKLF* files \n\n7. Delete campaign data in FHSKAMPF if linked to order\n\n8. Handle linked package data in FAUFWPK, FAUFWPT, FAUFWPL\n\n9. Update workshop statistics files for technicians/operations\n\nIn summary, the program handles cancellation of a workshop order by deleting/updating all linked data across multiple files and recording cancellation transactions.","file_name":"HS0660ALT1.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\n1. String Conversion Procedures\n\n- toUppercase: Converts a given input string to uppercase using the `%xlate` built-in function.\n\n- toLowercase: Converts a given input string to lowercase using the `%xlate` built-in function. \n\n2. Memory Management Procedures  \n\n- allocSpace: Allocates or reallocates memory for a pointer variable based on a given size. Checks if pointer is null before allocating, else reallocates.\n\n- deallocSpace: Deallocates memory for a pointer variable if it is not null.\n\n3. Workshop Order Header Creation\n\n- Creates a new workshop order header record (AUFSTAM) by:\n  - Generating a new order number (AUFNR) by incrementing last order number\n  - Setting order type (AUFART), date fields, requester info etc.\n  - Checking for EU VAT ID (USTID/USTOK) for foreign orders\n  - Setting pre-filled account and cost center based on order type\n\n4. Customer Data Lookup and Update\n\n- Looks up customer data by customer number (KDAUF)\n- Updates customer master data (KUDSTAM) if changed\n- Writes customer history data (HSKUDPF) \n\n5. Vehicle Data Lookup and Update\n\n- Looks up vehicle data by license plate (POLKZ) \n- Updates vehicle master data (FARSTAM) if changed\n- Writes vehicle history data\n\n6. Workshop Order Details Creation\n\n- Creates workshop order detail records (AUFWKO)\n- Copies data like customer, vehicle, dates etc. from header\n- Writes linked workshop comments/instructions (AUFWAR)\n\n7. Date Field Conversion\n\n- Converts date fields from RPG format to external format and vice versa\n\n8. Validation Checks\n\n- Various validation checks for dates, account numbers, cost centers etc.\n\n9. Special Prompts and Messages\n\n- Special prompts and messages printed in certain cases like stolen vehicle check.\n\nFiles Accessed:\n\n- KUDSTAM - Customer master file\n- HSKUIPF - Customer data file\n- FARSTAM - Vehicle master file \n- HSFAIPF - Vehicle data file  \n- AUFSTAM - Order header file\n- AUFWKO - Order details file\n- AUFWAR - Order comments file\n- and more...\n\nThe provided RPG code handles the core business process of creating workshop service orders in an automotive scenario, by looking up customer and vehicle information, validating data, creating order header and details, writing comments etc. The logic extracts and processes only the data needed.","file_name":"HS0600ALT.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code consists of an RPG program named HS0649 that performs the following functions:\n\n1. Component Positioning in Workshop Order\n- It is called by program HS0610 to process workshop orders.  \n- It assigns order components like text, campaigns, packages, parts etc to position numbers.\n\n2. Database Files\n- It reads and writes to the following database files:\n  - FAUFWKO (Workshop Order Header)\n  - FAUFWAW (Workshop Order Texts/Operations) \n  - FAUFWKK (Workshop Order Campaigns)\n  - FAUFWPK (Workshop Order Packages)\n  - FAUFWTE (Workshop Order Parts)\n- It also reads other files like workshop times (WAW), campaigns (WKK), packages (WPK), parts (WTE) to extract details.\n\n3. User Interface\n- It displays an interactive subfile for component positioning. \n- Allows selection and mass positioning of components.\n- Shows additional part details like quantity, text etc.\n\n4. Special Logic\n- Handles positioning of additional agreements for Repair & Maintenance orders.\n- Checks for and displays related Repair & Maintenance contracts.\n- Improved cursor handling and user guidance for the subfile.\n\nIn summary, the program provides a flexible interface for assigning and viewing order components in their required positions. It interacts with multiple database files and implements workflow related to workshop order processing. The subfile handling demonstrates typical RPG interactive logic.","file_name":"HS0649ALT.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nOverall purpose:\n- Process and maintain workshop orders. Allows entering order details like parts, labor, comments etc. \n\nKey files used: \n- AUFWKO - Header file for workshop orders\n- AUFWTE - Parts file for workshop orders \n- AUFWAW - Labor file for workshop orders\n- AGASTAM - Rate schedule file\n- TEISTAM - Parts master file\n- MONSTAM - Technicians master file\n- FARSTAM - Vehicles master file\n- KUDSTAM - Customers master file\n- HSAKTLF1 - Program activity log file\n\nMain functions:\n\n1. Validate and retrieve order header details (AUFWKO)\n   - Check if order number exists\n   - Get order header details like customer, vehicle, dates etc.\n\n2. Allow entering order lines - parts and labor (AUFWTE, AUFWAW)\n   - Retrieve part details from parts master (TEISTAM)\n   - Calculate pricing using rates from rate schedule (AGASTAM)\n   - Update parts issued and stock\n   - Validate and add labor details \n   - Update technician statistics (MONSTAM)\n\n3. Print order documents\n   - Generate order acknowledgement\n   - Generate pick list\n   - Generate invoice\n   - Update order status\n\n4. Maintain master files\n   - Add/update customer details (KUDSTAM)\n   - Add/update vehicle details (FARSTAM)\n   - Log all transactions (HSAKTLF1)\n\n5. Special functions\n   - Retrieve open orders for a customer\n   - Enter orders with multiple delivery addresses\n   - Handle campaign orders\n   - Record and track back-ordered parts\n\nSo in summary, it provides an integrated system to capture, process, and track workshop orders including parts, labor and billing. Key functions focus on transaction processing, pricing, and master file maintenance.","file_name":"HS0610ALT.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis appears to be an RPG program for managing workshop orders. The key functions are:\n\n1. Display Workshop Orders\n- Allows displaying all workshop orders, orders for a specific day, or only open orders\n- Orders can be displayed by customer number, license plate number, or official registration number\n- Displays details of the selected workshop order in a subfile\n\n2. Processing Workshop Orders\n- Read workshop order details by key \n- Retrieve associated order texts and operations\n- Calculate total order value\n- Allow changing view between parts, labor, and invoices\n\n3. Customer Matchcode Search\n- Accept customer number input\n- Validate format and do range check\n- Search customer file by number \n- Display matching customers in a subfile\n\n4. Official Registration Search \n- Accept official registration number input\n- Search registration file\n- Retrieve associated customer data\n- Display results in a subfile\n\n5. Retrieval from Electronic Archive\n- Allow retrieving archived data if enabled\n- Call archive retrieval program with key and selection criteria\n\nThe program interacts with these files:\n- Work Order File (AUFWKR) - Main order data\n- Work Order Text File (AUFWAR) - Order text records\n- Work Order Operations File (AUFOPR) - Operations/labor records\n- Parts File (AUFWTR) - Parts used on order\n- Customer File (KUDSTAR) - Customer data\n- Registration File (FARSTAR) - Vehicle registration data \n\nIt outputs to these display files:\n- HS0680S1 - Main order subfile\n- HS0680S2 - Order operations subfile \n- HS0680S3 - Order parts subfile\n- HS0680S4 - Customer search results subfile\n- HS0680S5 - Registration search results subfile\n- HS0680S6 - Selected order details subfile\n\nThe program allows navigating these different views of a workshop order.","file_name":"HS0680ALT.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\n1. toUppercase Procedure\n- Purpose: Convert string to uppercase \n- Input Parameter: string \n- Logic: Use %xlate built-in function to replace lowercase letters with uppercase counterparts\n- Output: Input string converted to uppercase\n\n2. toLowercase Procedure  \n- Purpose: Convert string to lowercase\n- Input Parameter: string\n- Logic: Use %xlate built-in function to replace uppercase letters with lowercase counterparts \n- Output: Input string converted to lowercase\n\n3. allocSpace Procedure\n- Purpose: Allocate or reallocate memory for a pointer variable \n- Input Parameters: \n    - ptr: Pointer variable \n    - bytes: Size to allocate/reallocate in bytes\n- Logic: \n    - If ptr is null, allocate new memory of size bytes and assign to ptr\n    - If ptr is not null, reallocate existing ptr memory to new size bytes\n\n4. deallocSpace Procedure\n- Purpose: Deallocate memory for a pointer if not null\n- Input Parameter: \n    - ptr: Pointer variable\n- Logic:\n    - If ptr is not null, deallocate memory \n\n5. Open work order header record (AUFWKO)\n- Write header record with order details\n- Update AUFTRAG file (AUFSTAM) with new order number\n\n6. Open work order text record (AUFWAR)  \n- Write text records with additional order text \n\n7. If customer is foreign, validate VAT ID\n\n8. Validate account number and cost center\n\n9. Retrieve and validate vehicle data from vehicle file (FARSTAM)\n\n10. Retrieve customer data from customer file (KUDSTAM)\n\n11. Write customer and vehicle data to order\n\n12. Write comments from vehicle (FZKPF) and customer (KUKPF) comment files \n\n13. Check for current campaigns and apply valid campaigns\n\n14. Retrieve order history from customer file (KUDPF)\n\n15. Convert date fields to external format\n\nThe code handles opening a new repair order via customer number or vehicle information, validating linked data, applying business rules, retrieving comments/campaigns, and writing the order details.\n\nFiles Referenced:\n- AUFSTAM - Repair Order Header\n- AUFWKO - Repair Order\n- AUFWAR - Repair Order Text \n- FARSTAM - Vehicle File\n- KUDSTAM - Customer File \n- FZKPF - Vehicle Comments\n- KUKPF - Customer Comments\n- KUDPF - Customer History","file_name":"HS0600ALT4.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code contains several procedures, each serving a specific purpose:\n\n1. String manipulation procedures:\n- toUppercase: Converts a string to uppercase.\n- toLowercase: Converts a string to lowercase.\n- allocSpace: Allocates or reallocates memory space for a pointer variable. \n- deallocSpace: Deallocates memory space for a pointer variable if not null.\n\n2. Workshop order processing procedures:  \n- Main logic:\n  - Checks for multiple order splits.\n  - Checks for campaigns.\n  - Checks for technician comments.\n  - Checks for multi-order.\n  - Checks for warranty contracts.\n  - Retrieves vehicle and customer data for order header.\n  - Allows entry of packages.\n  - Prints workshop order.\n  - Updates customer and vehicle master data if changed.\n- Text entry:\n  - Allows entry/update of text lines for labor, parts, other items. \n  - Calculates amounts based on entries.\n  - Updates order text file (AUFWAW).\n- Parts entry: \n  - Allows entry/update of parts.\n  - Checks inventory, calculates amounts.\n  - Updates parts file (AUFWTE).\n- Labor entry:\n  - Allows entry/update of technician hours.\n  - Calculates amounts based on hourly rate.\n  - Updates labor file (AUFWAW).\n- Other items entry:\n  - Allows entry/update of other items like lubricants.\n  - Calculates amounts.\n  - Updates other items file (AUFWAW).\n- Standings update:\n  - Updates technician standings based on hours entered.\n- Order file update:\n  - Updates order header file (AUFWKO) with latest data.\n\n3. Database files used:\n- AUFWKO: Order header file\n- AUFWAW: Order text file \n- AUFWTE: Order parts file\n- AGASTAM: Labor codes file\n- TEISTAM: Parts master file\n- MONSTAM: Technician master file\n- FARSTAM: Vehicle master file \n- KUDSTAM: Customer master file\n- HSAKTLF1: Active orders file\n- TRANSAK: Transactions file\n- HSOBKLF2: Backorder items file\n\n4. Other functionality:\n- Date manipulation procedures\n- Printing procedures\n- Error checking and handling\n\nSo in summary, the code handles the core business process of workshop order management, including order entry, pricing, invoicing and integration with inventory. The key entities modeled are orders, customers, vehicles, technicians, labor codes, parts, and backorders.","file_name":"HS0610ALT3.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis code contains several procedures and functions:\n\n1. toUppercase:\n- Converts a string to uppercase by replacing lowercase letters with uppercase ones using the built-in %xlate function.\n\n2. toLowercase:  \n- Converts a string to lowercase by replacing uppercase letters with lowercase ones using %xlate.\n\n3. allocSpace:\n- Allocates memory for a pointer variable. If the pointer is null, it allocates new space. If not null, it reallocates to a new size.\n\n4. deallocSpace:\n- Deallocates memory for a pointer if it is not null.\n\n5. Main logic:\n- Opens customer (KUDSTAM) and customer-order (HSKUIPF) files.\n- Gets customer data for order header/details.\n- Checks if vehicle is stolen by reading vehicle file (FARSTAM).\n- Checks customer for EU VAT ID.\n- Writes order header/details records.\n- Handles order splits.\n- Validates dates.\n- Writes comments from vehicle and customer files.\n- Handles campaigns.\n- Updates customer file after writing order.\n\nThis appears to be an order entry system that retrieves customer data, handles special EU VAT cases, validates vehicle info, writes the order details, and updates customer data.\n\nThe key files used:\n- KUDSTAM - Customer master file\n- HSKUIPF - Customer order file\n- FARSTAM - Vehicle master file \n- Various other files for validation/lookups\n\nThe code handles data entry for new orders, writing the records, and linking data between the customer, order, and vehicle systems.","file_name":"HS0600ALT3.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code contains several procedures/functions to perform the following:\n\n1. OpenWorkshopOrder (HS0600):\n- Open a new workshop service order based on vehicle data or customer number\n- Validate customer VAT ID for intra-EU transactions\n- Split service order for internal, external, goodwill etc \n- Retrieve and populate order header, customer, vehicle data\n- Write new order header and details records\n- Check for stolen vehicle\n- Apply any active campaigns\n- Print service order document\n\n2. ConvertToUppercase (toUppercase): \n- Convert input string to uppercase\n\n3. ConvertToLowercase (toLowercase):\n- Convert input string to lowercase \n\n4. AllocMemory (allocSpace):\n- Allocate or reallocate memory for a pointer variable\n\n5. FreeMemory (deallocSpace): \n- Free allocated memory for a pointer if not null\n\n6. ValidateData (multiple functions):\n- Validate customer account and cost center\n- Validate dates (registration, safety inspection etc)\n- Check for home location to print notice\n- Retrieve vehicle comments\n- Retrieve customer comments\n- Write customer data changes to history\n\n7. Campaigns (SRKAM):\n- Check for any active campaigns to apply to the service order\n\n8. PrintDocuments (HS060002):\n- Format and print the service order document\n\n9. UpdateWorkOrder (WKOUPD):\n- Write service order header and details records \n- Add order comments\n\nThe code handles opening a new service order, populating all required data, validating information, applying business rules, updating databases, printing documents, and interacting with other programs/APIs where needed.\n\nLet me know if you need any clarification or have additional questions!","file_name":"HS0600ALT2.txt"},

{"logic":"Here is my attempt at extracting and explaining the business logic from the provided RPG code:\n\nThe code consists of multiple procedures and functions to support the processing of workshop orders (werkstattauftrag). The key capabilities include:\n\n1. Processing workshop order header records (AUFWKO):\n- Read workshop order header record \n- Extract relevant data like customer number, vehicle number, order details etc.\n- Validate data, check for campaigns\n- Update customer master data if needed\n- Print workshop order form \n\n2. Processing workshop order detail records (AUFWAW):\n- Read workshop order detail records\n- Extract relevant data like operation codes, text, pricing etc. \n- Update operation statistics and billing data\n- Allow adding/editing detail records\n- Print updated workshop order\n\n3. Processing parts records (AUFWTE):\n- Read parts records \n- Extract part data like part number, quantity, price etc.\n- Update inventory \n- Print updated workshop order\n\n4. User interface and options:\n- Allow selection of data entry options - parts, operations, complete order etc.\n- Guide user through data entry screens\n- Allow adding comments \n\n5. Pricing and discounts:\n- Retrieve pricing data from master tables\n- Apply pricing rules, campaigns and discounts\n- Calculate net amounts\n\n6. Update files like customer master, inventory, operations data etc.\n\n7. Reporting:\n- Print updated workshop order\n- Update order history\n\nKey files used:\n- KUDSTAM - Customer master\n- AGASTAM - Operation codes master \n- TEISTAM - Parts master\n- AUFWKO - Workshop order header\n- AUFWAW - Workshop order details \n- AUFWTE - Workshop order parts\n- MONSTAM - Tech statistics \n- FARSTAM - Vehicle master\n- RABSTAM - Discounts master\n\nThe code handles the key business processes for workshop order management in an automotive service center. The logic extracts data from various sources, applies business rules, updates multiple files and generates updated documents.","file_name":"HS0610ALT2.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code contains procedures for:\n\n1. Converting strings to uppercase (toUppercase) and lowercase (toLowercase) using the %xlate built-in function. \n\n2. Allocating and reallocating memory for a pointer variable (allocSpace, deallocSpace).\n\n3. Processing workshop and multi-job order data:\n- Read order header records (HS0608S1, HS0608S2)\n- Allow adding new workers or multi-jobs (P001, P002)  \n- Edit existing worker/multi-job records (P053, P054)\n- Delete worker/multi-job records (P004)\n- Distribute standard times to workers (P008)\n- Calculate totals for hours and amounts per worker and multi-job\n- Write output records with totals and details (HS0608S3, HS0608S4, etc)\n- Update worker master records (MONSTAM)\n\nThe code interacts with these files:\n- AUFWAW - Order details file\n- MONSTAM - Worker master file \n- RABSTAM - Discount master file\n- HSMONPF - Worker totals temp file\n- FISTAM - Time recording file (if active) \n\nKey steps:\n- Read order data from AUFWAW into temp storage\n- Allow interactively adding/editing workers and multi-jobs\n- Calculate totals and write out details and totals\n- If time recording active, adjust worker hours based on recorded times\n- Update worker master with hours/amounts\n- Write updated temp totals and details to output files\n\nThe main logic relates to calculating and distributing hours/amounts for workshop and multi-job orders across workers, taking into account time recording data if active. The other procedures handle data input, output and updates.","file_name":"HS0608ALT.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\n1. Validation Routines\n\n- Check if work order number exists (HS061001)\n- Check for open campaigns (HS061004) \n- Validate work type and worker number (HS061005)\n- Validate parts number is in master file (HS061004)\n- Check for comments (KOMMEN)\n- Check for multi-work orders (HS061000)\n- Check for service contracts (HS061000)\n- Validate input data fields (various checks)\n\n2. Work Order Header Processing\n\n- Read work order header (AUFWKO)\n- Read vehicle/customer data (KUDSTAM, FARSTAM)  \n- Read campaign data if applicable (HSKAMPF)\n- Calculate dates\n- Write updated work order header with technician, dates etc.\n\n3. Work Order Details Processing \n\n- Read work order details (AUFWAW)\n- Calculate totals for labor and parts\n- Write new detail records (AUFWAW)\n- Update parts inventory file (TEISTAM) \n- Update technician statistics file (MONSTAR)\n- Write parts transaction file (TRANSAKT)\n\n4. Output\n\n- Print work order document (HS0650)\n- Print pick list (HS0510)\n\nThe code handles validation, calculating totals, updating files, printing outputs related to processing a workshop work order.\n\nKey files used:\n\n- AUFWKO - Work order header\n- AUFWAW - Work order details \n- AUFWTE - Parts details\n- TEISTAM - Parts master\n- MONSTAR - Technician statistics\n- TRANSAKT - Parts transactions\n- KUDSTAM - Customer master\n- FARSTAM - Vehicle master\n\nThe program processes steps for taking a workshop work order, validating inputs, calculating totals, updating inventory and statistics, and producing printed outputs.","file_name":"HS0610ALT1.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\n1. Procedures:\n\n- toUppercase: Converts a given string to uppercase by translating lowercase letters to uppercase using the %xlate built-in function.\n\n- toLowercase: Converts a given string to lowercase by translating uppercase letters to lowercase using %xlate. \n\n- allocSpace: Allocates or reallocates memory for a pointer variable. Checks if the pointer is null, allocates new memory if null, else reallocates to new size.\n\n- deallocSpace: Deallocates memory for a pointer if not null.\n\n2. Main logic:\n\n- Gets current system date and time.\n\n- Retrieves customer and vehicle data by chaining on files.\n\n- Checks if vehicle is stolen by looking at specific fields.\n\n- Retrieves and displays important vehicle and customer comments. \n\n- Checks for valid account number and cost center if specified.\n\n- Validates dates for registration, warranty, inspection etc. \n\n- Retrieves campaign data if applicable.\n\n- Generates a new work order number and outputs work order header record.\n\n- Outputs work order details record with customer, vehicle, dates and other relevant data.\n\n- Writes customer and work order text records. \n\n- Records customer data changes to history file.\n\nSo in summary, it opens a new work order, validating relevant data, retrieving comments and campaign info, generating work order records with pertinent data, and recording customer data history.\n\nThe code interacts with the following files:\n\n- Disk files:\n  - Customer (KUDSTAM)\n  - Work order header (AUFSTAM) \n  - Work order details (AUFWKO)\n  - Vehicle (FARSTAM)\n  - Vehicle/Inspection (HSFAIPF)\n  - Texts (AUFWAR, AUFWAW)\n  \n- Display files:\n  - HS060002 (Work order header display)\n  - HS060003 (Work order details display)\n\nLet me know if you need any clarification or have additional questions!","file_name":"HS0600ALT1.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code contains several procedures, each serving a specific purpose:\n\n1. Main program logic:\n- Reads order data (AUFWKO) and components like texts (TEX), AGA calculations (AUFWAW), parts (AUFWTE), packages (AUFWPK), campaigns (AUFWKK/WKL/WKT) into work file HS0651PF. \n- Processes this file sequentially and prints order confirmation/invoice/credit note based on input parameters.\n- Determines print positions and components to print based on order type and input flags.\n- Prints header, order text, AGA lines, part lines, package lines, campaign info, summaries.\n- Calculates totals like net amount, tax, grand total in DM or Euro based on input currency.\n\n2. Subroutines:\n- LKZ: Determines account code layout for header based on order data.\n- KUDFON: Prints customer phone/mobile number on header.\n- OVL: Handles page overflow and prints header on new page.\n- POSNEU: Prints position number or special text for repair orders.  \n- WAWRE: Calculates AGA line net/gross amounts and discounts.\n- LODRU: Prints labor hours/cost summary. \n- SODRU: Prints misc totals like AGA, packages.\n- KAMDRU: Prints campaign net amount.\n- WPKRE: Calculates package net/gross amounts.\n- WPTRE: Calculates parts net/gross amounts.\n- INTAB: Builds table of unique parts from orders.\n- XTERE: Prints accumulated parts from table with amounts.\n- KAMRE: Prints campaign amounts for hours and parts.\n\nThe code handles printing order confirmations, invoices, credit notes. It calculates amounts based on rates and discounts. It determines what components to print based on order type and parameters. Key data files used are orders (AUFWKO) and texts (TEX).","file_name":"HS0651ALT.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\n1. Customer invoice printing and file update logic\n\n- Read customer order header (AUFWKO) and line item (AUFWTE/AUFWAW/AUFWPK) files\n- Calculate invoice totals for hours, wages, parts, packages \n- Write invoice header record (RE1SUM)\n- Write invoice detail records (RE2SUM) for parts, labor, packages\n- Update order header file (AUFWKO) with invoice number, invoice date, invoice status\n- Update customer statistics file (HSBKUPF) \n\nKey files used:\nAUFWKO - Order header\nAUFWTE - Parts order lines\nAUFWAW - Labor order lines \nAUFWPK - Package order lines\nRE1SUM - Invoice header record\nRE2SUM - Invoice detail records\nHSBKUPF - Customer statistics file\n\n2. Invoice cancellation/credit memo logic\n\n- Same logic as invoice printing but handles reversals\n- Negates amounts for parts, labor, packages for proper crediting\n- Writes reversal indicators on invoice records\n- Updates order header with credit memo number, date, status\n\n3. Invoice formatting logic\n\n- Determines layout and content of invoice based on business requirements\n- Allows printing in multiple currencies (DEM, EUR)\n- Handles pricing and totals in alternate currencies\n- Formats parts lines, labor lines, package lines\n- Calculates and prints taxes as required\n- Prints customer-specific text/logos \n\n4. This appears to be an order/invoice processing system for an auto shop or dealership.\n\nKey files:\n- AUFWxx - Order and repair files\n- HSBKUPF - Customer statistics file\n- RE1/RE2SUM - Invoice output files\n\nInteraction with:\n- Order entry/repair system that populates AUFWxx files\n- External billing/accounting system that consumes invoice output files\n- Customer database that provides HSBKUPF statistics\n- User interfaces for order entry and invoice printing","file_name":"HS0650ALT6.txt"},

{"logic":"Based on the provided RPG code, here is my attempt at extracting and explaining the key business logic:\n\nThe code appears to be for generating workshop job sheets/invoices. The main functions include:\n\n1. Reading customer and job data from files:\n\n- Read customer master file (KUDSTAM) \n- Read job header file (AUFWKO)\n- Read job details like parts, hours etc (AUFWTR, AUFWTE, AUFWAW, AUFWPK etc)\n\n2. Building printable job sheet:\n\n- Determine valid job sheet types allowed based on job status \n- Default job sheet type based on job type code \n- Build job sheet detail lines by reading parts, labor rows\n- Calculate totals like labor hours, part quantities, totals\n- Determine printout layout parameters like pricing, warehouse location etc based on job type\n\n3. Updating data files: \n\n- Update job header with invoiced flag\n- Update job ledger with new invoice data\n- Update customer stats like last visit date\n\n4. Printing job sheets:\n\n- Call external program to print generated job sheet\n- Print to different printers based on workstation\n\n5. Currency conversion:\n\n- Read currency conversion rate \n- Calculate and print invoice values in Euro if applicable\n\nThe code interacts with these files:\n\n- Job details files like AUFWTE, AUFWAW, AUFWPK\n- Job ledger file HSAKTLF1\n- Job history file like HSAHWPF \n- Customer master file KUDSTAM\n- Currency conversion file HSEURPF\n\nIt contains procedures for string manipulation, memory allocation, job data updates, and printing job sheets.\n\nOverall, the code generates printable workshop job sheets and invoices by collecting data from various sources, performing calculations, updating databases, and calling external programs.","file_name":"HS0650ALT7.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- This is an RPG program that prints work orders for a vehicle repair shop. It reads various input files and prints a customized document for the customer.\n\nMain logic:\n\n1. Read customer data from files like FAUFWKO, FAUFWAW, FAUFWTE etc. These contain work order details, texts, parts data etc.\n\n2. Determine the work order type (WAW060) and select data to print based on this. Types include:\n   - Order text (WAW060=' ')\n   - AGA texts (WAW060='01') \n   - Standard times (WAW060='01', WAW230='M')\n   - AGA calculations (WAW060='01', WAW110<>0)\n   - Shop hours (WAW230='1')\n   - Campaign texts (WKK) \n   - Campaign standard times (WKL)\n   - Campaign parts (WKT)\n   - Packages (WPK)\n   - Package texts (PTX) \n   - Package standard times (WPL)\n   - Package parts (WPT)\n   - Parts (WTE)\n\n3. Build a print file HS0651PF with formatted data selected in step 2. Sort it by position number (POS#) and line number (LNR#). \n\n4. Read HS0651PF sequentially and print selected data:\n   - Print header/footer with dates, customer data\n   - Print texts, times, parts data depending on type\n   - Calculate and print amounts like totals, VAT etc.\n   - Print additional data like campaigns, packages\n   - Handle page overflow and print on multiple pages if needed\n\n5. Data is read from database files like FAUFWKO, FAUFWAW etc.\n\n6. Output is printed to a printer file like FWERKST.\n\n7. The program handles Euro currency conversion and can print amounts in Euros.\n\n8. Various parameters control printing like shop layout, customer data, standard times, campaigns etc.\n\nIn summary, this RPG code prints customized vehicle repair shop work orders by selecting, formatting and printing related data from input files based on work order details and parameters. The key steps are data selection, print file creation, formatted printing, calculations and multi-page handling.","file_name":"HS0651ALT2.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code consists of multiple procedures and functions to support generating and printing various types of documents in a workshop/auto repair shop setting.\n\nKey functions:\n\n- Read customer and order data from files\n- Calculate order totals (parts, labor, packages)  \n- Generate documents:\n    - Order confirmation (Auftragsbestätigung)\n    - Invoice (Rechnung) \n    - Credit memo (Stornorechnung)\n    - Proforma invoice (Proformarechnung)\n    - Material receipt (Materialschein)\n- Print documents to appropriate printer based on document type\n- Update files with document data\n- Handle currency conversion between DM and Euro\n- Track open order amounts and remaining labor\n- Validate data and show warnings\n\nKey business terms:\n\n- Auftrag = Order\n- Rechnung = Invoice\n- Storno = Credit memo\n- Werkstatt = Workshop\n- Ersatzteile = Spare parts\n- Arbeitswerte = Labor values \n- Pakete = Packages (bundles of labor+parts)\n\nFiles used:\n\n- AUFWKO: Order header\n- AUFWTE: Order items\n- AUFWAW: Standard labor times\n- AUFWPK: Packages\n- AUFWPL: Package labor\n- AUFWPTR: Package parts\n- HSAKTLF1: Activity file\n- NUMSTAM: Number range file \n- RE1SUM: Summary for invoice\n- RE2SUM: Item details for invoice\n- HSAHKPF: Invoice history\n- HSAHTPF: Invoice items history\n\nIn summary, the code handles common business processes around workshop orders, billing and document printing. The logic centers around calculations, validations, file updates and formatting outputs.","file_name":"HS0650ALT5.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code contains various procedures for:\n\n1. String manipulation\n- toUppercase: Converts a string to uppercase\n- toLowercase: Converts a string to lowercase  \n\n2. Memory management  \n- allocSpace: Allocates or reallocates memory for a pointer \n- deallocSpace: Deallocates memory for a pointer\n\n3. Printing shop documents\n- It reads data from files like customer master (KUDSTAM), item master (FISTAM) etc to extract information needed for document printing\n- Determines the document type (invoice, proforma etc) to be printed based on order data\n- Calculates document totals by accumulating item quantities, values etc\n- Writes records to output files like invoice summary (RE1SUM), invoice details (RE2SUM) etc\n- Updates order header with document printing status\n\n4. Exchanging data with external programs:\n- It calls other programs to get data like customer open items, statistical codes etc.\n- Passes order data as parameters \n- Receives data back from called programs\n\n5. Currency conversion\n- Retrieves currency code from customer master\n- If currency is Euro, converts DM amounts to Euro for printing\n\n6. Updating order dates\n- Updates date of last workshop visit on order confirmation\n\n7. Managing backorder items\n- Checks for pending items in temporary storage\n- Calls external program to print pending items list\n\nThe code handles data for different order types like service, spare parts, packages etc.\n\nKey files used:\n- Customer master, item master, order header, order details, pricing etc\n\nSo in summary, the RPG code covers essential functions needed in a printing shop for document processing, report printing and interfacing with other systems. The business logic centers around order processing, billing and integration.","file_name":"HS0650ALT4.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nOverall Program Logic:\n- This program allows changing an existing order by:\n  1. Splitting the order\n  2. Changing the invoice recipient \n  3. Changing the discount code\n\n- It first reads the FISTAM record to get the date.\n\n- It then allows selecting one of the 3 change options.\n\n- For each change option, it retrieves the existing order details, makes the change, writes updated records, and prints documents.\n\n\nSplit Order Logic:\n- User must enter order number, area, \"from split\", and \"to split\". \n\n- Program checks if order exists and new split is valid.\n\n- It reads the order header and details records. \n\n- It writes new header and detail records for the new split order.\n\n- It updates quantities and values in related files like shop statistics.\n\n- It allows selecting and splitting order text lines to the new split.\n\n- It prints the updated order.\n\n\nChange Invoice Recipient Logic:\n- User enters order number, area, split, and new invoice recipient number.\n\n- It checks if order and new recipient exist.\n\n- It updates the recipient details in the order header record.\n\n- It revaluates the order details for the new recipient. \n\n- It prints the updated order.\n\n\nChange Discount Code Logic: \n- User enters order number, area, split, and new discount code.\n\n- It checks if order exists and discount code is valid.\n\n- It updates the discount code in the order header.\n\n- It revaluates the order details using the new discount.\n\n- It updates quantities and values in related files like shop statistics.\n\n- It prints the updated order.\n\n\nRelated Files:\n- FISTAM - Date file\n- HSAKTLF1 - Shop activity file\n- HSEPKPF - Shop statistics file \n- HSPWDPR - Shop password file\n- AUFSTAR - Order header file\n- AUFWAR - Order text file\n- AUFWKR - Order header work file\n- AUFWTR - Order parts file\n- AUFWPKR - Order packages file \n- AUFWPLR - Order labor file\n- AUFWPTR - Order operations file\n- HSOBKLR2 - Order tracking file\n- MONSTAR - Shop statistics file\n- RABSTAR - Discount file\n- KUDSTAR - Customer file\n- HSBONPR - Customer special conditions file\n- HSZATPR - Customer terms of payment file\n\nPrint Files: \n- HS0640S1 - Order labor details \n- HS0640S2 - Order parts details\n- HS0640S3 - Order parts summary\n- HS0640S4 - Order labor summary\n- HS0640S5 - Order text details\n- HS0640S6 - Order packages details\n- HS0640S7 - Order packages summary\n- HS0640S8 - Order labor packages\n- HS0640Cx - Control formats\n\nThe code handles order data in multiple steps, validating inputs, updating related records, calculating prices with discounts, and printing updated documents. The key focus areas are order splitting, invoice recipient changes and discount code changes.","file_name":"HS0640ALT4.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code contains procedures to print a workshop job sheet (Belegdruck) based on data from various files. \n\nIt extracts data from the following files:\n- AUFWKO: Header data like customer and vehicle info\n- AUFWAW: Workshop text and AGA calculations \n- AUFWTE: Parts data\n- AUFWPK: Package/bundle data\n- AUFWPL: Package wage positions \n- AUFWPT: Package parts positions\n- AUFWKK: Campaign texts \n- AUFWKL: Campaign standard times\n- AUFWKT: Campaign parts\n- TEXSTAM: Additional text lines\n- KUDSTAM: Customer master data\n- FARSTAM: Vehicle master data\n- RE1SUM: Invoice data\n- RWPOSPF: Additional text for special invoice types\n\nIt prints the job sheet in sections:\n- Header with customer, vehicle, dates etc.\n- Position blocks for texts, times, parts etc.\n- Totals for parts, hours, wages etc.\n- Footer with terms, bank details etc.\n\nThe business logic focuses on:\n- Determining position numbers and component types\n- Calculating totals for hours, parts, wages\n- Printing position blocks in correct order\n- Handling special invoice types\n- Page overflow and printing on multiple pages\n- Currency conversion to Euro\n\nFiles accessed:\n- Multiple input files (AUFWxx, TEXSTAM etc)\n- Output spool file WERKST for printing\n\nDatabase interactions:\n- None\n\nUI interactions: \n- None\n\nIn summary, it generates a detailed job sheet by extracting data from various sources, doing calculations, and outputting in formatted blocks by position. The logic handles various invoice types, currency, and page layout.","file_name":"HS0651ALT1.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverall Program Purpose:\n- Position components in a workshop order to position numbers. Called by program HS0610.\n\nComponents processed:\n- Order text (WAW100)\n- AGA text supplementations (WAW200) \n- Multi standard times (WAW300)\n- Workshop/Hours (WAW400)\n- AGA calculation (WAW500)\n- AGA fixed prices (WAW600)\n- External service (WAW700)\n- Kits (WPK800)\n- Parts (WTE900)\n\nProcessing logic:\n\n1. Read workshop order header record (WKO)\n\n2. Process order components:\n   - Read order text records (WAW)\n     - Based on WAW fields, determine component type\n     - Move data to output record format\n   - Read kit records (WPK)  \n     - Move data to output record \n   - Read part records (WTE)\n     - Move data to output record\n       \n3. Sort components by position number \n\n4. Write sorted components to output subfile\n\n5. Allow repositioning components\n   - Update positions in WAW, WPK, WTE files\n\n6. Re-sort and rewrite output subfile \n\nFiles used:\n- WKO - Workshop order header\n- WAW - Order text/components\n- WPK - Kits\n- WTE - Parts\n\nOutput file:\n- HS0649S2 - Sorted subfile by position  \n\nIn summary, this program structures workshop order components into an ordered subfile by position number for display. The position numbers can be manually reordered.","file_name":"HS0649ALT3.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- This is an RPG program for processing workshop orders in a vehicle workshop. It assigns order components like text, campaigns, calculations etc to position numbers.\n\nMain functions:\n1. Assign order components to position numbers\n   - Reads order components like texts, campaigns, packages, parts etc\n   - Checks component type and assigns a position number\n   - Updates position number in the order file\n\n2. Display positions in subfile\n   - Clears subfile\n   - Reads selected order components\n   - Determines component type\n   - Fills display fields and writes to subfile\n   - Sorts subfile by position and type\n   - Writes sorted subfile records \n\nOrder Components:\n- Order Texts (WAW100): Text lines on order\n- AGA-Text Pricing (WAW200): AGA text pricing\n- Multi-Standard Times (WAW300): Multi standard times\n- Workshop Hours (WAW400): Workshop hours \n- Campaigns (WKK450): Campaigns\n- AGA-Calculation (WAW500): AGA calculations\n- AGA-Fixed Price (WAW600): AGA fixed prices\n- External Service (WAW700): External service\n- Packages (WPK800): Packages\n- Parts (WTE900): Parts\n\nFiles Used:\n- FAUFWKO: Workshop order file\n- FAUFWAW: Order texts file\n- FAUFWKK: Campaigns file \n- FAUFWPK: Packages file\n- FAUFWTE: Parts file\n- HS0649S1: Display subfile 1 \n- HS0649S2: Display subfile 2\n\nThis covers the key business logic extracted from the provided RPG code. Let me know if any part needs more explanation or clarification.","file_name":"HS0649ALT2.txt"},

{"logic":"Based on the provided RPG code, here is my attempt to extract and explain the key business logic:\n\nThe code contains several procedures, each serving a specific purpose:\n\n1. toUppercase:  \n- Purpose: Convert a string to uppercase\n- Logic: Uses the `%xlate` built-in function to replace lowercase letters with uppercase ones\n\n2. toLowercase:\n- Purpose: Convert a string to lowercase  \n- Logic: Uses `%xlate` to replace uppercase letters with lowercase ones\n\n3. allocSpace:\n- Purpose: Allocate or reallocate memory for a pointer variable\n- Logic: \n  - Checks if pointer is null (unallocated)\n  - If null, allocates memory of specified size \n  - If not null, reallocates memory to the new size\n\n4. deallocSpace:  \n- Purpose: Deallocate memory for a non-null pointer\n- Logic:\n  - Checks if pointer is not null\n  - If not null, deallocates the memory\n\nThe main logic in the program appears to be:\n\n- Read FISTAM record to get date\n- Open work file HSAKTLF1\n- Write record to HSAKTLF1 with job details\n- Read valid print options from file BELSTAR into subfile\n- Perform various validations on input data\n- Calculate invoice totals by summing up components\n- Write totals to invoice summary record RE1SUM\n- Write invoice detail records to RE2SUM\n- Print invoice using external program HS0651C\n- Update various other files like FISTAM, HSAKTLF1 etc.  \n\nSo in summary, the key functions seem to be:\n\n1. Collecting input data \n2. Calculating invoice totals\n3. Writing invoice records\n4. Printing invoice\n5. Updating other files\n\nThe code interacts with these files:\n\n- FISTAM: Read date \n- BELSTAR: Read valid print options\n- HSAKTLF1: Write job record\n- RE1SUM, RE2SUM: Write invoice summary and details\n- HS0651C program: Print invoice\n- FISTAM, HSAKTLF1: Update at end\n\nHope this helps explain the core logic and functionality in the provided RPG code! Let me know if you need any clarification or have additional questions.","file_name":"HS0650ALT1.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nOverall functionality:\n- This code allows updating of existing work orders by changing the split (accounting grouping), invoice recipient, and discount code.\n\nSplit change logic:\n- User enters work order number, area, \"from split\", and \"to split\". \n- Code checks if work order exists and new split is valid.\n- If new split is 02 (internal), user must enter internal account number and cost center.\n- Prints new header with new split if not existing, and related text lines.\n- Allows selecting to display related labor and parts to change to new split.\n\nInvoice recipient change logic: \n- User enters work order number, area, split, new invoice recipient number.\n- Code checks if work order exists and new customer number is valid.  \n- Displays new address for confirmation and changes invoice recipient in work order header.\n\nDiscount code change logic:\n- User enters work order number, area, split, new discount code.\n- Code checks if work order exists and new discount code is valid.\n- Updates all labor lines and parts lines with new discount code and revalues them.\n\nAdditional logic:\n- Splitting of work steps (labor) only allowed within block 00-05. \n- Special logic to adjust related mechanic statistics when splitting labor steps.\n- Splitting parts lines and revaluation of parts based on new discount.\n- Validation when changing invoice recipient to prevent issues with cross-border VAT.\n- Price determination logic based on discount groups and customer-specific prices.\n\nThe code interacts with these files:\n- Work order header file (AUFWKO)\n- Work order labor file (AUFWAR) \n- Work order parts file (AUFWTR)\n- Customer master file (KUDSTAM)\n- Pricing/discount file (PSTSTAM)  \n\nThis summarizes the key business logic extracted from the provided RPG code. Let me know if any part needs further explanation or expansion.","file_name":"HS0640ALT1.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code contains several procedures, each serving a specific purpose:\n\n1. toUppercase:\n- Purpose: Converts a given input string to uppercase.  \n- Parameters:\n  - string (Input): The string to convert to uppercase.\n- Logic:\n  - Uses the `%xlate` built-in function to replace lowercase letters with their uppercase counterparts.\n  - Returns the uppercase version of the input string.\n\n2. toLowercase:  \n- Purpose: Converts a given input string to lowercase.\n- Parameters:\n  - string (Input): The string to convert to lowercase.\n- Logic:\n  - Uses the `%xlate` built-in function to replace uppercase letters with their lowercase counterparts.\n  - Returns the lowercase version of the input string.\n\n3. allocSpace:\n- Purpose: Allocates or reallocates memory space for a pointer variable.\n- Parameters:\n  - ptr (Input/Output): The pointer variable to allocate/reallocate. \n  - bytes (Input): The amount of memory space to allocate in bytes.\n- Logic:\n  - Checks if ptr is null (unallocated).\n  - If null, allocates memory of size bytes and assigns to ptr.\n  - If not null, reallocates memory to ptr with new size bytes.\n\n4. deallocSpace:\n- Purpose: Deallocates memory space for a pointer variable if allocated.\n- Parameters:\n  - ptr (Input): The pointer variable to deallocate.\n- Logic:\n  - Checks if ptr is not null (allocated).\n  - If not null, deallocates the memory for ptr.\n\nThe main logic in the code involves processing and updating records related to workshop orders. Key steps include:\n\n- Read order header and line records from files\n- Perform validations and checks \n- Calculate order totals like labor hours, part quantities\n- Write updated totals to order header and summary records\n- Print order documents like invoices\n- Update order status on completion\n\nThe code interacts with these files:\n\n- Order header file (AUFWKO) \n- Order line files for labor (AUFWAR), parts (AUFWTR), packages (AUFWPK)\n- Summary files like order totals (RE1SUM)\n- Invoice printing file (OVRPRTF)\n\nIt handles different order types like standard orders, campaigns, quotations.\n\nOverall, the business logic focuses on retrieving workshop order data, performing calculations, updating records, printing documents, and managing order statuses. The RPG code implements this workflow and business rules.","file_name":"HS0650ALT3.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code contains several procedures, each serving a specific purpose:\n\n1. toUppercase:  \n- Purpose: Convert a string to uppercase.\n- Parameters: \n  - string (Input): The string to convert.\n- Logic: \n  - Uses the %xlate built-in function to replace lowercase letters with uppercase.\n  - Returns the uppercase string.\n\n2. toLowercase:\n- Purpose: Convert a string to lowercase.  \n- Parameters:\n  - string (Input): The string to convert.\n- Logic:\n  - Uses %xlate to replace uppercase letters with lowercase.\n  - Returns the lowercase string.\n\n3. allocSpace:\n- Purpose: Allocate or reallocate memory for a pointer variable.\n- Parameters:\n  - ptr (Input/Output): The pointer variable.\n  - bytes (Input): The amount of memory to allocate/reallocate.  \n- Logic:\n  - Checks if ptr is null (unallocated).\n  - If null, allocates memory of the specified size (bytes) to ptr.\n  - If not null, reallocates memory to ptr with the new size (bytes).\n\n4. deallocSpace:  \n- Purpose: Deallocate memory for a pointer if not null.\n- Parameters:\n  - ptr (Input): The pointer variable.\n- Logic:\n  - Checks if ptr is not null (allocated).\n  - If not null, deallocates the memory for ptr.\n\nThe code interacts with these files:\n- FISTAM: Customer master file\n- AUFSTAR: Order header file \n- AUFWKR: Order header work file\n- AUFWAR: Order line (work) file \n- AUFWTR: Parts order line (work) file\n- MONSTAR: Tech times file\n- RABSTAR: Discount code file\n- KUDSTAR: Customer master file\n- HSAKTLF1: Activity file\n- HSEPKPF: Password file\n- HSPWDPR: Password validation file\n\nThe main logic involves:\n- Reading customer and order data\n- Validating passwords\n- Updating/adding records to the work files\n- Splitting orders\n- Changing order header data like customer, discount code etc. \n- Recalculating order line amounts based on new discount codes\n- Printing order documents\n\nSo in summary, it enables maintenance of customer orders by authorized users, including order splitting, header updates, and rebasing of pricing.","file_name":"HS0640ALT3.txt"},

{"logic":"Based on the provided RPG code, here is the extracted business logic:\n\nThe code seems to implement the cancellation/storno of a workshop order. The key steps are:\n\n1. Read customer master data (FIS050)\n\n2. Check if order can be cancelled based on status (WKO300 must be 00 or blank, and no external services assigned (WKO830=0))\n\n3. If order can be cancelled:\n\n- Write a reversal record to transaction file (TRA) for each order line (parts and labor)\n\n- Delete all order header/lines from database files:\n  - Order header (AUFSTAM) \n  - Order lines - parts (TEISTAM), labor (AUFWTE)\n  - Labor by technician (AUFWAW)\n  - Parts packages (AUFWPK)\n  - Parts packages details (AUFWPT) \n  - Labor by technician details (AUFWPL)\n\n- Update order header with storno indicator (WKO260='1') \n\n4. Update statistics:\n\n- Update technician statistics (MONSTAR/SMONPF)\n\n5. Check for pending quantities/amounts:\n\n- Update pending quantities/amounts (OBKSTAM)\n\n6. Delete campaign if assigned to order (WKO840)\n\n7. Write a record to activity file (AKTLF) \n\nThe code interacts with the following files:\n\n- FISTAM - Customer master\n- AUFSTAM - Order header\n- TEISTAM - Order parts\n- AUFWTE - Order labor\n- AUFWAW - Labor by technician \n- AUFWPK - Parts packages\n- AUFWPT - Parts packages details\n- AUFWPL - Labor by technician details  \n- MONSTAR/SMONPF - Technician statistics\n- OBKSTAM - Pending quantities/amounts\n- AKTLF - Activity file\n- TRA - Transaction file\n\nThe program name HS0660 indicates this is a finance/accounting related program.\n\nLet me know if you need any clarification or have additional questions!","file_name":"HS0660ALT.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverall Functionality:\n- This RPG program processes workshop orders by assigning order components to position numbers. The components include: order text, AGA texts, multi labor times, workshop/hours, campaigns, AGA calculations, AGA fixed prices, external services, kits, and parts.\n\nKey Files Used:\n- FAUFWKO: Workshop order file\n- FAUFWAW: AGA calculation file \n- FAUFWKK: Campaign file\n- FAUFWPK: Kit file\n- FAUFWTE: Parts file\n\nMain Logic Flow:\n1. Read workshop order file (FAUFWKO)\n   - Identify component type based on fields like WAW060, WAW230 etc.\n   - Select relevant components into processing table FGA\n\n2. Process order text components \n   - Add to FGA with TYP# = 100\n   - Move data like order number, text etc. to processing fields\n\n3. Process AGA text components\n   - Add to FGA with TYP# = 200\n   - Move data like AGA number, AGA text etc. to processing fields\n\n4. Process multi labor time components\n   - Add to FGA with TYP# = 300\n   - Move labor time value to processing field\n\n5. Process workshop/hour components \n   - Add to FGA with TYP# = 400\n   - Move workshop hours value to processing field  \n\n6. Process AGA calculation components\n   - Add to FGA with TYP# = 500\n   - Move calculation values like price to processing fields\n\n7. Process fixed price components\n   - Add to FGA with TYP# = 600\n\n8. Process external service components\n   - Add to FGA with TYP# = 700\n\n9. Process kit components\n   - Add to FGA with TYP# = 800\n   - Retrieve kit parts data into processing table \n\n10. Process parts components\n    - Add to FGA with TYP# = 900\n    - Move part data like number, text, quantity etc. to processing fields\n\n11. Process campaign components\n    - Add to FGA with TYP# = 450\n    - Move campaign data like number, text, quantity etc. to processing fields\n    - If applicable, retrieve campaign parts into processing table\n\n12. Sort FGA records \n   - Sort by position number + component type\n   - Write sorted table to display file FHS0649S2\n\n13. Display sorted components in subfile for user interaction\n\nThe key processing logic involves identifying the different order components based on file fields, selectively adding them to a processing table FGA with a type identifier, moving relevant data into processing fields, sorting the table, and displaying the sorted components in a subfile for the user. Relevant linked data like kit parts or campaign parts are also retrieved and displayed. The overall goal is to organize and present the order components in a structured manner for further processing in the application.","file_name":"HS0649ALT1.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\n1. String Conversion Procedures\n\n- toUppercase: Converts a given input string to uppercase.\n\n- toLowercase: Converts a given input string to lowercase. \n\n2. Memory Management Procedures \n\n- allocSpace: Allocates or reallocates memory for a pointer variable.\n\n- deallocSpace: Deallocates memory for a pointer variable if not null.\n\n3. Order Header Update\n\n- Allows updating various fields in the order header like split, customer for invoicing etc. Validations are performed to ensure data consistency.\n\n4. Order Line Update\n\n- Allows splitting order lines like labor and parts to a different split. Pricing, tax calculations are updated based on split. \n\n5. Integration with external programs:\n\n- Call out to program HS0680 to print shop order.\n\n6. Database Files:\n\n- FISTAM: Order header\n- AUFWKO: Shop order header\n- AUFWAR: Shop order labor lines\n- AUFWTR: Shop order parts lines\n- KUDSTAM: Customer master\n- RABSTAM: Pricing/Discounts\n- MONSTAM: Tech hours tracking\n- TEISTAM: Parts master\n\n7. Interaction with displays:\n\n- Writes output to display files like HS0640S1, HS0640S2 etc.\n- Accepts input from screens like HS0640C1, HS0640C2 etc.\n\nIn summary, the RPG code provides essential shop order management capabilities like pricing, splitting, invoicing etc by integrating with other programs and database files. The logic is encoded in modular procedures and subroutines.","file_name":"HS0640ALT2.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nOverview:\n- The code handles printing different types of invoices/documents like service invoices, credit memos etc based on input parameters.\n\nMain Steps:\n\n1. Read FISTAM record to get booking date (BUCHDA).\n\n2. Based on input parameters like order number (AUFNR), area (BEREI), workshop/counter (WETE), split (SPLITT):\n   - Validate if all wage works are settled for the order.\n   - Validate if all standard times are settled.\n   - Validate if all multi standard times are settled.\n   - Validate if all campaign wage works are settled.\n   - Read order components like wage work (AUFWAR), campaigns (AUFWKK), parts (AUFWTR), packages (AUFWPK). \n\n3. Calculate invoice totals by adding up wage work, campaign, part and package amounts.\n\n4. Write invoice header and item records to output files based on invoice type. \n\n5. Update order header after invoice printing to mark it as invoiced.\n\n6. Update open customer balances.\n\n7. If invoice type is service invoice or credit memo:\n   - Write records to invoice summary file (RE1SUM, RE2SUM).\n   - Write records to invoice history file (HSAHWPF, HSAHTPF).\n   - Update campaign header file (HSAHPPF) with accumulated totals.\n\n8. The program handles printing invoices in Euro or DM currency based on customer master data.\n\n9. Invoice printing positions and layout is controlled by input parameters.\n\n10. Input parameters also control which invoice types are allowed for an order based on its status.\n\n11. The program checks and prevents duplicate invoice printing.\n\nKey Files Used:\n\n- FISTAM: Booking date\n- AUFWAR: Wage work \n- AUFWKK: Campaigns\n- AUFWTR: Parts\n- AUFWPK: Packages\n- RE1SUM: Invoice totals\n- RE2SUM: Invoice detail lines \n- HSAHWPF: Invoice history - wage work\n- HSAHTPF: Invoice history - parts\n- HSAHPPF: Invoice history - packages\n- KUDSTAM: Customer master\n- NUMSTAM: Number range for invoice numbers\n\nIn summary, the program handles complex business logic for flexible invoice printing and updating multiple databases. The logic checks data consistency, prevents duplicates, calculates totals, handles currency conversion and prints invoices in customized formats.","file_name":"HS0650ALT2.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code contains several procedures, each serving a specific purpose:\n\n1. Splitting an existing order:\n\n- Input: Order number, Area, \"From split\", \"To split\"\n- Validates order exists and new split is valid\n- Creates new order header record with new split if not existing\n- Allows selection to change work operations and parts to new split\n\n2. Changing customer invoice recipient: \n\n- Input: Order number, Area, Split, New customer invoice number\n- Validates order exists and new customer is valid\n- Displays new address for confirmation/update\n- Updates new customer invoice number in order header\n\n3. Changing rebate code:\n\n- Input: Order number, Area, Split, New rebate code  \n- Validates order exists and new rebate code is valid\n- Updates all work operations and parts with new rebate code\n\n4. Printing shop order:\n\n- Prints existing shop order\n\n5. Splitting technician hours:\n\n- Only blocks 00-05 of technician hours can be split\n- Old values in technician stats deducted for \"From split\"\n- New values added to technician stats for \"To split\"\n\n6. Splitting parts:\n\n- New parts positions created according to split change\n- Inventory tracking updated based on split change\n- Old values in technician stats deducted for \"From split\" \n- New values added to technician stats for \"To split\"\n- Price determination logic checked and applied\n\nThe code interacts with these files:\n\n- Order header file\n- Order work operations file \n- Order parts file\n- Technician stats file\n- Inventory tracking file\n- Pricing file\n\nIt contains UI displays for input, confirmation, and output.","file_name":"HS0640ALT.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nOverall Functionality:\n- This program displays workshop orders based on user selection criteria. It allows viewing all open orders, orders for the day, or filtered by order number, customer number, vehicle number, etc.\n- It displays details of a selected workshop order in multiple subfiles showing header info, order texts, parts, and work steps/pricing.\n- It has search functions by customer number and vehicle registration number.\n\nSubroutines:\n\n1. ALLAUF:\n   - Purpose: Display all open workshop orders or orders for the day.\n   - Logic:\n     - Read all open orders or all orders for today's date from file AUFWKR.\n     - For each order meeting criteria:\n       - Move header details like customer, vehicle, order no to variables.\n       - Call RESUPR to read invoicing data if order is invoiced.\n       - Call SUBFUE to move data to display fields.\n       - Write order header record to subfile 1.\n\n2. WESAUF: \n   - Purpose: Display details of selected workshop order in subfile 2.\n   - Logic:  \n     - Read order header, text, parts, and work/pricing details from associated files into subfiles 2 and 3.\n     - If pricing subfile is empty, call NETRE to calculate net totals for parts and work.\n     - Display subfiles 2 and 3.\n\n3. KUMC:\n   - Purpose: Search orders by customer number.\n   - Logic:\n     - Based on full or partial customer number entered, read matching records from customer file into subfile 4.\n     - Allow selection of customer to filter orders.\n\n4. AKMC: \n   - Purpose: Search orders by vehicle registration number.\n   - Logic:\n     - Based on full or partial registration number entered, read matching records from vehicle file into subfile 5.\n     - Allow selection of registration to filter orders.\n\n5. SUBLOE:\n   - Purpose: Clear order subfiles before new selection.  \n\n6. RESUPR:\n   - Purpose: If order is invoiced, read invoicing header data.\n\n7. SUBFUE:\n   - Purpose: Move data to order header subfile fields.\n\n8. NETRE:\n   - Calculate net totals for parts and work steps from associated files.\n\n9. EINKD:\n   - Logic to filter orders by customer number entry. \n\n10. EINFG:\n    - Logic to filter orders by vehicle registration number entry.\n\n11. SR11: \n    - Logic to toggle between order list and detail views based on user pressing F11.\n\nFiles Referenced:\n\n- AUFWKR: Workshop Order Header File\n- AUFWAR: Workshop Order Texts File \n- AUFWTR: Workshop Order Parts File\n- AUFWPR: Workshop Order Work Steps/Pricing File\n- KUDSTL: Customer Master File\n- FARSTL: Vehicle Registration Master File \n- RE1SUM: Invoice Header Totals File\n- HSAKT: Archive File\n\nThis summarizes the key business functionality and data entities identified in the provided RPG code. The program appears to focus on workshop order management, display and search. Please let me know if any additional information or clarification is needed!","file_name":"HS0680ALT1.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverall Functionality:\n- This code handles printing different types of invoices/credit notes (Auftragsbestätigung, Rechnung, Stornorechnung, Gutschrift etc.) for a workshop/service center.\n\nKey Steps:\n\n1. Read invoice type selected by user and validate if it's allowed based on order status.\n\n2. Read order details like customer, date, items/services etc. from different files.\n\n3. Calculate totals like net amount, VAT amount, discounts etc. based on items. Handle credit notes by multiplying amounts by -1.\n\n4. Write invoice header and details to invoice print file. \n\n5. Update order files like open order, sales statistics etc. with new invoice status.\n\n6. For credit notes, reverse booked revenue by deleting sales postings.\n\n7. Print invoice using external program.\n\nKey Files Used:\n\n- FISTAM: Date file\n- HSAKTLF1: Activity log \n- AUFWKR/PL/PT/KT/KK: Order headers\n- AUFWTR/TE: Parts\n- AUFWAR: Labor\n- AUFWPK: Packages \n- HSAHPPF: History items\n- HSAHTPF: History parts\n- RE1SUM/RE2SUM: Invoice totals\n- NUMSTAM: Number range for invoice numbers\n\nInterfaces:\n- User entry of invoice type\n- External print program to generate invoice output\n- Database updates like order status, customer statistics etc.\n\nIn summary, the code handles the complete business process of generating workshop/service center invoices and credit notes by gathering data from various sources, calculating invoice totals, updating databases, generating invoice print file and triggering external print program.","file_name":"HS0650ALT.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nOverview:\nThe code is for a workshop management system and contains logic related to campaigns, technicians, timesheets, parts inventory, and billing.\n\nKey functions:\n\n1. Campaign Management\n\n- Display list of open campaigns (procedure SRAKT)\n- Add new campaign (procedure SR06)\n  - Generates next campaign number \n  - Initializes campaign with status \"X\"\n- Delete campaign (procedure SR004)\n  - Deletes campaign header record\n  - Deletes campaign details records \n  - Resets related timesheet and inventory records\n- Update campaign description/text (procedure SR008)\n\n2. Technician Management \n\n- Display list of technicians (procedure SR04)\n  - Shows name, total hours, and hours remaining\n- Assign technician to campaign (procedure SR04)\n  - Checks for valid/active technician\n  - Updates timesheet (MON) records\n- Remove technician from campaign (procedure SRMON)\n  - Reverses timesheet (MON) record updates\n\n3. Timesheet Management\n\n- Display timesheet line items for a campaign (procedure SR007)\n  - Shows assigned technicians and hours \n- Update/change timesheet line item (procedure SR007)\n  - Validates data values\n  - Recalculates remaining hours\n  - Updates timesheet (MON) records\n\n4. Parts Inventory Management\n\n- Display parts list for a campaign (procedure SR006)\n- Update part quantities on issue/receipt (procedure SRBES)\n  - Updates inventory (TEI) records\n\n5. Billing\n\n- Calculate total cost for a campaign (procedure SR007)\n  - Sums up technician hours * rate\n  - Sums up parts quantities * cost\n- Generate customer invoice (procedure SRBES)\n  - Creates billing transaction (TRN) records\n\nThe code utilizes RPG data structures, keyed file access, subfile processing, and calls to subprocedures. There is also logic to integrate with timesheet data from a ZEF system if active.\n\nLet me know if any part of the business logic needs further explanation!","file_name":"HS0609ALT.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis RPG program appears to handle the printing of different types of workshop documents like invoices, credit notes etc. \n\nThe key functions are:\n\n1. Validate Input Parameters\n   - Check if mandatory input fields like order number (AUFNR), area (BEREI), workshop (WETE) etc are passed and are valid\n   - Initialize variables like document type (BEL01B), printer (BELPRT) etc based on input\n   - Read various files like order header, parts list etc to get data\n\n2. Calculate Invoice Totals\n   - Read order detail lines (parts, labor etc) \n   - Calculate totals like gross amount, discounts, net amount etc by line type\n   - Update summary totals by document type\n\n3. Print Documents\n   - Based on document type, call the relevant print program (HS0651C)\n   - Pass document details like header text, currency, totals etc as parameters \n   - Update files like order header to mark it as invoiced\n  \n4. Update Order Status\n   - Mark order header as invoiced after printing invoice\n   - For credit notes, reset the invoiced flag\n   - Update customer turnover figures in customer master\n\n5. Validate Business Logic\n   - Various checks like all labor lines/multipliers charged, outstanding parts in staging etc\n   - Warnings displayed in case of issues \n\n6. Handle Campaign Orders\n   - Identify & mark campaign orders\n   - Validate if campaign already ordered\n   - Calculate campaign totals separately \n\n7. Manage R&W Agreements\n   - Check for R&W additional agreements\n   - Print relevant notes on invoice\n   - On credit note, reset R&W totals\n\n8. Track Document History\n   - Write records of documents printed to history files\n\nSo in summary, it handles printing invoices and related documents for workshop orders by calculating totals, printing via format, updating statuses, validating logic and tracking history.","file_name":"HS0650.txt"}

]

def process_folder_06(parent_folder_id):    
    
    folder_name = "Customer"
    folder_business_logic = ""
    
    folder_structure={"files":["HS0649.txt","HS06210.txt","HS06006.txt","HS06007.txt","HS06211.txt","HS0660.txt","HS06213.txt","HS06005.txt","HS06004.txt","HS06212.txt","HS06400.txt","HS06001.txt","HS0670.txt","HS06003.txt","HS06002.txt","HS0602.txt","HS0616.txt","HS06501.txt","HS06515.txt","HS06514.txt","HS0617.txt","HS0603.txt","HS0615.txt","HS0601.txt","HS06270.txt","HS06502.txt","HS0654_ORG.txt","HS0653_V40.txt","HS06503.txt","HS0600.txt","HS0614.txt","HS0610.txt","HS0604.txt","HS06513.txt","HS06512.txt","HS0605.txt","HS0611.txt","HS0607.txt","HS0613.txt","HS06504.txt","HS06511.txt","HS0612.txt","HS0606.txt","HS0608.txt","HS06090.txt","HS0609.txt","HS0635.txt","HS0618.txt","HS06154HS.txt","HS06153.txt","HS0640.txt","HS0654.txt","HS06152.txt","HS0680.txt","HS06151.txt","HS06155.txt","HS0652.txt","HS0646.txt","HS06009.txt","HS06008.txt","HS0653.txt","HS0690.txt","HS06154.txt","HS06156.txt","HS0645.txt","HS0651.txt","HS06157.txt","HS06154H.txt","HS0652CS.txt","HS0600C.txt","HS06155C.txt","HS06154C.txt","HS06400C.txt","HS06512C.txt","HS0610C.txt","HS0616C1.txt","HS0651C.txt","HS0616C2.txt","HS0654SPAS.txt","HS0602SC1.txt","HS06152C.txt","HS06001C.txt","HS06151C.txt","HS06154HC.txt","HS0609C.txt","HS0613C.txt","HS0646C1.txt","HS0652C.txt","HS06154C2.txt","HS06154C1.txt","HS0615C.txt","HS0660ALT1.txt","HS0600ALT.txt","HS0649ALT.txt","HS0610ALT.txt","HS0680ALT.txt","HS0600ALT4.txt","HS0610ALT3.txt","HS0600ALT3.txt","HS0600ALT2.txt","HS0610ALT2.txt","HS0608ALT.txt","HS0610ALT1.txt","HS0600ALT1.txt","HS0651ALT.txt","HS0650ALT6.txt","HS0650ALT7.txt","HS0651ALT2.txt","HS0650ALT5.txt","HS0650ALT4.txt","HS0640ALT4.txt","HS0651ALT1.txt","HS0649ALT3.txt","HS0649ALT2.txt","HS0650ALT1.txt","HS0640ALT1.txt","HS0650ALT3.txt","HS0640ALT3.txt","HS0660ALT.txt","HS0649ALT1.txt","HS0640ALT2.txt","HS0650ALT2.txt","HS0640ALT.txt","HS0680ALT1.txt","HS0650ALT.txt","HS0609ALT.txt","HS0650.txt"]}
    files_name=[]
    for file in business_06:
        if(folder_business_logic==""):
            folder_business_logic=file["logic"]
            files_name.append(file["file_name"])
        else:
            folder_business_logic = combine_business_logic(folder_name,folder_structure,files_name,folder_business_logic,file["file_name"],file["logic"])
            files_name.append(file["file_name"])
    
    logic = folder_business_logic
    return logic

class HigherLevelBL06(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request):
        start_time = time()
        folder_id = request.data.get('id')
        business_logic = process_folder_06(folder_id)
        end_time = time()  # Record the end time
        elapsed_time = end_time - start_time 
        response_data = {
            "response": business_logic,
            "elapsed_time_seconds": elapsed_time
        }
        return Response(response_data, status=200)







# HS06 Number Files Higher Level Business Logic

business_06N=[
    
{"logic":"Here is the extracted business logic from the provided RPG code:\n\n1. Customer Order Opening\n\n- Allows opening a customer order by entering vehicle data or customer number. \n\n- Validates and retrieves vehicle data like registration number, chassis number, vehicle type etc from the vehicle master data file (FARSTAM).\n\n- Validates and retrieves customer data like name, address etc from the customer master data file (KUDSTAM).\n\n- Performs checks for duplicate customer numbers, valid dates, allowed order types based on customer etc.\n\n- Default values are populated for various fields like order type, dates, advisor etc.\n\n- Special logic for Scania vehicles to retrieve additional details from SCAS.\n\n2. Order Split Selection\n\n- Allows selecting the order split type like warranty, repair contract, campaign etc.\n\n- Checks if active vehicle contracts like R&W, ARV, REP are present and shows messages. \n\n- For contracted services, prompts to select the appropriate CS split based on active contracts.\n\n- Default split values set based on customer type, vehicle type etc.\n\n3. Validation and Defaults\n\n- Various validations on dates, vehicle details, customer info, order types etc.\n\n- Default values populated for fields like dates, times, order accounts etc based on configs.\n\n4. Updates\n\n- Updates the customer, vehicle and order files with the new order data.\n\n- Maintains change history for customer and vehicle master data.\n\n5. Integration\n\n- Integration with SCAS system to retrieve vehicle details.\n\n- Integration with AXAPTA ERP system for additional validations.\n\n- Integration with other systems like DKV, UTA etc.\n\n6. Miscellaneous\n\n- Displays vehicle comments, campaign info etc based on configs.\n\n- Email address management routine.\n\n- Other features like credit limit check, technician calendar, job management etc.\n\nThe key files used are KUDSTAM for customer master, FARSTAM for vehicle master and AUFWKO for order document. The program allows creating and maintaining customer vehicle orders in an automobile dealer scenario.","file_name":"HS0600.txt"},

{ "logic":"Here is the extracted business logic from the provided RPG code:\n\nThis RPG program appears to handle the positioning/assignment of components to position numbers in a workshop job/work order. The key functions include:\n\n1. Positioning various component types to position numbers:\n- Work order texts (TYP#100) \n- AGA texts (TYP#200)\n- Multi labor times (TYP#300)\n- New labor times (TYP#350)\n- Workshop/hours (TYP#400) \n- Machine hours (TYP#430)\n- Campaigns (TYP#450)\n- AGA calculations (TYP#500)\n- AGA fixed prices (TYP#600) \n- External services (TYP#700)\n- Kits (TYP#800)\n- New kits (TYP#850) \n- Parts (TYP#900)\n\n2. Displaying components in a subfile for selection/update\n\n3. Allowing mass update of selected components to a single position\n\n4. Integration with new workshop route logic (when WKO280='AV') to also position new labor times\n\n5. Integration with new external services to also position those (when FLNEU='F') \n\n6. Additional logic to:\n- Fetch and position job header/description info if called from job order processing \n- Suppress positioning if certain splits (like EPS)\n- Handle parts packaging and text\n- Display parts/kits components in kits/packages\n- Link components to workshop damage coding\n- Protect position numbers linked to jobs\n- Allow job change for certain component types\n- Filter display based on F10 option\n\nThe file I/O includes chain/reads on various externally described files like AUFWRZ, AUFWKK, AUFWTE.\n\nSo in summary, this program's business logic centers around positioning/linking various work order and job components to position numbers, supporting new functions like labor routes, external services, etc. The output subfile provides a consolidated view for selection and update.","file_name":"HS0649.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- This is an RPG program named HS0660 for cancelling a workshop order. \n\nMain functionality:\n- A workshop order can only be cancelled if WKO300 is 00 or blank, and there are no assigned external services (WKO830=0) to the order.\n\n- After cancellation, WKO260 gets cancellation flag '1'. \n\n- A cancellation record is written for each order item. \n\n- All order items are deleted.\n\n- Order header (AUFSTAM) is read to get the account key.\n\n- After cancellation:\n  - Transaction records are written to reduce stock levels. \n  - Wage records are deleted to reset technician statistics.\n  - Purchase order items are deleted.\n  - Campaign data is deleted.\n  - Customer outstanding data is updated.\n  - Import interface data is deleted.\n\n- Additional checks:\n  - No open clock times for the order.\n  - Cancellation only allowed if order net value is zero.\n  - No unfinished external services linked to the order.\n  - User authority check via CZM for processing external workshops.\n  - Send cancellation data to Vehicle History Information system (WHI).\n\n- Special handling: \n  - Status update for connected FTM modules/packages.\n  - EPS split orders.\n  - Job/work orders.\n  \nRelated files:\n\n- FISTAM - Customer file\n- AUFPKO - Order packages file  \n- AUFSTAM - Order header file\n- AUFWSKF - Order GWL file\n- AUFWRZ - Order standard times file \n- AUFWAW - Order wages file\n- AUFWKO - Order header file\n- AUFWTE - Order items file\n- AUFWTLF3 - Order items file\n- AUFWPK - Order packages file\n- AUFWPT - Order package items file \n- AUFWPL - Order package wages file\n- AUFWKK - Order text lines per package\n- AUFWKT - Order package campaign items\n- AUFWKL - Order package campaign wages\n- FFISTAM - Item file\n- FHSAKTLF1 - Activity file \n- FHSBTSLF1 - Operating unit file\n- FHSEPKPF - Access keys file\n- FHSKAMLF1 - Campaign file\n- FHSMONPF - Tech times file\n- FHSOBKLF1 - Customer outstanding header file \n- FHSOBKLF2 - Customer outstanding items file\n- FHSOBKLF8 - Customer outstanding per order file\n- FHSKRUPF - Customer outstanding new file\n- FHSFLALF1 - External services file\n- FHSPWDPF - Access passwords file\n- FMONSTAM - Tech master file\n- FTEISTAM - Stock file\n- FTRANSAKT - Transaction file\n- FHSMADPF - Change documentation file\n- FHSMPAF - Import parts file\n- FHSMAWPF - Import wages file \n- FHSMTEPF - Import items file\n\nThe program interacts with the database to read, update, delete and write records to perform the order cancellation functions.","file_name":"HS0660.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nOverall Purpose:\n- Convert an existing repair order (KV) into a workshop order by specifying a target split (internal account). This involves validating the target split, transferring relevant data from the KV, and recalculating pricing.\n\nKey Steps:\n1. Get required input parameters - Order number, Area, \"From split\", \"To split\".\n\n2. Validate that the order exists and the target split is valid. If not, show error.\n\n3. Read customer master data to get country, customer discount code, subsidiary status.\n\n4. Read accounting data to get booking date. \n\n5. Validate VAT ID for EU/Non-EU split 55/65.\n\n6. Check if target split is already open:\n   - If yes, transfer data like customer number, dates, texts, pricing etc. Recalculate discount if needed.\n   - If no:\n      - Get default accounts for internal splits from DTAARA. \n      - For AXAPTA, get accounts from custom tables.\n      - Validate accounts.\n      - Create new split header record with new split.\n      \n7. Labor:\n   - Read existing labor lines.\n   - Recalculate pricing with new split. \n   - Write new labor lines with new split.\n   - Update labor statistics.\n   \n8. Parts:\n   - Delete all existing parts lines for old split.\n   - Read parts data from selection screen.\n   - Write new parts lines for each line using new split.\n   - Recalculate pricing.\n   - Update stock statistics.\n   \n9. Packages:\n   - Split package components like labor and parts.\n   - Recalculate pricing.\n   \n10. Check credit limits in AXAPTA on submit.\n\n11. Write split change data to audit trail.\n\n12. End program.\n\nKey Files Used:\n- KV Repair Orders (FAUFSTAM) \n- Pricing Conditions (FHRAZPF)\n- Accounting Master Data (FFISTAM) \n- Labor Statistics (FHSMONPF)\n- Stock Statistics (FTEISTAM)\n- AXAPTA Customer Master (FAXAXTPF)\n- AXAPTA Config Tables (FAXVOIPF)\n- Repair Order Audit Trail (FTRANSAKT)\n\nInterfaces:\n- User screen I/O\n- Database I/O \n- Call to AXAPTA credit limit check\n- Writing to audit trail\n\nIn summary, the code handles validation, data transfer, and repricing to convert a repair order to a workshop order by changing the internal split. It interacts with pricing conditions, statistics, AXAPTA and audit trail.\n\nPlease let me know if you need any clarification or have additional questions!","file_name":"HS0670.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code is for maintaining burden codes (BC) which are used for processing standard times.\n\nKey functions:\n\n1. Add new BC record\n\n- Allowed range is 20-59\n- Validate BC is not blank or duplicate\n- Write new record to BC file (HSBCVPR) \n\n2. Update existing BC record\n\n- Move user input fields to BC record\n- Update BC file (HSBCVPR)\n\n3. Delete existing BC record \n\n- Validate BC not used in other records (HSBCSPR)\n- Protect records 01-19 and 9A-9Z \n- Delete BC record from BC file (HSBCVPR)\n\n4. Display BC records in subfile\n\n- Clear then fill subfile with BC records \n- Protect records 01-19 and 9A-9Z\n\nRelated files:\n\n- HSBCVPR - BC master file\n- HSBCSPR - Stores BC usage in other records \n\nThe code allows maintaining burden codes which are used in standard time processing. Key functions include add, update, delete and display of BC records while validating values and protecting certain ranges.","file_name":"HS0602.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code implements customer credit limit checking functionality by interacting with the AXAPTA ERP system.\n\nMain steps:\n\n1. Check if user is authorized for SDPS access (KZLB)\n\n2. Check if AXAPTA is active (AXAPTA variable) \n\n3. Check if credit limit functionality is active (AXAKLA variable)\n\n4. Retrieve customer data from SDPS (HSKUIPR) and AXAPTA (KUDSTAR) files\n\n5. Get additional customer info from AXAPTA (AXAXTLR5/AXAXTLR2) \n\n6. Get customer credit limit data from AXKLKR file\n\n7. Check if customer has temporary credit limit (KLK_TKL field)\n\n8. Validate if current date is within temporary credit limit validity period (KLK_TKLV, KLK_TKLB)\n\n9. Calculate customer turnover over past years by retrieving data from HSBKULR2 file\n\n10. Check if turnover meets specified minimum (F_UMS field) \n\n11. Write filtered customer data to output file HS0616PR\n\n12. Allow downloading of output file (HS0616C2 call)\n\nThe code interacts with the following files:\n- SDPS files: HSBTSLR1, HSKUIPR, KUDSTAR \n- AXAPTA files: AXAXTLR5, AXAXTLR2, AXKLKR\n- Turnover file: HSBKULR2\n- Output file: HS0616PR\n\nAdditional details:\n- Uses selection criteria entered in screen fields (F_AXG, F_AXV etc) to filter data\n- Converts identifying codes (AXG, AXV etc) into descriptive values\n- Stores workflow status and messages in INFO45 field\n- Cursor positioning logic present \n\nIn summary, this program implements credit limit validation for customers by retrieving data from multiple systems and applying complex selection rules.","file_name":"HS0616.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis RPG program appears to be for validating and selecting account and cost center values in some kind of order entry system.\n\nThe key procedures and logic are:\n\n1. PLAUSI - Validation logic\n- Validates passed in account number (AXKTO) and cost center (AXKST)\n- Looks up account and cost center values in HSAXIF file\n- If not found, sets error messages \n- If found, sets description and explanation text\n- Sets OK flag if both account and cost center are valid\n\n2. BEDF - Interactive selection logic\n- Allows user to select account or cost center from list\n- Builds selection list by:\n  - If account selected, retrieves valid accounts from HSAXIL1\n  - If cost center selected:\n    - If account not already selected, retrieves all cost centers\n    - If account selected, gets valid cost centers for that account from HSAXDL1\n- Allows user to page through selection list and pick value\n- Returns selected account or cost center value\n\n3. SFL1* - Selection list display logic\n- Clears (SFL1LOE)\n- Loads (SFL1LAD) \n  - Calls KSTSTSSR to check if filtering cost centers by account\n- Displays number of records (SFL1ANZ)\n- Handles selection and return to caller (SFL1AUSW)\n\n4. KSTSTSSR - Cost center filtering logic\n- If account passed, checks HSAXDL1 if only certain cost centers allowed for account\n- Sets indicator if all cost centers allowed or just certain ones\n\nThe program interacts with the following files:\n\n- HSAXIF - Main account and cost center file\n- HSAXIL1 - Account extract from HSAXIF \n- HSAXDL1 - Account/valid cost center relationship file\n\nAnd the following screens:\n\n- HS0617W1 - Main order entry screen\n- HS0617W2 - Selection list display\n- HS0617C1 - Selection list format\n\nIn summary, the key business logic is to validate account and cost center entries, optionally allow interactive selection, and restrict cost center selection by account if defined.","file_name":"HS0617.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code is for controlling the default workload codes (Belastungscode, BC) used for processing job times. The BC defaults are defined by categories:\n\n- Category A: Order \n- Category K: Customer\n- Category L: Service\n\nThe logic is:\n\n1. Category A overrides Categories K and L\n2. Category K overrides Category L \n3. Category L overrides the default BC (BCV010)\n\nAdditional logic:\n\n- If BC (BCS010) = K, then use customer-specific defaults --> No discount on wages\n- If BC (BCV050) = J, then billing rate can be changed + No discount on wages \n\nThe code contains procedures for:\n\n1. Converting strings to uppercase and lowercase\n\n2. Allocating and deallocating memory for a pointer variable\n\n3. Controlling BC default values:\n   - Adding a new BC default\n   - Changing an existing BC default\n   - Deleting a BC default\n   \n4. Checking if the job involves R&W split billing\n\n5. Protecting entries from central price control system (BC 9A-9Z) from being changed\n\nThe BC default values are stored in a file called HSBCSLR1.\n\nOther relevant files:\n- HSKUIPR: Customer master data\n- HSRZNPR: Service master data \n- HSBCSLR1: BC default values\n- HSBCSLR1: Central price control entries\n\nThe code interacts with these files to retrieve data for lookups and maintain the BC default values.\n\nNo specific UI or database interactions are coded. The lookups leverage built-in RPG functions for file I/O.\n\nIn summary, the key business logic is setting workload code defaults by category, with a hierarchy that allows higher categories to override lower ones. The code facilitates maintaining these defaults.","file_name":"HS0603.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code contains several procedures serving different purposes:\n\n1. Credit Limit Check for Sales Order\n\n- The program is called when creating or changing a sales order in Axapta. \n\n- It checks if the customer has a credit limit defined in Axapta.\n\n- It calculates the total outstanding invoices and open sales orders for the customer.\n\n- It retrieves any temporary credit limit overrides defined for the customer.\n\n- It calculates if the total outstanding amount exceeds the credit limit.\n\n- If the limit is exceeded, a warning is displayed to the user.\n\n- The program blocks creation of new sales orders that exceed the credit limit, if credit limit lock is activated in Axapta.\n\n- Exceptions can be defined per sales order to allow exceeding the limit.\n\n2. Credit Limit Monitoring\n\n- This procedure is called from a batch program HS06157.\n\n- It periodically checks for customers exceeding credit limits.\n\n- If limits are exceeded, warnings are logged and displayed to users entering new sales orders.\n\n- Warnings are only displayed once per user per sales order to avoid repetitive alerts.\n\n3. Credit Limit Warning Log\n\n- Warnings are logged to a file HSKLPF for audit purposes.\n\n- Log entries contain customer data, limit info, user, date/time etc.\n\n- The log provides a history of credit limit warnings.\n\n4. Temporary Credit Limit Extensions\n\n- Additional credit limit amounts can be defined in Axapta on a temporary basis.\n\n- If a temporary limit exists for the customer, it is used instead of the permanent limit.\n\n- This allows overriding the standard limit for a defined period.\n\n5. Credit Limit Exceptions\n\n- Exceptions can be defined per sales order to allow exceeding the credit limit. \n\n- They are checked before blocking sales orders exceeding the limit.\n\n- If an exception exists, the order can be created despite exceeding the limit.\n\nIn summary, the program implements comprehensive credit limit checking integrated with Axapta order processing. It provides warnings, blocking, logging and overrides to manage credit limits.\n\nThe code interacts with the Axapta database for:\n\n- Customer master data\n- Sales orders\n- Invoices\n- Credit limits and exceptions\n\nAnd additionally uses these files: \n\n- HSKLPF for logging warnings\n- Temporary tables HS0615S1, HSKLOF for calculations\n\nThe user interface consists of a display file HS0615D to show the warnings.","file_name":"HS0615.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis program checks if there is an active maintenance agreement (R&W-Vertrag) or an upcoming due date for a vehicle service. Based on the input parameters, it either displays an alert on the screen (HS0600) or calls the due date monitoring program (HS0650).\n\nKey steps:\n\n1. Check if a maintenance agreement record (RWVRILF4) exists for the vehicle (FGNR).\n   - If yes, set indicator 50 to show the alert on screen.\n   - If the agreement has expired, show additional alert text.\n\n2. Check the due date monitoring data (CTLHS3, CTLHS4):\n   - Get the due date interval (TAGEA) and convert it to days (TAGE). Default is 30 days if no interval.\n   - Get the current odometer reading (KM_AKT) from the vehicle master data (DG_KM). \n   - Add tolerance kilometers (KM_TOL) to the current reading.\n\n3. Read the upcoming due dates file (HSFZTPF):\n   - For each record, check if the due date or the odometer limit has been reached and the service is not marked completed.\n   - If yes, set indicator 51 to show the alert.\n   - Get the due date (FZT020) and description (FZT030) to display.\n   - Exit loop once first upcoming due date is found.\n\n4. Based on the parameters:\n   - If PGM called, start due date monitoring program HS0051.\n   - If ANZ called, display the alert screen HS0601W1 if R&W or due date exists.\n   - If RUE called, return indicator if a due date is approaching.\n\nFiles used:\n- RWVRILF4 - Maintenance agreement master data\n- CTLHS3, CTLHS4 - Due date monitoring control data\n- HSFZTPF - Upcoming due dates\n- Vehicle master data (FGNR)\n\nUI interaction:\n- HS0600 - Display alert screen\n- HS0650 - Due date monitoring program\n\nThis summarizes the key business logic extracted from the provided RPG code. It checks for due dates and maintenance agreements, retrieves the necessary data, and displays alerts or starts monitoring based on defined parameters. The code interacts with master data, control data, and transaction files as well as UI programs.","file_name":"HS0601.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- This code is for damage coding on work orders in a workshop management system. It allows entering damage codes by customer and workshop.\n\nKey Files:\n- AUFWKO: Work order header file\n- AUFWSK: Work order damage coding file\n- AUFWSKF: Damage coding file layout \n- CWPMSGF: CWP message file \n- CWPMSRF: CWP message relations file\n\nProcedures:\n\n1. SR_WSK: Displays and maintains damage coding screen\n- Clears damage coding subfile \n- Reads work order damage codes into subfile\n- Allows adding, changing and deleting damage codes\n- Validates codes against CWP message file\n- Displays related CWP messages as search help for codes\n- Writes changed codes back to AUFWSK file\n\n2. SR_HINZU: Adds new damage code\n- Validates code against CWP message file\n- Writes new code to AUFWSK file\n\n3. SR_AENDERN_K: Changes existing customer damage code\n- Validates changed code against CWP message file  \n- Updates code in AUFWSK file\n\n4. SR_AENDERN_W: Changes existing workshop damage code\n- Validates changed code against CWP message file\n- Updates code in AUFWSK file\n\n5. SR_LOESCHEN: Deletes existing damage code\n- Deletes code from AUFWSK file\n\n6. SR_MSG_ID_K: Validates customer damage code against CWP message file\n\n7. SR_MSG_ID_W: Validates workshop damage code against CWP message file\n\n8. SR_AUFPOS: Checks if damage code is assigned to a valid work order position\n\n9. SR_COD_POS: Checks for damage codes without positions\n\n10. SR_POS_COD: Checks for positions without damage codes\n\n11. SR_CODW_OK: Checks if workshop damage coding is complete\n\n12. SR_EPA_I: Displays related extended prices (EPS)\n\n13. SR_EPA_DEL: Deletes related EPS when damage code is deleted\n\n14. SR_JOB: Retrieves related work order job UUID \n\nIn summary, the code provides maintenance of damage coding on work orders, validating codes and related positions, with integration to CWP message file.","file_name":"HS0614.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe program allows managing workshop orders and contains the following key functionality:\n\n1. Check if a workshop order already exists and is active before allowing edits (SRACT routine). Prevent simultaneous editing by multiple users.\n\n2. Validate and update customer master data (KDUPD routine) including name, address, payment info etc. Write change history. \n\n3. Validate and update vehicle master data (FZUPD routine) including registration number, vehicle type, manufacture year etc. Update mileage history.\n\n4. Check for open campaigns related to the order and vehicle (SRKAM routine). \n\n5. Validate order header details like dates, times, vehicle info. Check date sequences are valid.\n\n6. Allow editing order text lines, inserting blank lines, positioning text etc. (ADTEXT routine).\n\n7. Allow entry of standard jobs/service items, checking validity, prices, discounts etc. (ADFEST routine).\n\n8. Calculate totals and taxes for jobs. Check credit limits. \n\n9. Allow entry of parts/accessories, checking stock levels and prices (SRPAK routine).\n\n10. Check if parts are under warranty (SR07 routine).\n\n11. Check upcoming maintenance appointments (SR08 routine).  \n\n12. Retrieve and display vehicle info from 3rd party system (SR20 routine).\n\n13. Print workshop orders and invoices (SRDRU routine).\n\n14. Interact with other systems: ERP (AXAPTA), Contracts (RWVRIPF), Campaigns (HS06090), Rental (MULTI.EXE) etc.\n\nThe program interacts with these files:\nHSFAIPF, FARSTAM, AUFWKO, AUFWAW, HSAKTLF1, HSBONPF, HSBSTL1, HSEPKPF, HSKAMPF, HSKUIPF etc.\n\nIt uses these keyed lists: \nKEYWKO, KEYWAW, KEYAGA, KEYEPK, KEYKEN, KEYKDR, KEYKDA etc. \n\nAnd contains these other notable routines:\nKOMMEN, KDUPD, FZUPD, SR05, SR14, SR19, INTPLAUSI, INTPLAUSIAX, SR_TEILE etc.\n\nIn summary, the core logic revolves around workshop order management and integration with surrounding systems. The code ensures data validity across the order lifecycle.","file_name":"HS0610.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program is designed to calculate and print wage supplements for mechanics on work orders when certain conditions are met.\n\nThe key steps are:\n\n1. Read work order header (AUFWKO) and wage supplement (AUFWAW) files by work order number (AUFNR), branch (BEREI), date (WETE), split (SPLITT).\n\n2. If work order status (WKO280) is not 'AV' (completed), skip processing. Also skip if work order is still open (WKO300 <> '00').\n\n3. Initialize wage supplement record (WAW) for each mechanic (WAWEGR='01') with default values.\n\n4. Zero out wage fields WAW160, WAW190, WAW110 for all mechanics to reset totals. \n\n5. Calculate total hours for all mechanics on work order (SUMME_H).\n\n6. For each mechanic, if wage code (WAW060) is labor (>'01') and supplement indicator (WAW230) is '1', check if supplement percentage (WAW170) > 0. \n\n7. Calculate supplement amount (ZUSCHLAG) by multiplying hours (WAW150) by supplement percentage (WAW170).\n\n8. Write wage supplement record (WAW) for each mechanic with supplement code (WAWZUS), hours (WAW100), amounts (WAW160, WAW190). \n\n9. Optionally calculate overtime wage supplement based on total PE hours.\n\n10. Delete any wage records (WAW) where net amount (WAW190) = 0.\n\n11. Write wage supplement report (AUFWAW).\n\nFiles used:\n- AUFWKO - Work order header\n- AUFWAW - Wage supplement \n- AUFWRZ - Wage line items\n\nThis program calculates wage supplements for mechanics on completed work orders based on hours worked and designated supplement percentage. The results are written to the wage supplement file and report.","file_name":"HS0604.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis code appears to be related to determining the last order number for a workshop manager in some kind of dealership system.\n\nThe main logic is:\n\n1. Open the FISTAM file for input.\n\n2. Read a record (FISTAR) from FISTAM into memory. \n\n3. Move the workshop manager ID (WERKME) into a field in memory (FIS250).\n\n4. Subtract 1 from another field in memory (FIS320).\n\n5. Move the result of the subtraction into the output parameter AUFNRL. This contains the last order number for the workshop manager.\n\n6. Close the FISTAM file.\n\n7. Set on the LR indicator.\n\nSo in summary, this code looks up the last used order number for a given workshop manager by:\n- Opening an order file \n- Reading a record\n- Extracting the workshop manager ID \n- Calculating the last order number by subtracting 1 from another field\n- Returning the last order number \n\nThe FISTAM file appears to be some kind of order file. The workshop manager ID and last order number are stored in fields in the records in this file.\n\nNo database interactions are indicated.\n\nThe only output is the last order number passed back in the AUFNRL parameter.\n\nLet me know if any part of the logic needs further explanation!","file_name":"HS0605.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program appears to be related to displaying blocked customer information in a workshop order management system.\n\nThe key steps are:\n\n1. Initialize variables and open files\n\n- DATEDIT(*YMD) sets date format to YYYYMMDD\n- Opens files FKUDSTAM, FHSKUILF1, FHSBTSPF, FHSBTSLF1 for input \n- Opens file FHS0611D for output\n\n2. Read customer master data (FKUDSTAM)\n\n- Chains to file FKUDSTAM using keys KZLZEN (customer number) and NUMZEN (sequential number)\n- Reads customer name into field HEINAM from file FHSBTSPF\n\n3. Read workshop order header data (FHSKUILF1) \n\n- Chains to file FHSKUILF1 using keys KZLZEN and NUMZEN\n- Reads blocking indicator KUI000\n\n4. Check blocking indicator\n\n- If KUI000 is not blank:\n   - Copy KUI000 to KUI000A\n   - Set indicator SPERRE_JA/SPERRE_NEIN based on blocking code in KUI070\n   - Write blocked customer data to output file FHS0611D\n\n5. Display results\n\n- If any records were written to FHS0611D:\n   - Set indicators to allow screen output\n   - Write output screen FHS0611C1\n   - Write printer output\n\nIn summary, this program reads customer and order data, checks for blocking codes, and writes any blocked customer records to an output file and screen. The focus is on identifying and reporting blocked customers.\n\nFiles used:\n\n- Input\n   - FKUDSTAM - Customer master file\n   - FHSKUILF1 - Workshop order header file \n   - FHSBTSPF - Name file\n- Output\n   - FHS0611D - Output file with blocked customers\n   - FHS0611C1 - Output screen\n\nLet me know if you need any clarification or have additional questions!","file_name":"HS0611.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis program is designed to adjust the productivity of technicians for actual billable hours when a new standard times routine is used. It is called by program HS0650 when BEL01B='03' or '05'.\n\nIt receives the following input parameters:\n- AUFNR: Order number \n- BEREI: Area (SC/SAAB)\n- WETE: Workshop counter\n- SPLITT: Split indicator\n- BEL01B: Transaction type \n\nThe program does the following:\n\n1. Checks if new standard times routine is active based on WKO280 value. If not, exits.\n\n2. Sums the standard times values (hours and amount) for the order from AUFWRZR file. \n   Validates that the totals are > 0.\n\n3. Sums the initially calculated productivities (hours and amount) for each technician from AUFWAR file. \n   Validates that the totals are > 0.\n\n4. Calculates the productivity percentages of each technician based on their share of the total initial hours and amounts.\n\n5. Calculates the share of the total standard times hours and amounts for each technician based on their productivity percentages.\n\n6. Adjusts the productivity statistics for each technician in HSMONPR and MONSTAR files by:\n   - Subtracting initial productivity values \n   - Adding the corresponding standard times values\n   - Based on the transaction type:\n     - BEL01B='03' (Invoice): Subtracts initial values, adds standard times values\n     - BEL01B='05' (Cancellation): Adds initial values, subtracts standard times values\n\nThis achieves the goal of adjusting the productivity values based on actual billable standard times, while retaining the share of each technician.\n\nThe program interacts with the following files:\n- AUFWKO: Order header file\n- AUFWRZ: Order standard times file \n- FISTAM: Date file\n- AUFWAW: Order initial productivity file\n- FMONSTAM: Technician date file\n- HSMONPF: Technician statistics header file\n- MONSTAR: Technician statistics detail file\n\nThe output of the program is the adjusted productivity statistics in HSMONPF and MONSTAR.","file_name":"HS0607.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis RPG program appears to be related to workshop orders and time tracking.\n\nThe main logic flow is:\n\n1. Check if worker hours are recorded for the order (variable EC = '01'):\n   - Read order details from file AUFWAR\n   - If hours exist (AGAMON > 0), set indicator ANTWH = 'J'\n\n2. Check if time stamps exist for the order (variable ZEF = 'J'):\n   - Build order key ABANUM from input parameters\n   - Read time stamp records from file LZABF0\n   - If records exist:\n     - Save start date/time (ABDATE/ABANFZ) \n     - Save end date/time (ABDATE/ABENDZ)\n\n3. Convert industry minutes to normal minutes:\n   - Call subroutine SRTIEF to convert start/end times\n   - Subroutine logic:\n     - Move input time to temp field\n     - Multiply minutes by 60 \n     - Divide seconds by 100 to get minutes\n     - Move result to output field\n\nThe program interacts with these files:\n\n- AUFWAR - Contains order details\n- LZABF0 - Contains time stamp records\n\nIt accepts these input parameters:\n- AUFNR - Order number\n- BEREI - Order section \n- WETE - Order type\n- SPLITT - Order split\n- AUFDAT - Order date\n- ANTWH - Indicator for worker hours\n- ZEFDATA - Time stamp start date\n- ZEFUHRA - Time stamp start time\n- ZEFDATE - Time stamp end date\n- ZEFUHRE - Time stamp end time\n\nAnd sets these output parameters:\n- ANTWH - Indicates if worker hours exist\n- ZEFDATA - Populated if time stamps exist\n- ZEFUHRA - Populated if time stamps exist \n- ZEFDATE - Populated if time stamps exist\n- ZEFUHRE - Populated if time stamps exist\n\nThe overall business purpose seems to be retrieving time details for a workshop order.","file_name":"HS0613.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis code appears to be validating payment guarantee and block indicators for a customer order in a workshop management system.\n\nIt does the following:\n\n1. Retrieves customer master data (KUIPF) and order header data (KUDSTAM)\n\n2. Validates the following business rules:\n\n- Check if payment guarantee indicator (KUI070) is set to 'S' \n\n- Check if payment guarantee valid to date (KUD470) and payment guarantee from date (KUD460) are not blank\n\n- Check if payment guarantee valid to date (KUD470) is less than or equal to today's date\n\n3. If any of the validations fail:\n\n- Call program HS0612W1 to display an error message\n\n- Set on the error indicator (LR)\n\nSo in summary, this code encapsulates business logic to validate payment guarantee data on a customer order, including:\n\n- Fetching relevant data from customer master and order header files\n- Checking if guarantee indicator is set  \n- Validating guarantee date range\n- Displaying error message if validations fail\n\nIt interacts with the following files:\n\n- KUIPF - Customer master file\n- KUDSTAM - Order header file\n\nAnd displays errors via program HS0612W1, which likely contains UI/messaging logic.\n\nThe core purpose is to enforce correct payment guarantee data on customer workshop orders before further processing.","file_name":"HS0612.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\n1. String Conversion Procedures\n\n- toUppercase: Converts a given input string to uppercase using the `%xlate` built-in function.\n\n- toLowercase: Converts a given input string to lowercase using the `%xlate` built-in function. \n\n2. Memory Management Procedures \n\n- allocSpace: Allocates or reallocates memory for a pointer variable based on the given size. Checks if pointer is null, allocates new space if so, else reallocates existing space.\n\n- deallocSpace: Deallocates memory for a given pointer if not null.\n\n3. Work Order Processing\n\n- Reads work order details like customer number, work order number etc from database files. \n\n- Calculates package totals, discount amounts etc and writes them to output files.\n\n- Reads parts data, calculates totals, updates parts inventory files.\n\n- Reads labor data, calculates totals, assigns technicians, updates technician files.\n\n4. Transaction Logging\n\n- Logs parts transactions like issues, returns etc to transaction file with details like date, customer, part no, quantity etc.\n\n5. Date/Time Utilities\n\n- Procedures to retrieve current date and time and format it.\n\nThe code interacts with various database and interface files like work orders, inventory, labor, transactions etc. It contains procedures to perform business functions like work order costing, parts management, labor assignment and logging.","file_name":"HS0606.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nOverall purpose:\n- This program allows maintaining workshop hours and standard times for vehicles. It handles adding/updating technicians' hours, multi-purpose hours, assigning standard times to jobs, applying discounts etc.\n\nKey functions:\n1. Add/update technicians' hours (P001)\n- Allows adding a new technician to the job by entering details like name, hours, billing rate etc. \n- Updates the technician hours data (AUFWAR, HSMONPR, MONSTAR files).\n- Applies wage group based discounts if defined.\n\n2. Add/update multi-purpose hours (P002)  \n- Handles adding new standard time codes and hours under multi-purpose.\n- Saves the standard times in a temporary file (HSRZAPF).\n- Retrieves the descriptions etc. from standard time code files. \n- Updates the multi-purpose hours in AUFWAR file.\n\n3. Assign standard times (P008, P048)\n- Displays list of unassigned standard times.\n- Allows assigning them to technicians.\n- Updates AUFWAR, MONSTAR and HSMONPR files.\n\n4. Edit/delete technician and multi-purpose hours (P004, MONDLT)\n- Marks the records for deletion.\n- Handles deleting hours from AUFWAR and updating MONSTAR, HSMONPR files.\n\n5. Apply discounts:\n- Based on wage groups (HS0095)\n- Special discounts like for daughter companies (SR_WRZ160) \n- EPS discounts (WRZ200/210)\n\n6. Validation and controls:\n- Credit limit check (SR_LIMIT)  \n- Validation for hours entered (PRUEF)\n- Checking if technician exists etc.\n\n7. User interface:\n- Multiple subfile views for hours (SRSFL5)\n- Switching between workshops/technicians and standard times screens (VIEW)\n- Guiding user through screens (SR04)\n\nFiles used:\n- AUFWAR, AUFWAW, AUFWKO etc - Work order files\n- HSMONPR, MONSTAR - Technician master files\n- HSRZIPF, HSRZTPF etc - Standard time master files\n\nSo in summary, it allows maintaining the time and billing related data for jobs, applying discounts, guiding the user through the process and doing necessary validations.","file_name":"HS0608.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThis RPG program appears to be related to managing workshop orders, campaigns, and timesheets. The key functions include:\n\n1. Processing workshop orders (AUFWKR)\n- Read order details like customer, date, etc\n- Calculate billing rate based on order type \n- Add records to output files/subfiles for display\n\n2. Managing campaigns (HSKAMPR, S7F001)\n- Check for open campaigns for a workshop order \n- Allow adding/deleting campaigns \n\n3. Managing timesheet data (AUFWKLR, AUFWKTR, HSMONPR)\n- Read and display timesheet records per order \n- Allow assigning technicians and hours to campaigns\n- Validate hours entered against technician capacity\n- Update technician capacity totals\n- Calculate billing amounts\n\n4. Updating inventory (TEISTAR, TRANSPR)\n- When parts used on a campaign, update inventory transactions\n\n5. Reporting \n- Multiple subfile displays for orders, campaigns, timesheets\n- Allow updating of campaign details and technician notes\n\nThe code interacts with these files:\n- FISTAM: Customer master file\n- AUFWKR/AUFWKLR/AUFWKTR: Order/timesheet/parts usage details\n- HSKAMPR: Campaign master file \n- HSMONPR: Technician master file\n- TEISTAR: Inventory master file\n- TRANSPR: Inventory transactions file\n\nThe subfile displays and file I/O indicate this is an interactive green-screen application, likely for use in a workshop office.\n\nPlease let me know if any additional information on the business logic would be helpful!","file_name":"HS0609.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- The code is for an application called SDPS-ZENTRAL used in the workshop area of SCANIA DEUTSCHLAND.  \n- It allows changing the parts prices and discounts on stored workshop orders.\n- Changes are only possible if the order status (WKO300) is blank, 00 or 02 (KV).\n\nMain logic:\n1. Check user authority to change prices/discounts based on user ID.\n2. Initialize variables, open files, clear screens.\n3. Retrieve open workshop orders and display in subfile.\n4. Allow changing part prices, discounts, positions, descriptions on orders via subfile.\n5. Protect part descriptions for SDE/subsidiaries. \n6. Protect positions for EPS orders.\n7. Update prices/discounts in database if changed in subfile.\n8. Write changed order data back to database.\n9. Log changes made to orders. \n\nInterfaces:\n- Database files:\n  - AUFWKO - Workshop orders\n  - AUFWTE - Parts on workshop orders\n  - HSAKTLF1 - Change log\n  - HSEPKPF - User IDs\n  - Other pricing/discount files\n  \n- Screens:\n  - HS063501 - Main screen \n  - HS0635C1 - Parts subfile\n\nThe code interacts with the database to retrieve, update and log changes to workshop order pricing data based on user input on the screens. It contains authorization checks, file I/O, calculations, screen handling and logging. The core tasks are order price/discount updates and protecting key data fields.","file_name":"HS0635.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code appears to perform validation on sales order dimensions entered by a user when creating a sales order in the SDPS-2000 system. \n\nIt checks the following:\n\n1. Branch (BRANCH)\n- Ensure a branch is entered\n- Validate the entered branch code against a branch master data table (AXAXTLF2)\n\n2. Account (KTO) \n- Ensure an account is entered\n- Validate the account against a split account master data table (HSAXIF) to ensure it is allowed for the sales order split\n\n3. Cost Center (KST)\n- Ensure a cost center is entered  \n- Validate cost center against master data (HSAXIF)\n- Validate combination of account + cost center against account/cost center split mapping table (HSAXDL1) \n\n4. Individual Number (KTR)\n- Validate based on whether system is configured to require (CTLHS6 indicator)\n- Check for blanks if required\n\n5. Product Code (PRDCODE)\n- Validate based on whether system is configured to require (AXD_PRD indicator) \n- If entered, validate against product master data table (AXDIMPF)\n\n6. Special Code (SPZCODE)\n- Validate based on whether system is configured to require (AXD_SPEC indicator)\n- Special case to allow blank for a specific account + cost center + split + special code combination\n\nIf any validation fails, a return code (FEHLCODE) is set that can be used by the calling program to determine which dimension validation failed.\n\nThis program validates sales order dimensions against master data to ensure splits are mapped to valid account/cost center combinations. It is likely called when a sales order is created or changed in SDPS-2000.\n\nThe code interacts with these files:\n- AXAXTPF: Branch file\n- AXAXTLF2: Branch/Plant file\n- HSAXIF: Split mapping file\n- HSAXDL1: Account/Cost Center split mapping file \n- AXDIMPF: Product master data file\n- CTLHS6: Configuration/Control file","file_name":"HS0618.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverall Program Functionality:\n- Allows changing various details of an existing work order, including split, invoice recipient, discount code.\n- Validates changes and updates work order header record (AUFWKR). \n- Propagates changes to related detail records like work steps (AUFWAR), parts (AUFWTR), etc.\n- Records change history for auditing.\n\nSplit Change:\n- Input required: Work order number, Area, From Split, To Split\n- Validates work order exists and new split is allowed based on contract.\n- Validates no order blocks exist for new split and customer.\n- Updates work order header with new split.\n- Copies over work step and part records from old to new split.\n- Rates new split based on customer/contract. \n- Records change history.\n\nInvoice Recipient Change: \n- Input required: Work order number, Area, Split, New Customer Number\n- Validates work order exists and new customer is valid.\n- Validates split alignment between existing order and new customer.\n- Updates work order header with new customer details.\n- Rerates order based on new customer/contract.\n- Records change history.\n\nDiscount Code Change:\n- Input required: Work order number, Area, Split, New Discount Code\n- Validates work order exists and new code is valid.\n- Updates work order header and rerates all work steps and parts using new code. \n- Records change history.\n\nThe program interacts with these files:\n- AUFWKO: Work Order Header\n- AUFWAR: Work Steps\n- AUFWTR: Parts\n- AUFWKR: Work Order Contract\n- KUDSTAM: Customer Master\n- HSAKTLF1: Change History\n\nAdditional functionality exists for:\n- Viewing open orders\n- Splitting based on packages\n- Updating technician statistics\n- Validation against AXAPTA","file_name":"HS0640.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nThe code implements functionality to generate electronic invoices in XRechnung XML format. \n\nKey aspects:\n\n1. It can generate invoices from different sources:\n- Service invoices (SPAS) based on data from ITPINVH table\n- Repair shop invoices (WT) based on data from HSAHKPF/HSAHTPF/HSAHWPF/HSAHPPF tables  \n- Manual invoices based on data from AXMRKPF table\n\n2. It retrieves all relevant data like customer info, addresses, payment terms etc. from various tables.\n\n3. It dynamically builds the XRechnung XML structure and populates it with the invoice details.\n\n4. The XML generation involves:\n- Setting up the XML header with metadata like invoice date, type etc.\n- Adding billing and shipping address details under Party nodes\n- Adding invoice lines for parts, labor etc. under InvoiceLine nodes  \n- Calculating totals like line amounts, taxes etc. under TaxTotal and LegalMonetaryTotal nodes\n\n5. The generated XML file is then exported and optionally sent to the customer.\n\n6. There is also dialog functionality to enter invoice details manually.\n\n7. Additional procedures handle utility tasks like data retrieval, string formatting, date calculations etc.\n\nSo in summary, it is an invoice generation application focused on creating XRechnung compliant XMLs from various data sources and business contexts. The core functionality is the flexible and dynamic construction of the XML structure using RPG code.\n\nRelevant files:\n- ITPINVH - Service invoice header\n- HSAHKPF - Repair shop invoice header \n- AXMRKPF - Manual invoice header\n- BSPCUST - Customer master data\n- FISTAM - Biller master data\n\nThe application interacts with these files and DB2 tables to generate the end XML document.","file_name":"HS0654.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis appears to be an RPG program for displaying workshop orders. The key functions include:\n\n1. Displaying workshop orders\n- Allows displaying all workshop orders, only open orders, or orders for the current date\n- Displays details like order number, customer number, vehicle number, status etc in a subfile\n- Handles pagination and navigation of the subfile\n\n2. Lookup by customer number\n- Allows searching for orders by customer number using a matchcode\n- Displays matching orders in a subfile\n- Allows selecting a customer to filter orders\n\n3. Lookup by vehicle number  \n- Allows searching for orders by vehicle/chassis number\n- Displays matching orders in a subfile\n- Allows selecting a vehicle number to filter orders\n\n4. Lookup by repair code\n- Allows searching for orders by repair code \n- Displays matching orders in a subfile\n- Allows selecting a repair code to filter orders\n\n5. Display order details\n- Shows additional details for a selected order in subfiles\n- Displays order header, parts, labor, packages etc.\n- Calculates net values for parts and labor\n\n6. Integration with other programs/files\n- Reads data from workshop order (AUFWKR), customer (KUDSTAR), vehicle (HSFAILR), and other files\n- Calls other programs like HS0062C to retrieve archived data\n\nThe code interacts with display files like HS068000 for user interface. It handles subfile operations for output display. There is also some logic for handling pricing and totals.\n\nOverall, this program allows users to search, view and analyze workshop orders in an interactive manner by integrating with other programs and data files in the system. The business logic centers around order inquiry, lookup and display functions.","file_name":"HS0680.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code is for printing a repair order document.\n\nDatabase Files:\n- HSAHWPF - Header work order file\n- HSAHTPF - Header parts file \n- HSAHPPF - Header package file\n- HSBTSLF1 - Form file\n- HSFZTLF4 - Inspection deadline file\n- HSLAEPF - Country file\n- HSKUIPF - Customer master file  \n- KUDSTAM - Dealer master file\n\n1. Main logic:\n- Read input parameters - repair order details like order number, date etc\n- Open output spooled file for printing\n- Call procedure to print document header \n- Call procedure to print order lines\n- Call procedure to print parts\n- Call procedure to print packages\n- Close output file\n\n2. Print document header:\n- Initialize printer page count\n- Get customer details by chaining on order header record\n- Build customer address strings\n- Get order date details \n- Get inspection deadline details by chaining\n- Get UID/tax ID details by chaining to customer and dealer master records\n- Write header details to output file  \n\n3. Print order lines:\n- Declare cursor on order lines file\n- Fetch order line records \n- Check for new position number \n- If new position, print position total for previous position\n- Print line details for each order line record fetched\n\n4. Print parts:\n- Declare cursor on parts file\n- Fetch part records for current position\n- Print each part record details\n\n5. Print packages:\n- Declare cursor on packages file \n- Fetch package records for current position\n- Print each package record details\n\n6. Utility logic:\n- Format customer address strings\n- Increment line counter and check page overflow\n- Print document header on new page\n\nThe code handles printing of the work order document by retrieving and formatting data from the related database files.","file_name":"HS0652.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverall Program Logic:\n- The program allows managing purchase orders and related services/items. It interfaces with AXAPTA for some validations.\n\nMain Procedures:\n\n1. CheckAuthority: Checks if the user has authority to access the program functions.\n\n2. SFLLOE: Clears the display files. \n\n3. SFLFUE: Populates the display files with data from database files for initial display. Filters data based on date range.\n\n4. VIEW_C1: Writes service description details to display file in C1 format. \n\n5. VIEW_C3: Writes purchase order header details to display file in C3 format.\n\n6. AUFKUD: Retrieves purchase order and customer details for a service. Checks if purchase order is open, invoiced or cancelled.\n\n7. STATUS_FL: Determines service line item status based on conditions.\n\n8. STORNO_FL: Performs cancelation of service line item.\n\n9. AUFRECH: Displays purchase order or invoice details. \n\n10. BESNEU: Allows creation of new purchase order or editing existing one. Retrieves supplier details. Interfaces with AXAPTA for validations.\n\n11. LEISNEU: Allows creation of new service line item. Interfaces with AXAPTA for credit limit check.\n\n12. ANSCHRIFT: Builds address blocks for supplier and delivery addresses.\n\n13. SR_EINKAUF: Builds text blocks for terms and conditions.\n\n14. DRUCKBS: Prints purchase order.\n\n15. TXTZEILEN: Allows maintaining number of text lines per service.\n\n16. DETAILS: Displays and allows editing service line details like pricing and invoice details.\n\n17. RWCHEK: Checks if service is R&W split type. \n\n18. STATUS_KL: Determines service and purchase order status text. \n\n19. WRITE_FLB: Writes new or updated purchase order to file.\n\n20. WRITE_FLA: Writes new or updated service line item to file.\n\n21. UPDATE_FLB: Updates existing purchase order header record.\n\n22. PLAUSI: Performs various validity checks.\n\n23. PLAUSI_AXA: Does additional validity checks by interfacing with AXAPTA. \n\n24. BEDIENER: Allows input prompts and lookups via F4 function key.\n\n25. SR_SPERRE_L: Checks for supplier blocking.\n\n\nDatabase Files Used:\n\n- HSBTSLF1: Company file\n- AXAXTPF: AXAPTA company file\n- AXAXTLF2: AXAPTA company branch file \n- FAXDIMPF: AXAPTA dimensions file\n- HSBNDDIR: Binding directory\n- HSFLBPF: Purchase order file\n- HSFLAPF: Purchase order line file \n- HSFLTPF: Purchase order line text file\n- HSFLLLF1: Service codes file\n- HSANSPF: Consultants file\n- LIFSTAM: Supplier master file \n- FHSLAEPF: Country codes file\n- FKUDSTAM: Customer master file\n- FHSKUIPF: Customer alternate delivery addresses\n- FHSNRKPF: Purchase order number range file\n- FHSAHKLF3: Invoice file\n- FAUFWKO: Shop order file \n- FRWVRILF5: R&W contracts file\n- FFLBEST: Print file purchase order\n- HS0646S1: Display file 1 \n- HS0646S3: Display file 3\n\nThe program contains extensive validation logic, interactions with AXAPTA as well as printing functions related to managing purchase orders and related services/items.","file_name":"HS0646.txt"},

{"logic":"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- This program generates an XML e-invoice file for a given invoice number based on data from various database files.\n\nMain functions:\n1. Initialization\n   - Get invoice number and date from input parameters or by looking up based on user id.\n   - Determine invoice type based on invoice number prefix.\n   - Initialize filename, timestamp etc.\n\n2. Get invoice header details\n   - Get invoice header record based on invoice number/date.\n   - Get customer data from invoice header.\n   - Determine document type (Invoice/Credit Memo).\n   - Get contact and address info for biller based on dealer id.\n\n3. Get invoice line details\n   - For workshop and counter invoices, get parts, labor, packages from related database files. \n   - For manual invoices, get details from invoice item file.\n\n4. Generate XML \n   - Output XML header with invoice metadata.\n   - Add invoice recipient, biller, line items, totals etc. as XML elements.\n\n5. Write payment info\n   - If blank direct debit, output bank details for biller.\n   - If direct debit info present, add direct debit XML element.\n\n6. Export XML file\n\nDatabase interactions:\n- Read invoice header (AHK) and related detail records (AHT, AHW, AHP)\n- Read manual invoice header (MRK) and detail (MRP) records  \n- Read dealer contact info (ANS)\n- Read customer direct debit preference (KUI) \n- Write generated XML to IFS file\n\nUI interactions:\n- Prompt for missing invoice number if not passed as parameter\n\nThe program generates an e-invoice XML file by extracting data from the database based on a given invoice number. The core logic involves assembling XML elements by pulling data from various sources like invoice header, line items, customer info etc.","file_name":"HS0653.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThis RPG program appears to be for processing active work orders in a workshop management system.\n\nMain logic:\n\n1. Call program HS0013 to check for inactive jobs and automatically delete them from the HSAKTPF file. This keeps only active jobs.\n\n2. Clear the subfile (SFL) S1. \n\n3. Read records from the HSAKTLR1 file into the SFL S1 to display active work orders.\n   - The key fields for HSAKTLR1 are AKT01X and AKT02X.\n   - Loop through HSAKTLR1 records with AKT013='1' (active flag). \n   - Move work order number (AKT010) to AKT01X and work order description (AKT020) to AKT02X.\n   - Write records to the SFL S1.\n\n4. If no records found, add a blank record to SFL S1 indicating 'NO ENTRIES'.\n\n5. Display the SFL S1 subfile on the screen.\n\n6. Allow option to refresh subfile or exit program based on user input.\n\nFiles used:\n\n- HSAKTLF1 - Main file for active work orders\n- HSAKTLR1 - Read format of HSAKTLF1 for subfile\n- HS0690S1 - Subfile for display (SFL)\n\nAdditional details:\n\n- Program is designed to run interactively on a workstation.\n- Allows viewing and working with active workshop work orders.\n- Appears to be part of an ERP or workshop management system.\n- Includes header comments indicating it is for SCANIA Deutschland.\n\nIn summary, the key business logic revolves around displaying active work orders in a subfile for a workshop management system. Let me know if any part needs further explanation or clarification.","file_name":"HS0690.txt"},

{"logic":"Here are the key points extracted from the RPG code provided:\n\n1. This program is for managing external services (Fremdleistungen) for the workshop. It allows capturing, displaying, printing, and invoicing external services.\n\n2. An external service can be ordered at full tax rate or reduced tax rate. Mixed tax rate orders are not allowed. \n\n3. An external service order can have 3 statuses:\n   - Blank = Order placed with supplier\n   - 1 = Released for invoicing to customer\n   - 2 = Not yet invoiced to customer and cancelled. Data is retained.\n\n4. The program allows searching for external services based on various criteria like vehicle number, order number, order date etc.\n\n5. For a new external service order:\n   - The supplier master data is selected first\n   - Required details like customer order no, item text, prices etc. are entered\n   - System generates an external service order number\n   - The order can be printed\n   - The order is saved in the external service header (HSFLKPF) and item (HSFLPPF) files\n   - The status is updated in customer order header file (AUFWKO)\n   \n6. To invoice an external service:\n   - The status is changed to 1 in HSFLKPF file\n   - The counters are updated in AUFWKO file\n   - The price is moved to the WAW file\n   \n7. To cancel an external service:\n   - The status is changed to 2 in HSFLKPF\n   - Corresponding entries in WAW file are deleted\n   - Counters in AUFWKO are decremented\n   \n8. The program interacts with the following files:\n   - HSFLKPF - External service header file\n   - HSFLPPF - External service item file \n   - AUFWKO - Customer order header file\n   - AUFWAW - Customer order item file\n   - FISTAM - System settings file\n   - AGASTAM - Work order file\n   \nIn summary, the key functionality includes managing the entire lifecycle of an external service order - from creation to invoicing or cancellation. The status and counts are maintained across multiple files for consistency.","file_name":"HS0645.txt"},

{"logic":"Here is the extracted business logic from the provided RPG code:\n\nThe code contains several procedures, each serving a specific purpose:\n\n1. Process invoice/credit note document\n   - Read order header (AUFWKO) and item details (AUFWAW, AUFWTE etc)\n   - Determine document type (invoice, credit note etc) and split\n   - Calculate totals like net amount, VAT etc.\n   - Print invoice/credit note with header, item details, totals\n   - Generate PDF and/or print document\n   - Email PDF based on customer email address\n   - Archive document\n\n2. Print job descriptions (AUFJOB)\n   - Read job header (job alias) and details\n   - Print job descriptions under separate item positions\n\n3. Determine VAT portion (SCAS)\n   - Read SCAS invoice header (HMSCSCPR) \n   - Read SCAS invoice lines with VAT details (SCAXOPR)\n   - Calculate VAT portion\n   - Consider reversal on credit notes\n   - Validate VAT percentage \n   - Add up applicable VAT amounts\n\n4. Lookup customer master data (KUDSTAM)\n   - Get customer name, address etc.\n   - Determine country, VAT ID\n   - Get email address for PDF sending\n\n5. Lookup text modules (TEXSTAR)\n   - Retrieve text lines for headers, footers etc. \n   - Format text lines to defined length\n\n6. Lookup campaigns (AUFWKKR)\n   - Retrieve campaign details \n   - Print as information on invoice\n\n7. Lookup appointments (HSFZTLR4)\n   - Get upcoming appointments of specific types\n   - Print on invoice\n   \n8. Lookup vehicle master data (FARSTLR4)\n   - Get phone numbers of vehicles\n   - Print on invoice\n   \n9. Direct debit details (AX1230)\n   - Provide invoice data\n   - Retrieve direct debit details like date, mandate reference etc.\n   - Print direct debit notice on invoice\n\n10. Tyre label data (HS03102)\n    - Pass invoice data \n    - Lookup tyre label details\n    - Print on invoice\n    \n11. Control invoice output\n    - Check if email PDF, print or both\n    - Consider batch/dialog mode\n    - Handle different document types\n    - Set PDF subject, recipient etc.\n\nThe code interacts with these files:\n\n- Work order files like AUFWKO, AUFWAW\n- Master data files like KUDSTAM, TEXSTAR  \n- EDI files like SCAS EDI invoice data\n- Appointment data HSFZTLR4\n- Vehicle data FARSTLR4 \n- Campaign data AUFWKKR\n- Tyre label data HS03102F\n- Direct debit data AX1230\n- Output control data like CTLHS7, email addresses etc.\n\nIt generates output in these forms:\n\n- Printed invoice/credit note\n- Email with PDF invoice/credit note attached\n- Direct debit notice printed on invoice\n- Archive copy of invoice/credit note\n\nThe business logic handles different document types like invoice, credit note, proforma etc. It also supports VAT handling for domestic, EU and non-EU transactions.","file_name":"HS0651.txt"} 
]

def process_folder_06N(parent_folder_id):    
    
    folder_name = "Customer"
    folder_business_logic = ""
    
    folder_structure={"files":["HS0649.txt","HS0660.txt","HS0670.txt","HS0602.txt","HS0616.txt","HS0617.txt","HS0603.txt","HS0615.txt",
                               "HS0601.txt","HS0600.txt","HS0614.txt","HS0610.txt","HS0604.txt","HS0605.txt","HS0611.txt","HS0607.txt",
                               "HS0613.txt","HS0612.txt","HS0606.txt","HS0608.txt","HS0609.txt","HS0635.txt","HS0618.txt","HS0640.txt",
                               "HS0654.txt","HS0680.txt","HS0652.txt","HS0646.txt","HS0653.txt","HS0690.txt","HS0645.txt","HS0651.txt"]}
    files_name=[]
    for file in business_06N:
        if(folder_business_logic==""):
            folder_business_logic=file["logic"]
            files_name.append(file["file_name"])
        else:
            folder_business_logic = combine_business_logic(folder_name,folder_structure,files_name,folder_business_logic,file["file_name"],file["logic"])
            files_name.append(file["file_name"])
    
    logic = folder_business_logic
    return logic

class HigherLevelBL06N(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request):
        start_time = time()
        folder_id = request.data.get('id')
        business_logic = process_folder_06N(folder_id)
        end_time = time()
        elapsed_time = end_time - start_time 
        response_data = {
            "response": business_logic,
            "elapsed_time_seconds": elapsed_time
        }
        return Response(response_data, status=200)







# Customer Search Higher Level Business Logic, Mermaid Diagram and Mermaid Flowchart

business_logic_customer={
    
'HS0238.txt': "Here is the business logic extracted from the provided RPG code:\n\n1. Program Purpose:\n- This program is for customer master search and duplicate check. It allows searching for customers by various criteria like name, address, postcode etc. and shows search results in a subfile for selection.\n\n2. Input Parameters:\n- KZL (char 3): Branch number \n- KDNR (char 6): Customer number\n- KDMC (char 5): Program to call for details\n- RET (char 3): Return code \n\n3. Global Data Structures:\n- MATCHID (char 6): Matchcode value\n- DDUKPLE (char 5): Search criteria - postcode range\n- §RETURN (char 3): Return code\n\n4. Main Procedures:\n\n4.1 Initial Setup:\n- Initialize variables, subfile etc.\n- Read user profile for allowed branches\n- Set initial sort order and search criteria\n\n4.2 Search:\n- Based on input criteria, search by postcode range or matchcode\n- For postcode: Read postcode file, find matching addresses\n- For matchcode: Find matching customer numbers \n\n4.3 Selection Display:\n- Show results in subfile\n- Allow changing sort order and search criteria\n- On selection, return customer number and branch \n\n4.4 Subroutines:\n\n- SFLLOE: Clear subfile\n- PLZ: Build subfile by postcode\n- MATCH_KUD: Build subfile by matchcode on customer number\n- MATCH_KUI: Build subfile by matchcode on alternative customer number\n- FUELS1: Fill subfile with address details\n- SR16: Change sort order\n- TRIMBL: Remove blanks from search fields\n\n5. Called Programs/Files:\n- KUDSTAM: Customer master file\n- KUDSTLFF: Postcode file\n- HSKUILF1: Alternative customer number file\n- HSBTSLF1: User profile file\n\nSo in summary, this is an interactive search program for the customer master file allowing flexible search criteria and subfile display of results.",

'HS0900.txt': "Here is the extracted business logic from the provided RPG code:\n\nThis appears to be an RPG program for searching and displaying customer information based on search criteria entered by the user.\n\nThe key steps are:\n\n1. Initialize data structures and variables \n\n2. Read search criteria entered by the user:\n    - Customer number (KDNR)\n    - Zip code (DUKPLE) \n    - Street (DUKSTR)\n    - City (DUKORT) \n    - First name (DUKNA1)\n    - Last name (DUKNA2)\n\n3. Clear previous search results from subfile (HS0900S1)\n\n4. Read customer master file (HSKUIPR)\n    - Validate record is not blocked (KUI070 <> 'S') \n\n5. For each customer record:\n    - Convert search criteria and master file fields to uppercase for comparison\n    - Check if search criteria matches customer fields\n        - Zip code (DUKPLE = KUD080)\n        - Street (DUKSTR scans KUD060)\n        - City (DUKORT scans KUD090)\n        - First name (DUKNA1 scans KUD030)\n        - Last name (DUKNA2 scans KUD040)\n    - If all criteria match, write customer to output subfile (HS0900S1)\n\n6. If no records match, indicate no records found\n\n7. Display subfile to user (HS0900C1)\n\n8. When user selects a record:\n    - Retrieve customer number (KUI010)\n    - Exit program\n\nThis program interacts with the following files:\n\n- HSKUIPR - Customer master file (input) \n- HS0900S1 - Output subfile with search results\n- HS0900C1 - Format for displaying subfile\n\nThe user interface consists of:\n\n- HS0900W2 - Input search criteria screen\n- HS0900C1 - Output subfile display\n\nIn summary, this is an interactive customer search program that allows users to search for customers based on various criteria and displays the matching results in a subfile for selection.",

'HS0815.txt': "Here is the business logic extracted from the provided RPG code:\n\nThis RPG program appears to be part of an automotive dealer system for Scania. The main functions are:\n\n1. Customer Search\n- It calls another program HS0238 to search for a customer by customer number (RE1100). \n- The search criteria includes customer number (RE1100), clearing center (HS815), and clearing number (§KDNR).\n- The result is returned in §KDNR.\n\n2. Invoice Processing\n- It can process invoices by invoice number (RE1050) or by customer number (RE1100).\n- Invoice details like invoice date (RE108x), totals (RE106x) are moved to output files.\n- Output file HS0815S1 contains invoice header details.\n- Output file HS0815S2 contains invoice line details like quantity (RE2100), net amount (RE2110), VAT amount (RE2120). \n\n3. Display Invoices\n- Invoices from HS0815S1 and HS0815S2 are displayed after writing to output files.\n- Invoice selection happens based on user input.\n- Selected invoice details from HS0815S1 and HS0815S2 are shown in display files HS0815C1 and HS0815C2.\n\nIn summary, this RPG program enables search for customers, processing of invoice documents, and displaying invoices in an automotive dealer system.\n\nThe key files used are:\n\nInput Files:\n- HS0815S1 - Invoice Header\n- HS0815S2 - Invoice Lines\n\nOutput Files: \n- HS0815C1 - Invoice Header Display\n- HS0815C2 - Invoice Lines Display\n\nOther Files:\n- HS0238 - Customer Search Program\n- RE1SULF1 - Invoice Header Work File\n- RE1SULF3 - Invoice Header Work File \n- RE2SUM - Invoice Lines Work File\n\nThe program allows processing invoices either by invoice number or customer number as input.",

'HS06009.txt':"Here is the extracted business logic from the provided RPG code:\n\nOverall purpose: This RPG program interacts with the Service Delivery Planning System (SDPS) to retrieve and display draft vehicle work orders for selection and further processing in SDPS.\n\nKey steps:\n\n1. Initialize\n   - Set date format to ISO\n   - Get site ID (kzlb) and description (kzlf)\n   - Define temporary storage for work order data (#sel1, Rec_#d) \n   \n2. Get draft work orders\n   - Build SQL statement to select draft work orders (#sel1)\n   - Execute SQL to populate work order details (Rec_#d)\n   \n3. Display work orders\n   - Write work order details from SQL to display file (HS06009S1)\n   - Allow searching/filtering records\n   - Page through results\n   \n4. Select work order\n   - When option 1 chosen, pass work order ID and other details to SDPS using parameter list\n   - This triggers subsequent processing of selected work order in SDPS\n   \n5. Additional logic\n   - Customer name lookup using multiple files (HSFAIPF, FARSTAM, HSKUIPF, KUDSTAM)\n   - Search logic:\n      - Convert input to uppercase\n      - Remove spaces\n      - Match against multiple fields\n   \n\nKey files:\n\nInput: \n- WOPWOF - Work order file\n- HSFAIPF - Partner file\n- FARSTAM - Partner role file \n- HSKUIPF - Customer file\n- KUDSTAM - Customer role file\n\nOutput:\n- HS06009S1 - Display file for work order selection\n- DD§PWO - Parameter list passed to SDPS\n\nThe program facilitates work order selection from Digital Dealer and transfer to SDPS for further processing. Key steps include SQL retrieval of open work orders, interactive search/select, and passing of selected order details to SDPS. Additional logic handles lookup of customer data from various source files.",

'HS1061.txt':"Based on the provided RPG code, here is the extracted business logic along with the related files, databases and UI:\n\nThe code represents a program named HS1061 that performs customer/supplier/vehicle selection for letter writing in the SDPS-2000 application.\n\nKey Business Logic:\n\n1. Allow selecting customers, suppliers or vehicles based on various criteria like number range, search text, sales rep, etc. \n\n2. Build selection criteria SQL statements dynamically based on input parameters.\n\n3. Call HS1061C program after building selection criteria to retrieve selected records.\n\n4. Write selection criteria to database file HSBRSPF/HSBRSPR. \n\n5. Selection can be done for:\n   - Customers (BEREICH = 'KUD')\n   - Suppliers (BEREICH = 'LIF')  \n   - Vehicles (BEREICH = 'FZA')\n\nRelated Files:\n\n1. HSBRSPF/HSBRSPR - Database file to store selection criteria\n\n2. HSBTSLF1 - Database file that contains dealer short code\n\n3. S7L011A - Database file that contains open campaigns (for vehicles selection) \n\nUI Interaction:\n\n1. Program displays selection screens HS10610x to get input parameters\n\n2. Selection results are shown in grid to user\n\n3. User can select records and press F1 to call letter writing program HS1062C\n\nIn summary, the core logic is to provide selection capabilities for master data (customers, suppliers, vehicles) based on flexible criteria provided through selection screens. The results can then be consumed for downstream processing like letter writing.",

'HS0870.txt':"Here is the business logic extracted from the provided RPG code:\n\n1. The program allows selecting and analyzing order/invoice data based on various criteria like customer number, order number, invoice number etc.\n\n2. It provides two different views for the selection results - View 1 shows workshop orders/invoices and View 2 shows service counter orders/invoices. \n\n3. The selection criteria include:\n   - Order/Invoice number\n   - Order/Invoice date \n   - Order number\n   - Order date\n   - Matchcode\n   - Customer number\n   - License plate number\n   - Package number\n   - Part number\n   - Revenue group\n\n4. The selection can be restricted to:\n   - Only own businesses\n   - Only workshop\n   - Only service counter\n\n5. The results can be sorted by:\n   - Invoice number\n   - Invoice date\n   - Order number  \n   - Order date\n   - Matchcode\n   - Customer number\n   - License plate number\n   - Part number\n\n6. The selection results can be printed or displayed in a subfile.\n\n7. For open orders, the order text is searched if a search term is specified.\n\n8. Archived order/invoice PDFs can be displayed or printed if allowed.\n\n9. Statistical overviews of packages (new/old) can be generated and printed. \n\n10. Selection results can be exported to Excel.\n\n11. Credit limit info and exceptions are displayed for daughter companies.\n\n12. Orders/invoices can be sent to or processed in WHI.\n\nSo in summary, it provides comprehensive selection and analysis of order and invoice data using various criteria and outputs the results in different formats like display, print, export etc. The key business purpose is to support order/invoice evaluation and statistics.",

'HS0680.txt':"Here is the extracted business logic from the provided RPG code:\n\nThis appears to be an RPG program for displaying workshop orders. The key functions include:\n\n1. Displaying workshop orders\n- Allows displaying all workshop orders, only open orders, or orders for the current date\n- Displays details like order number, customer number, vehicle number, status etc in a subfile\n- Handles pagination and navigation of the subfile\n\n2. Lookup by customer number\n- Allows searching for orders by customer number using a matchcode\n- Displays matching orders in a subfile\n- Allows selecting a customer to filter orders\n\n3. Lookup by vehicle number  \n- Allows searching for orders by vehicle/chassis number\n- Displays matching orders in a subfile\n- Allows selecting a vehicle number to filter orders\n\n4. Lookup by repair code\n- Allows searching for orders by repair code \n- Displays matching orders in a subfile\n- Allows selecting a repair code to filter orders\n\n5. Display order details\n- Shows additional details for a selected order in subfiles\n- Displays order header, parts, labor, packages etc.\n- Calculates net values for parts and labor\n\n6. Integration with other programs/files\n- Reads data from workshop order (AUFWKR), customer (KUDSTAR), vehicle (HSFAILR), and other files\n- Calls other programs like HS0062C to retrieve archived data\n\nThe code interacts with display files like HS068000 for user interface. It handles subfile operations for output display. There is also some logic for handling pricing and totals.\n\nOverall, this program allows users to search, view and analyze workshop orders in an interactive manner by integrating with other programs and data files in the system. The business logic centers around order inquiry, lookup and display functions.",

'HS0258.txt':"Here is the extracted business logic from the provided RPG code:\n\nThis RPG program appears to be for searching and displaying supplier master data records.\n\nThe key functions are:\n\n1. Search Criteria Entry\n\n- The user can enter search criteria such as postal code (DUKPLZ), city (DUKSTR), address (DUKORT), name (DUKNAM), and branch (DUKBRA).\n\n- The entered search criteria are converted to uppercase and used to find matching supplier records. \n\n2. Supplier Record Retrieval\n\n- The LIFSTLF2 file is opened for retrieval of supplier master records (LIFSTLR2). \n\n- The search criteria entered by the user are compared to the corresponding fields in the supplier records (LIF060, LIF090, LIF030, LIF040). \n\n- Matching supplier records are selected and added to an internal table (ZL1).\n\n3. Subfile Display\n\n- The selected supplier records are displayed in a subfile (HS0258S1).\n\n- The display shows key fields like supplier number (LIF010) and name (LIF030). \n\n- Additional indicators:\n    - Supplier blocked (LIF255) is shown in red.\n    - Own/foreign customer is shown in different colors.\n\n- The user can select a supplier record by entering a selection number (WAHL), which returns the supplier number (LIF010).\n\n4. Subfile Navigation\n\n- Logic is included to navigate between subfile pages.\n- The number of records per page is defined (PAG1).\n- Cursor position is controlled.\n\nIn summary, this is an interactive search program that allows users to find and select supplier master records based on selection criteria. The key files used are LIFSTLF2 for supplier master and HS0258S1 for the subfile display. The result is returned via LIF010 when a record is selected.",

'RW0150.txt':"Here is the extracted business logic from the provided RPG code:\n\nThis appears to be an RPG program for managing partner data.\n\nMain logic:\n\n1. Read input parameters for search criteria (partner ID, customer number, name)\n\n2. Clear screen and display file headings \n\n3. Read partner data from VKSSPF file (likely a partner master file)\n\n4. Search for partners matching input criteria \n\n5. If no matches found, display message that no data was found\n\n6. Allow user to select a partner record \n\n7. Pass selected partner ID, customer number and name back to calling program\n\n8. Loop back to clear screen and search again until user exits\n\nSubroutines:\n\n1. SFL1LOE:\n   - Clear screen and display file headings\n\n2. SFL1LAD: \n   - Read partner file\n   - Search for matches\n   - Display results or no match message\n\n3. SFL1ANZ:\n   - Handle paging of results \n\n4. SFL1AUSW:\n   - Allow user to select a record\n   - Pass selected record details back to caller\n   \nFiles:\n\nVKSSPF - Partner master file (searched and read) \n\nRW0150D - Workstation file for user input\n\nRW0150S1 - Subfile for search results\n\nRW0150C1 - Format for screen headings \n\nRW015001 - Format for paging headings\n\nThis program allows searching the partner master file, displaying results, and selecting a partner record to pass back to the calling program. It handles typical RPG operations like file I/O, data selection and subfile management.",

'HS0230.txt':"Here is the extracted business logic from the provided RPG code:\n\n1. Customer Master File (KUDSTAM)\n\n- Stores customer header data like customer number (KUD000), name (KUD030), address (KUD060-KUD090), etc.\n\n- New customers can be added by writing a new record.\n\n- Existing customers can be updated by changing field values and rewriting the record.\n\n- Customers can be deleted by deleting the record.\n\n2. Individual Customer Data File (HSKUIPF) \n\n- Stores additional customer data like payment terms (KUI060), credit status (KUI070), payment method (KUI080), etc.\n\n- A record exists for each relationship between a customer and a branch (KUI000). \n\n- New customer-branch relationships are added by writing a new record.\n\n- Existing records are updated by changing field values and rewriting.\n\n- Allows assigning multiple customer numbers (KUI010) to the same customer master record.\n\n3. Customer Search and Selection\n\n- Customers can be searched and selected using:\n  - Customer number (KUI010)\n  - Branch key (KUI000) \n  - Matchcode (KUD050)\n  - Salesperson (KUD310)\n  - Mailing indiciator (KUI140)\n\n- Selection results are displayed in a subfile for viewing and updating.\n\n4. Maintaining Customer History\n\n- All changes to customer master and customer-branch records are logged.\n\n- Complete change history can be displayed. \n\n5. Customer Statistics\n\n- Sales statistics per customer per branch can be displayed in a subfile.\n\n6. Integration with SAP AX\n\n- Special routines to interface with SAP AX for validation, default values, updating AX records, etc.\n\n7. Address Verification\n\n- Customer addresses are verified against postal database.\n\n- Duplicate checking is performed to find potential duplicate customers.\n\n8. User Authorization\n\n- Users must be authorized to add, change or delete customers.\n\n- Password checking for sensitive fields like credit status, payment terms, etc.\n\n9. ERP Integration\n\n- Interfaces with finance system (FIBU) for account validation, check for existing accounts, etc.\n\nThe key files used are KUDSTAM for customer master data, HSKUIPF for customer-branch specific data, and HSKUDPF for change history. The program allows maintaining customer records, relationship records, statistics, histories, integration with SAP AX and FIBU, address verification, and security.",

'HS0341.txt':"Here is the extracted business logic from the provided RPG code:\n\nThis code seems to be for a parts/inventory management system. It focuses on looking up part prices for customers.\n\nMain logic flow:\n\n1. Get input parameters (fabrication plant code and part number)\n\n2. Validate input part number exists \n   - If not, exit\n\n3. Get default values\n   - Price query type = List price (BEREI='1') \n   - Price split = '01' (SPLITT='01')\n   - Price type = Customer price (WETE='2') \n\n4. If customer number blank:\n   - Prompt for customer number\n   - Lookup customer info\n   - If customer not found, exit\n\n5. Lookup part info\n   - Get part description, price\n   - Check if part has quantity breaks\n     - Call Pricing program (HS0095) to check for quantity breaks\n   - If quantity breaks exist:\n     - Call Pricing program (HS0095) to get quantity break price \n   - Else:\n     - Use base part price\n   - Calculate discounted price\n   - Store price details\n\n6. Set output flags\n   - Price found \n   - Additional text\n   - Errors if any\n\n7. Return to prompt for next part lookup\n\nThis program calls other programs:\n\n- HS0238 - Customer search \n- HS0095 - Pricing program\n- HS0087 - Store audit values\n\nAnd reads data from files:\n\n- TEISTAR - Part master file\n- HSKUIPR - Customer master file \n- KUDSTAR - Customer order file\n\nThe key data used:\n\n- Part number\n- Customer number \n- Pricing parameters like price type, quantity etc.  \n\nIn summary, the business logic focuses on retrieving the correct discounted price for a part based on customer, quantity and other pricing parameters. It handles error conditions and interfaces with other programs and data files.",

'HS0061.txt':"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- This code is for a dealer management system for Scania on the AS/400\n- It retrieves outgoing invoices/credit memos\n- It handles both branches and dealerships\n\nProcedures:\n\n1. Initialize variables and data structures\n- Initialize system date (DATUM)\n- Define data structures for user (ALGUSR), Axapta (AXAPTA), key for branches (KEYFIL), and key for dealerships (KEYFIX)\n\n2. Determine if there are branches and/or dealerships\n- Check branch file (HSBTSLR1) to see if there are any branches (KZLANZ='0')  \n- Check dealership file (HSFILPR) to see if there are any dealerships\n- Set indicator 77 if there are dealerships \n\n3. Allow selection of branch or dealership\n- If branch entered, validate against branch file\n- If dealership entered, validate against dealership file\n- Retrieve invoices/credit memos for selection using program HS0061C\n- Pass indicators 71/72 to determine report type (invoices/credit memos)\n\n4. F14 command to print settlement lists \n- Calls program HS0067\n\n5. F4 command for operator lookup\n- Allows user to search for operator ID (BTS02X)\n- Calls program HS0021 to search operator file (BTSFIL)\n\nFiles:\n- HSBTSLR1 - Branch file\n- HSFILPR - Dealership file \n- BTSFIL - Operator file\n- Other files likely used:\n  - Invoice/credit memo files\n  - Customer files\n\nPrograms Called:\n- HS0021 - Operator lookup\n- HS0061C - Retrieve invoices/credit memos\n- HS0067 - Print settlement lists\n\nIn summary, the key business logic handles validation and selection of branches or dealerships, retrieval of invoices/credit memos, and provides additional functions like operator lookup and settlement printing. The code utilizes various data files and calls other programs to implement the required business functionality.",

'HSCVSF.txt':"Here is the extracted business logic from the provided RPG code:\n\nOverall Purpose:\n- This code is for customer master data management and conversion of search fields.\n\nKey Files Used:\n- KUDSTAM (Customer Master File)\n\nProcedures:\n\n1. Main Logic:\n- Read customer master record (KUDSTAR) \n- Call subroutine SR001 to convert search fields\n- Update converted search fields back to customer master record\n- Read next record and loop\n\n2. SR001 - Convert Search Fields:\n- Populate search fields (SF1, SF2) from customer fields \n- Call SUCF to concatenate search fields\n- Convert search fields to uppercase (GROBU) \n- Convert umlauts in search fields (UMLAU)\n- Move converted search fields to customer master fields \n\n3. SUCF - Concatenate Search Fields:\n- Concatenate input search fields (SF1, SF2) into output SUFELD\n\n4. GROBU - Uppercase Conversion: \n- Convert input string KLEIN to uppercase in GROSS\n\n5. UMLAU - Umlaut Conversion:\n- Convert umlauts in input FG1 to AE, OE, UE in FG2\n\n6. PRUEF - Umlaut Check:\n- Check input character A for umlauts\n- If umlaut, convert to AE, OE, UE in A and B\n\nIn summary, the core logic converts customer fields to standardized search fields by concatenating, uppercasing, and converting umlauts. The search fields are updated back to the customer master file.",

'RS0011.txt':"Here is the business logic extracted from the provided RPG code:\n\nThe code is for a retail sales management application's customer scoring module.\n\nIt reads customer scoring contact data from an input file RSCS3F and updates/writes to an output file RSCSCF. \n\nThe key fields used to uniquely identify records are:\n- CS3_VGRP \n- CS3_KDNR\n- CS3_ART\n- CS3_DAT \n- CS3_STS\n- CS3_STANR\n\nThe logic is:\n\n1. Set the input file RSCS3F to read records. \n\n2. Read a record from RSCS3F into the RSCS3R format. \n\n3. Search for the record in RSCSCF using the unique key fields.\n\n4. If not found in RSCSCF:\n   - Move field values from RSCS3R to RSCSCR format\n   - Write the record to RSCSCF\n   \n5. Read next record from RSCS3F\n\n6. Repeat steps 3-5 until end of file reached on RSCS3F.\n\nThis ensures only unique contact records from the input file are written to the output file. \n\nThe files used are:\n\n- Input File: \n  - Name: RSCS3F \n  - Format: RSCS3R\n  - Source: Customer scoring contact data CSV file\n  \n- Output File:\n  - Name: RSCSCF\n  - Format: RSCSCR\n  - Destination: Customer scoring contact database table\n  \nThe business logic handles the common use case of extracting data from a CSV file, filtering out duplicates, and inserting into a database table. The unique key fields, file names, formats provide the context needed to understand the logic.",

'VK2108.txt':"Here is the extracted business logic from the provided RPG code:\n\nThe code appears to be related to some kind of vehicle rental system. \n\nProcedures/Functions:\n\n1. VK2108:\n   - Main driver program that calls other procedures to perform specific tasks.\n   - Retrieves user initials from a file (HSBTSLF1).\n   - Handles parameter input PARM1, PARM2, PARM3, PARM4.\n   - Calls different procedures based on PARM1 value.\n   - Displays results/output in a subfile (VK2108S1).\n\n2. SR_BELEG:\n   - Retrieves transaction/booking details from a file (SVWKXLF4 or AXBUCLR) and accumulates booking amount by booking number.\n   - Checks if booking already exists in subfile (VK2108S1). If yes, updates existing record. If no, writes new subfile record.\n\n3. SR_KUNDE: \n   - Retrieves customer details by customer number (VMV060) from files (HSKUIPF, KUDSTAM).\n   - Populates customer name (GWM040).\n\n4. SR_BETRAG:\n   - Retrieves booking amount (VMR050) by key (PKZ, VERTRAG) from file (VKVMRPF). \n   - Populates amount field (GWM050).\n\nParameters:\n\n- PARM1: Specifies the action to perform:\n  - KST: Retrieve bookings by cost object (PARM2).\n  - GWM: Update used car rental bookings (?) \n  - AUF: Generate new order number (PARM3).\n  - SUI: Retrieve saved search criteria (PARM4).\n  - SUO: Save search criteria (PARM4).\n\n- PARM2: Cost object or other key value.\n\n- PARM3: Order type (character 1-1).\n\n- PARM4: Search criteria text.\n\nFiles Used:\n\n- HSBTSLF1: User initials file\n- SVWKXLF4: Bookings file\n- AXAXTPF, AXBUCLR: Axapta files (?)\n- VKVMVLF1: Rental contracts file\n- VKVMRPF: Rental amounts file \n- VKGWBLF1, VKGWMLF1: Used car rental files (?)\n- VKVSSPF: Search criteria file\n- HSKUIPF, KUDSTAM: Customer files\n- VK2108S1: Output subfile\n\nIn summary, the code handles retrieval of bookings and related data by cost object or other criteria, populates a subfile with results, generates new order numbers, and saves/retrieves search criteria. The main business domain appears to be vehicle rentals.",

'HS0069.txt':"Here is the extracted business logic from the provided RPG code:\n\n1. String Conversion Procedures\n\n- toUppercase: Converts a given input string to uppercase characters.\n\n- toLowercase: Converts a given input string to lowercase characters. \n\nBoth procedures use the built-in %xlate function to perform the case conversion.\n\n2. Memory Management Procedures  \n\n- allocSpace: Allocates or reallocates memory for a pointer variable. It checks if the pointer is null (unallocated) and allocates or reallocates memory of the specified size accordingly.\n\n- deallocSpace: Deallocates memory for a pointer if the pointer is not null (allocated).\n\n3. Vehicle Information Display\n\n- Retrieves vehicle information like vehicle registration number, vehicle description, customer number and name etc. from various files like FARSTLF4, HSFAIPF, HSKUIPF etc.\n\n- Displays vehicle comments, customer comments, order history, campaigns, extended warranty information etc. related to the vehicle. \n\n- Displays upcoming vehicle maintenance deadlines from scheduling system.\n\n- Allows searching within the displayed information.\n\n- Handles pagination of results.\n\n4. Interaction with External Systems\n\n- Calls external programs like HS00512, HS0873, HS1212C1 to retrieve additional information.\n\n- Interacts with database tables like HSFZKPF, HSKUKPF, HSAHKLF, WPCACF etc. to retrieve information.\n\n- Prepares SQL statements to interact with database to retrieve rental and insurance information. \n\nIn summary, the code provides a comprehensive vehicle information interface by aggregating relevant data from various systems and allowing users to view, search and paginate through it. The business logic focuses on data retrieval, preparation, display and navigation.",

'HSCVMCA.txt':"Here is the business logic extracted from the provided RPG code:\n\nThis code appears to be for customer master data management and conversion of customer codes (HSAHKPF).\n\nThe main logic flow is:\n\n1. Read customer code records (HSAHKPR)\n2. For each record:\n\n- Extract customer code fields AHK270 and AHK410\n- Build search fields (SF1, SF2) from AHK270 and AHK410 \n- Call search field build subroutine (SUCHF)\n- Convert search field to uppercase (GROBU)  \n- Convert umlauts in search field (UMLAU)\n- Write converted search fields back to AHK270 and AHK410\n\nSubroutines:\n\nSUCHF:\n- Builds search field (SUFELD) by concatenating non-blank characters from input fields\n\nGROBU: \n- Converts search field (KLEIN) characters to uppercase except specific umlauts\n\nUMLAU:\n- Converts umlauts in search field (GROSS) to AE, OE, UE\n\nPRUEF:\n- Helper subroutine for UMLAU to check and convert specific umlaut characters\n\nIn summary, this program standardizes customer codes by converting them to uppercase and expanding umlauts. The converted codes are written back to the customer master records.\n\nThe program interacts with the following files:\n\n- HSAHKPF - Input - Customer master file\n- HSAHKPR - I/O - Customer code records \n\nNo database or UI interaction is indicated in the code.",

'RSE5626035.txt':"Based on the provided RPG code, here is the extracted business logic:\n\nThe code defines two data structures - CUSTREC and ORDREC. \n\nCUSTREC represents a customer record and contains the following fields:\n- CUSTNUM - Customer number \n- NAME - Customer name\n- ADDRESS - Customer address\n- CITY - City \n- STATE - State\n- ZIP - Zip code\n\nORDREC represents an order record and contains the following fields:\n- ORDER# - Order number\n- CUSTNUM - Customer number (foreign key to CUSTREC)  \n- ORDERDATE - Order date\n- SHIPDATE - Ship date \n- SHIPMETHOD - Shipping method \n- SHIPPING - Shipping charge\n\nThe main logic in the code does the following:\n\n1. Opens the customer file CUSTMAST for input.\n\n2. Opens the order file ORDERS for input. \n\n3. Reads a record from the ORDERS file into ORDREC.\n\n4. Searches the CUSTMAST file by CUSTNUM to retrieve the corresponding CUSTREC record.\n\n5. If a valid CUSTREC is found, it prints the customer name, order details like order number, order date, shipping date, shipping method and shipping charge.\n\n6. If a valid CUSTREC is not found, it prints an error message. \n\n7. Repeats steps 3-6 in a loop until end of ORDERS file. \n\n8. Closes the ORDERS and CUSTMAST files.\n\nThis program links data from the ORDERS and CUSTMAST files by CUSTNUM to print a customer's name and order details. The files used are:\n\n- CUSTMAST - Customer master file\n- ORDERS - Order detail file\n\nNo UI or database interactions are indicated in the code. The input and output operations are done on physical files.",

'HSCVMCK.txt':"Here is the business logic extracted from the provided RPG code:\n\nThis code is for customer master data conversion and matching code generation.\n\nIt reads a customer master record (KUDSTAR) and processes the matching code field (KUD050). \n\nThe key steps are:\n\n1. Initialize search fields SF1 and SF2 to blanks.\n\n2. Copy KUD050 to SF1. \n\n3. Call SUCF to populate SF2 with a condensed version of SF1 by removing blanks. \n\n4. Convert SF2 to uppercase by calling GROBU. This handles German umlauts.\n\n5. Call UMLAU to convert any umlauts in the uppercase version to AE, OE, UE.\n\n6. Move the final uppercase converted string to KUD050 to overwrite the original matching code.\n\n7. Update the customer master record (KUDSTAR).\n\nSo in summary, it generates a normalized matching code by:\n\n- Removing blanks\n- Converting to uppercase \n- Handling German umlauts\n\nThe processed matching code is stored back to the customer master record.\n\nThis program interacts with a customer master file (KUDSTAM). The matching code field is used for searching and matching customer records. By standardizing it, the matching process is improved.",

'CD0500.txt':"Here is the business logic extracted from the provided RPG code:\n\nThe code is for a program named CD0500 which is used for managing corporate groups (Konzerngruppen).\n\nIt contains the following key procedures:\n\n1. SFL1AUSW - Evaluates user input on subfile 1 for managing corporate groups and customers. It allows creating a new group, searching for a group, updating group name/comments, adding/removing customers to a group etc. \n\n2. SR_KGSUCHE - Searches for corporate groups based on input criteria like group number, name, comments or customer number. It prepares a dynamic SQL statement based on input, executes search, displays results on subfile 2.\n\n3. SFL1LOE - Clears subfile 1.\n\n4. SFL1LAD - Loads details of a corporate group and assigned customers on subfile 1.\n\n5. SFL1ANZ - Displays subfile 1. \n\n6. SFL2LOE - Clears subfile 2.\n\n7. SFL2ANZ - Displays subfile 2.\n\n8. GETCUSTOMERNAM - RPG procedure to retrieve customer name by calling SQL stored procedures on SATZENTRAL and HDLZENTRAL databases.\n\nThe main database tables used are:\n\n- CDKGNF - Contains corporate group master data \n- CDKGZF - Links customers to corporate groups\n\nThe program interacts with the user through displays like CD0500W1, CD0500W2 for input and subfiles CD0500S1, CD0500S2 to show outputs.\n\nIn summary, the business logic focuses on managing corporate groups and customer assignments by allowing CRUD operations through an interactive green-screen interface. The data is stored in DB2 tables and retrieved using embedded SQL in the RPG program.",

'CS0130.txt':"Based on the provided RPG code, here is the extracted business logic along with the related files and interactions:\n\nOverview:\n- This RPG program allows maintaining payment terms and print settings per customer for a specific division. \n- It is called from programs CS0100 and CS0120.\n\nKey Functions:\n1. Display customers\n- Retrieves a list of customers belonging to the input division who have entries in file CSFALF or fields KUI274,2,1 or KUI274,3,1 in file HSKUIPF.\n- Displays customer number, name, payment terms, payment term days, print individual invoices flag, and export invoice data excel flag.\n\n2. Add/update customer record\n- Allows adding or updating a record for a customer.\n- Validates payment terms code. Updates CSFALF and KUI274 in HSKUIPF.\n\n3. Delete customer record\n- Deletes the CSFALF record if present.\n- Resets KUI274,2,1 and KUI274,3,1 to blanks in HSKUIPF.\n\n4. Search for customer\n- Allows searching for a customer by number. Positions to the matching record.\n\nRelated files:\n- HSKUIPF (UF): Contains customer master data \n- CSFALF (UF): Contains payment terms data per customer and division\n- AXAXTPF (IF): Contains division data\n- KUDSTAM (PF): Contains customer master file\n- AXVALLF1 (PF): Contains valid payment terms codes\n\nInteractions:\n- Accepts division code, customer number as input parameters\n- Displays and updates interactive display file CS0130D\n- Reads customer master file HSKUIPF\n- Reads/updates payment terms file CSFALF\n- Validates payment terms code against AXVALLF1\n- Reads customer master file KUDSTAM \n- Reads division file AXAXTPF\n\nIn summary, this RPG program allows maintaining payment terms and print settings per customer by division through reading/updating various master files, validating inputs, and interacting with the user display file.",

'HS1900C.txt':"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- This RPG program is named HS1900C and titled \"SDPS Telephone Book\". \n- It was created by programmer EL on 30.03.2007 for the customer SCANIA DEUTSCHLAND.\n- The program belongs to the \"General Administration\" area of the SDPS Central application.\n\nFunctionality:\n- The main logic of the program is in subroutine HS1900, which is called near the end.\n- Before calling HS1900, the program adds several libraries to the job using ADDLIBLE. These likely contain subroutines, data structures, etc needed by the program.\n  - The libraries added are:\n    - ESW_00764T\n    - ESW_E00000 \n    - ESWTEL10\n    - ESDPCSCR\n- Based on the program name and title, this program likely manages a telephone book for the SDPS application. \n  - It may allow users to view, search, add, edit, or delete telephone book entries.\n  - It likely interacts with a database file containing the telephone records.\n\nIn summary, this is an RPG program for maintaining a telephone book for the SDPS Central application. The core logic is in subroutine HS1900, which interacts with a database file that stores the telephone records. The program adds required libraries and calls HS1900 to perform the main telephone book management functions.",

'HSMN09C.txt':"Here is the business logic extracted from the provided RPG code:\n\nThe code implements a financial accounting menu system with the following main functions:\n\n1. Daily Processing Menu:\n- Display/Print booking error logs \n- Display booking of revenues from daily closing\n- Display booking voucher \n- Display/Print account/cost center/cost object\n- Display account with all cost centers/cost objects \n- Display/Print cost center/cost object with all accounts\n- Display/Print margins on sold vehicles\n- Display number of sold vehicles\n- Display/Print EU/Non-EU revenues  \n- Print rental vehicle costs/revenues\n\n2. Account Current Menu: \n- Display account current\n- Clear account current\n- Print account statements  \n- Print open items\n- Print various outstanding lists\n- Search/Analyze open items\n- Maintain interest calculations\n- Generate interest calculations\n\n3. Dunning Menu:\n- Create/Reset dunning levels\n- Display/Change dunning blocking\n- Retrieve dunning from Scania\n- Print dunning by dunning level\n- Print dunning by customer number\n\n4. Manual Invoice/Credit Memo Menu:\n- Enter invoices/credit memos\n- Maintain text modules \n- Maintain number ranges\n- Maintain accounts for automatic posting\n- Maintain 3rd digit of G/L account related to customer numbers\n- Maintain VAT rates\n- Maintain default texts for manual invoices\n- Transfer accounts for automatic posting to new fiscal year or print\n- Transfer G/L account determination/customer numbers to new fiscal year or print\n- Print text modules\n\n5. Master Data Menu: \n- Maintain G/L accounts\n- Maintain customer accounts\n- Maintain posting text keys\n- Maintain cost center texts\n- Maintain sort keys\n- Print G/L account list \n- Print customer account list\n\n6. Axapta Menu:\n- Determine product code for vehicle number  \n- Display mapping of accounts/cost centers FI <-> Axapta\n- Manual invoice entry for Axapta\n- Cash book\n- Display/Select Axapta bookings\n- Display/Print account current\n- Send customer/vendor accounts to Axapta\n- Display/Print cost object list\n- Display/Print cost object list with margins\n- Display account with all cost centers/cost objects\n- Export open invoices with payment guarantee\n- Create booking file for external accounting e.g. SAP\n- Change order/revenue types\n- Internal order account/cost center\n\n7. Transfer bookings\n8. Create interim/month-end closing\n\nThe menu system controls user access to the programs and provides password protection for sensitive functions. Printer output is generated for many programs.\n\nThe code interacts with the following files:\n- Work files like HSMN09CD, HSMN09C1 etc. to display menus and pass data between programs\n- Authorization files like CTLHS1, CTLHS2 etc. to check user access rights\n- Shared data areas like AUSWKZ, BUCH etc. to share data between programs\n- Printer files like MANURG, LIST121 etc. to generate printed output\n\nIn summary, the RPG code implements a comprehensive menu-driven financial system for managing accounting processes including dunning, invoice processing, account management and integration with Axapta. The extracted business logic provides clarity on the end-to-end functionality.",

'ADW0030.txt':"Here is the extracted business logic from the provided RPG code:\n\nThis code handles duplicate address checking for customer master data maintenance.\n\nThe main logic flow is:\n\n1. Initialize variables  \n   - Get current org code (ORGA), user/branch code (KZLB)\n   - Initialize return code (§RTNCDE), duplicate flag (DUBLETTE), etc\n\n2. Call webservice AWDUBPR to check for duplicate address\n   - Pass input: customer number (PKZ+ADRNR) \n   - Get output: duplicate flag, possible duplicate customer numbers (§PKZO, §ADRNRO)\n\n3. If duplicate address found\n   - Retrieve possible duplicate customer details from database using §PKZO and §ADRNRO\n   - Display duplicate search results grid for user to review\n   - Set duplicate flag (DUBLETTE) on\n  \n4. Set final return code  \n   - If duplicate found, set §RTNCDE='*FOUND' and warning message\n   - If no duplicate, set §RTNCDE='*OK'\n   \n5. Suppress duplicate check for change of existing customer record\n\n6. Write duplicate search results to output file ADW0030S1\n\n7. Format and display search results grid using SFL\n\nKey files used:\n\n- HSKUIPF - Partner customer file\n- KUDSTAM - Own customer master file \n- ADW0030S1 - Search results detail file\n- ADW0030C1 - Search results SFL format file\n\nThis program would be called from customer master maintenance programs to perform duplicate checking before creating a new customer record.\n\nThe duplicate check logic and results display allows users to identify and reuse existing customer records, avoiding creation of duplicates.",

'HS0235.txt':"Here is the extracted business logic from the provided RPG code:\n\n**Overview:**\nThe code implements functionality to maintain payment guarantees for customers in the system. Key aspects include:\n\n- Displaying and editing payment guarantee details for customers\n- Adding new payment guarantees for customers\n- Restrictions on editing and adding payment guarantees based on user rights, customer status etc.  \n- Writing change flags and history records when payment guarantee details are modified\n\n**Procedures/Functions:**\n\n1. `CheckAuthority`: \n   - Purpose: Check if user has authority to edit/add payment guarantees. If not, exit program.\n   - Parameters:  \n     - `§PGMNAM`: Program name \n     - `§PGMTXT`: Program title\n     - `§PGMOPT`: Program option\n   - Logic:\n     - Call `CheckAuthority` API to validate authority\n     - If no authority, exit program\n\n2. `SR06N`: \n   - Purpose: Add new payment guarantee for a customer\n   - Parameters: \n     - `NEUKUD`: Customer number for new guarantee\n     - `NEUMAT`: Material number  \n     - `NEUNAM`: Name\n     - `NEUZAN`: Payment guarantee amount  \n     - `NEUDAT`: Valid to date\n     - `NEUUST`: VAT ID\n     - `NEULKZ`: VAT ID status\n     - `NEUOK`: VAT ID OK\n   - Logic:\n     - Validate if customer can have payment guarantee added\n       - Not an Axapta participant, not blocked, not cash payer\n       - Not a duplicate customer ID\n     - Default new payment guarantee values\n     - Allow editing based on user authority\n     - Validate maximum guarantee amount \n     - Write change flags and history records\n     - Add new payment guarantee to customer\n\n3. `SRHISF`:\n   - Purpose: Populate history record with current customer and payment guarantee header details\n   - Logic: \n     - Move current customer/payment guarantee header fields to history record format\n\n4. `SRHISS`:\n   - Purpose: Write history record to file\n   - Logic:\n     - Open history file\n     - Write history record\n     - Close history file\n\n5. `AENHIS`:\n   - Purpose: Write full record change history on update\n   - Logic:  \n     - Get current date and user\n     - Write to last change date, user in history format\n\n6. `SRAKT`:\n   - Purpose: Get current date and time\n   - Logic:\n     - Move current date to `AKTDAT` \n     - Move current time to `AKTTIM`\n     \n7. `WriteKui260SR`:\n   - Purpose: Write change flag KUI260\n   - Logic:\n     - Based on user type (Axapta or free) and customer type (Axapta or free), determine if change flag should be written and for which customer IDs.\n\n**Key Files**\n\n- `KUDSTAM`: Customer master file\n- `HSKUIPF`: Customer master index file\n- `HSKUDPF`: Customer history file\n\nThe code handles loading and interacting with these files to retrieve, update and store customer and payment guarantee details.\n\n**User Interface**\n\nThere appears to be user interface screens defined that allow:\n\n- Display and editing of existing payment guarantees \n- Adding new payment guarantees\n- Searching/filtering payment guarantees\n\nThese include:\n\n- `HS0235W6`: Add/edit payment guarantee screen\n- `HS0235C1`: Payment guarantee subfile 1\n- `HS0235C2`: Payment guarantee subfile 2 \n- `HS0235W9`: Search screen\n\nThe RPG code handles loading these screens, responding to user actions on the screens, and updating the display.\n\nLet me know if you need any clarification or have additional questions!",

'HS0470.txt':"Here is the extracted business logic from the provided RPG code:\n\nOverview:\n- The code handles the manual recording of parts receipts/accessions in Scania's parts inventory system. It allows entering receipt quantities, supplier invoice numbers, etc. for received parts.\n\nKey functions:\n1. Accession input screen (HS047001)\n- Allows entering part number, quantity, supplier invoice number for each parts receipt\n- Validates required fields like quantity, supplier number\n- Displays warning if receipt value exceeds limit\n- Prints accession transactions (BA code 30) \n\n2. Part master file (TEISTAM)\n- Reads part data like description, unit price etc. from Scania's part master file for displaying on input screen\n- Updates file with new average unit cost after each receipt\n\n3. Supplier master file (LIFSTAM)\n- Validates entered supplier number against master file\n- Checks for supplier blocks\n\n4. Customer master file (FISTAM)  \n- Reads customer number and country code for validations\n\n5. Transaction file (TRANSAKT)\n- Outputs transaction records (BA 30) for each parts receipt \n\n6. Other functions:\n- Calculates new average unit cost after each receipt\n- Checks for customer overdues, prompts user if found\n- Validation/warnings for receipt value, unit cost variance\n- Default supplier number based on part master/customer codes\n- Multi-part number handling\n\nFiles Used:\n- TEISTAM: Part master file\n- LIFSTAM: Supplier master file  \n- FISTAM: Customer master file\n- TRANSAKT: Transaction file\n- FHSBTSLF1: Daughter company file\n- VKSSPL4: Daughter company/own customer numbers\n\nInterfaces:\n- User screen I/O on HS047001\n- Part number search screen HS0258\n- Overdue details screen HS0560\n- New order screen HS0471 (receipt via purchase order)\n\nLet me know if any part of the logic needs more explanation or if you would like me to expand on any area.",

'HSTRG10.txt':"Based on the provided RPG code, here is the extracted business logic along with the related files and interactions:\n\nThe code represents a program named HSTRG10 that displays history records created by triggers.\n\nKey Files:\n- HTTSHF/HTTSHL1 (Physical File TEISTAM): Contains trigger history records for part number changes.\n- HTKSHF (Physical File KUDSTAM): Contains trigger history records for customer number changes.  \n- HTLSHF (Physical File LIFSTAM): Contains trigger history records for vendor number changes.\n\nAdditional Files: \n- CDTRFF (Copy File): Used to retrieve field descriptions.\n- VKSSPL4 (Physical File): Used to retrieve user name for a user ID.\n\nUser Interface Files:\n- HSTRG10C1 (Display File): Main display file.\n- HSTRG10S1 (Subfile): Shows the history records.\n- HSTRG10W5 (Display File): Shows record details on F5.\n\nParameters:\n- PARM1: Library/File name\n- PARM2: Search key \n- PARM3: Calling program name\n\nMain Logic:\n1. Initialize and get parameter values\n2. Allow user to select file for history\n3. Based on file selected, retrieve history records between date range\n   - Read records from HTTSHF/HTTSHL1 for part number file\n   - Read records from HTKSHF for customer number file\n   - Read records from HTLSHF for vendor number file\n4. Write records to subfile if they match search criteria\n5. Allow viewing of record details on F5\n6. On F11, toggle between showing old and new field values\n\nIn summary, the program displays historical changes to part numbers, customer numbers and vendor numbers by reading relevant trigger history files based on user selection. The results are shown in a subfile and record details can be displayed on F5.",

'HS0560.txt':"Here is the extracted business logic from the provided RPG code:\n\nThe code contains several procedures/functions to perform the following:\n\n1. String Manipulation\n   - toUppercase() - Converts a string to uppercase\n   - toLowercase() - Converts a string to lowercase\n\n2. Memory Management\n   - allocSpace() - Allocates or reallocates memory for a pointer variable\n   - deallocSpace() - Deallocates memory for a pointer variable\n\n3. Processing Customer Balances:\n   - The main logic searches for overdue customer balances based on input criteria such as order date, order number, customer number etc.\n   - It retrieves relevant order data from files like customer master (KUDSTAR), order header (HSOBKLR2/3), order lines (HSOBKPR) etc.\n   - The selected orders are displayed in a subfile for selection. \n   - The user can then process the overdue balances by specifying delivery quantity. This generates output for delivery notes.\n   - The stock levels and order balances are updated based on deliveries.\n   - Various validations are performed during delivery processing.\n\n4. User Interface Handling:\n   - The display handling allows viewing orders in different sorted orders.\n   - It allows selection of orders by type - workshop, counter etc. \n   - Navigation between different subfile views is enabled using function keys.\n\n5. Reporting:\n   - The overdue balances subfile data can be printed after processing.\n\n6. Files Referenced:\n   - KUDSTAR - Customer master\n   - HSOBKLR2/3 - Order header\n   - HSOBKPR - Order lines\n   - HSAHKLR1 - Cost distribution\n   - AUFTKR - Counter order header \n   - AUFWKR - Workshop order header\n   - TEISTAR - Parts master\n   - AUFTTR/AUFWTR - Delivery notes\n   - TRANSAKT - Transaction file\n\nThe code handles the key business process of managing overdue customer balances and enabling delivery processing for selected orders. Let me know if you need any clarification or have additional questions!",

'HS0239.txt':"Here is the business logic extracted from the provided RPG code:\n\nOverall Functionality:\n- This RPG program allows maintaining bank details for a given customer. It provides functions to view, add, change and delete bank accounts.\n\nParameters:\n- DEBLIF (Input): Customer number \n- KZL (Input): Central key of customer's home location\n- KONTO (Input): Account number of customer's home location  \n- BEREICH (Input): Bank detail type (e.g. payments, loans etc.)\n- ANZ (Input): Number of bank details to maintain\n- ParmIban (I/O): IBAN number\n- ParmBic (I/O): BIC code \n- ParmBN (I/O): Bank name\n\nAdditional Inputs: \n- FIRMA: Company name\n- UMGEBUNG: Company code  \n\nProcessing:\n1. Validate input parameters\n\n2. If home partner, set indicator *IN80 to '1'\n\n3. Get central key KZLZEN and account number KontoZen for customer's home location\n\n4. Get description BERBEZ for input bank detail type BEREICH\n\n5. Repeat until F3 or F12 is pressed:\n   - Call SFL1LOE to clear detail screen\n   - Call SFL1LAD to load bank details into subfile\n   - Call SFL1ANZ to display number of records in subfile\n   - Case of user action:\n      - F3 or F12 pressed - exit loop\n      - F6 pressed - call SR06 to add new bank detail\n      - Selection from subfile - call SFL1AUSW to process user action\n\n6. Set indicator *INLR to '1' to prevent re-display of screen\n\nSubroutines:\n\nSFL1LOE: Clear detail screen\nSFL1LAD: Read bank details from file HSBNKF into subfile HS0239S1 based on selection criteria\nSFL1ANZ: Count and display number of records in subfile\nSFL1AUSW: Process user action on subfile record\n   - F1 - Call SR_BANK to validate IBAN\n   - F2 - Allow change of bank detail \n         - Call PLAUSISR to validate input  \n         - If valid, update file HSBNKR\n         - If bank detail type changed, update sort order in HSBNKL1\n   - F4 - Allow delete of bank detail\n         - If confirmed, delete record from HSBNKR\nSR06: Allow user to add new bank detail\n   - Initialize fields  \n   - Loop until F12 pressed to exit without add:\n     - Display add screen HS023902\n     - Call PLAUSISR to validate input\n     - If valid:\n       - Determine next sort number\n       - Write new record to HSBNKR\nPLAUSISR: Validate input fields for add/change\n   - Check required fields  \n   - Validate IBAN \n   - Check for duplicate bank detail\n   - Validate country code\n   - Validate bank detail type\nSR04: Provide F4 search help\nSR_BANK: Call program ADW0010 to validate IBAN\n\nFiles Used:\nHSBNKF: File containing customer bank details\nHSBNKR/HSBNKL1: Files updated when adding/changing bank details\n\nIn summary, this RPG program provides maintenance of bank details for a customer by allowing users to view, add, change and delete records through an interactive subfile. It validates all user input and updates associated files.",

'HSHI_SNUHP.txt':"Here is the business logic extracted from the provided RPG code:\n\nThis code is doing customer data migration from one region to another (Munich to Nuremberg) in an ERP system for Scania Deutschland.\n\n1. It first checks the current user's region code in the ALGUSR variable. If not 'SNU' (Nuremberg), it exits.\n\n2. It opens the input file KUDSNU_HP which contains the list of customers to be migrated from Munich (SBU) to Nuremberg (SNU). \n\n3. It reads each record from KUDSNU_HP and checks if the home partner (HP) should be changed to SNU and the change date (VDATUM) is blank.\n\n4. It searches for the customer in the KUDSTAR file using the customer number (KDNR).\n\n5. It then searches for the customer in the KUIL file to get the SNU customer number. \n\n6. If found, it updates the home partner and branch in KUIL, KUDSTAR, KUKPF, KUAPF files:\n\n   - KUIL: Updates home partner code (KUI020) and number (KUI030). If previous branch was 600, sets change indicator (KUI260).\n\n   - KUDSTAR: Updates home partner code (KUD000) and number (KUD010). If previous branch was 600, updates branch to 610.\n\n   - KUKPF/KUAPF: Updates home partner code and number.\n\n7. It updates the change date in KUDSNU_HP.\n\n8. It repeats for each record in KUDSNU_HP.\n\nIn summary, this program migrates customers from Munich to Nuremberg by changing the home partner and branch details in multiple customer files based on an input file. The core files used are:\n\n- KUDSNU_HP: Input file \n- KUIL: Customer master file\n- KUDSTAR: Customer master file\n- KUKPF: Customer file\n- KUAPF: Customer file\n\nIt is an ERP migration program specific to Scania Deutschland.",

'HS0238C.txt':"Here is the business logic extracted from the provided RPG code:\n\nThis code appears to be a main program that calls another program HS0238 to perform some functionality related to customers.\n\nThe key points are:\n\n- Purpose: Main program that calls HS0238 to search/check duplicate customer master records\n\n- Modules Called: \n  - HS0238 (with 4 parameters passed):\n    - Param 1: Blank space \n    - Param 2: Blank space\n    - Param 3: 'ZGANZ' (seems to indicate full/complete search)\n    - Param 4: Blank space\n\n- Functionality:\n  - The main program doesn't contain much logic, it simply calls HS0238 while passing some parameters\n  - The purpose seems to be searching and checking for duplicate customer master records\n  - HS0238 likely contains the core logic for searching and deduplicating \n  - The parameters passed indicate some kind of full or complete search is desired\n\n- Other Details:\n  - This program is called HS0238C\n  - It's part of an application called SDPS-ZENTRAL\n  - The application area is customers\n  - Created by P.Wehn on 06.12.2004\n\nIn summary, this main RPG program calls another program HS0238 to perform customer master search and deduplication functions by passing it some parameters. The core logic resides within HS0238 which gets called from this main program.",

'VK2117.txt':"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- This is an RPG program named VK2117 that appears to be related to vehicle rental contracts and their history.\n\nMain Functions:\n1. Display contract history in a subfile\n2. Allow searching the subfile records\n3. Retrieve and format subfile record details from associated files\n\nSubroutines:\n\nSR_ANZ1:\n- Purpose: Build and display subfile of contract records\n- Logic:\n  - Clear existing subfile records\n  - Call SR_SUB1 to populate subfile \n  - Set subfile cursor position\n  - Write subfile format and records to display subfile\n  \nSR_SUB1: \n- Purpose: Populate subfile with contract records\n- Logic:\n  - Read contract header records (VKVMHPF)\n  - For each header record:\n    - Get header record info like date, customer name etc.\n    - Determine contract type code\n    - Check if it matches search criteria\n    - If yes, write record to subfile\n  - If no records, write blank line with message\n  \nSR_ART:\n- Purpose: Determine contract type code \n- Logic:\n  - Get contract type code (VMH030)\n  - Lookup description in VSS file\n  - Set subtype field in subfile record\n  \nSR_SUCHEN:  \n- Purpose: Check if record matches search criteria\n- Logic:\n  - Initialize found flag to false\n  - If search term is blank or found in customer name, type code etc. \n    - Set found flag true\n    \nFiles Referenced:\n- VKVMHPF: Contract header/master file\n- VKVSSPF: Contract types file\n- KUDSTAM: Customer master file \n- HSKUIPF: Vehicle header file\n\nDisplays Referenced: \n- VK2117W1: Subfile display format\n- VK2117C1: Subfile control format \n\nSo in summary, this program allows users to view and search through vehicle rental contract history by fetching data from associated files, populating a subfile and allowing text searches on key fields.",

'HS0921.txt':"Here is the extracted business logic from the provided RPG code:\n\nThe code appears to be for a dealer service application that processes customer accounts to select valid offset accounts.\n\nMain logic:\n\n1. Read fiscal year from file FISTAR into field GSJJ2.\n\n2. Move account segment values from file FISTAR into fields TEILN and BUCHH. \n\n3. Build keys using account segment values to search other files.\n\n4. Validate fiscal year:\n\n- Check if current fiscal year, if not subtract 1 from GSJJ2 to get previous fiscal year.\n\n- Check if GSJJ2 matches VGLJJ, if not set indicator for old fiscal year.\n\n5. Prompt for account number input using display file HS092101.\n\n6. Search file HSRKTR using key built from account segments. If not found:\n\n- Validate account number using file HSKUIPR.\n\n- If valid, write new record to HSRKTR. \n\n- If not valid, display error.\n\n7. If account is found in HSRKTR, display valid prior years from HSRKTR in subfile using display file HS0921C1.\n\n8. Allow updating, adding or deleting records in HSRKTR.\n\n9. On exit, set indicator showing process completed.\n\nThe code interacts with the following files:\n\n- FISTAR - Fiscal year and account segment values\n\n- HSRKTR - Account validation records\n\n- HSKUIPR - Account number validation\n\n- KUDSTAR - Account number validation\n\n- HS092101 - Account number input screen \n\n- HS0921C1 - Prior years subfile display\n\nAnd uses these data structures:\n\n- FIRMA - Company name\n\n- ALGUSR - User name\n\nThe main business purpose is to validate account numbers entered for a customer against prior year data, prompting for input, displaying valid options, and allowing maintainence of the account validation records.",

'HSCVMCKSHA.txt':"Here is the business logic extracted from the provided RPG code:\n\nThis code is for customer master data conversion and focuses on converting match codes.\n\nMain logic:\n1. Read customer master record into memory (CHAIN KUDSTAR).\n2. Call subroutine SR001 to convert match code. \n3. Update customer master record (UPDATE KUDSTAR).\n4. Read next record and loop back (READE KUDSTAR).\n\nSR001 subroutine logic:\n1. Clear work fields SF1, SF2, KLEIN, GROSS.\n2. Move customer name (KUD050) to SF1. \n3. Call SUCHF to populate search field SF2 with non-blank chars from SF1.\n4. Convert SF2 to uppercase (GROBU) and replace umlauts (UMLAU). \n5. Move result to customer name (KUD050).\n\nSUCHF subroutine logic:\n- Loop through SF1 and move non-blank chars to SF2.\n- Return SF2.\n\nGROBU subroutine logic: \n- Convert lowercase letters in KLEIN to uppercase in GROSS, except for umlauts.\n- Return GROSS.\n\nUMLAU subroutine logic:\n- Loop through GROSS and check for umlauts.\n- Replace ä/Ä with Ae, ö/Ö with Oe, ü/Ü with Ue, ß with SS.\n- Return result in GROSS.\n\nPRUEF subroutine logic:\n- Check input letter A for umlauts.\n- If umlaut, replace with equivalent and set output letter B. \n- Check if A is lowercase.\n- Return flags indicating umlaut found and lowercase found.\n\nIn summary, this RPG code handles converting a customer name field to a standardized match code format by:\n- Extracting non-blank chars \n- Converting to uppercase\n- Replacing umlauts with two-letter equivalents\n- Updating the customer master record\n\nIt interacts with a customer master file (KUDSTAR). The converted match code is updated back to the customer name field (KUD050) on the file.",

'VK2100.txt':"Here is the business logic extracted from the provided RPG code:\n\nThe code contains several procedures, each serving a specific purpose:\n\n1. Validation procedures:\n- SR_CHECKLOCK: Checks if a rental contract is locked by another user.\n- SR_PRUEFEN: Validates rental dates, calculates rental costs and checks for errors.\n- SR_PRUEFENF: Checks if approval is required for a rental contract.\n\n2. Lookup procedures:  \n- SR_KUNDE: Looks up customer details based on customer number.\n- SR_FZG: Looks up vehicle details like make, model etc based on chassis number.\n- SR_STATUS: Looks up rental status text based on status code.\n- SR_ART: Looks up rental type text based on vehicle usage code.\n\n3. Calculation procedures:\n- SR_DAUER: Calculates rental duration in days, weeks and months.\n- SR_KM: Calculates extra kilometers driven.\n- SR_TARIF: Looks up rental rates based on tariff code.\n\n4. Display procedures: \n- SR_ANZ1/2/3: Displays rental contracts in different views.\n- SR_NEU: Initializes screen fields with blank values.\n- SR_VER: Displays rental contract details for editing.\n\n5. Update procedures:\n- SR_VMV: Updates rental contract master file (VMV) with new values. \n- SR_UPDATE: Validates and writes changed rental data to database.\n- SR_HISTORIE: Logs changes to rental history file (VMH).\n\n6. Other procedures:\n- SR_SPEICHERN: Creates new rental contract.\n- SR_FILTER: Applies search filters to only show specific contracts.  \n- SR_TARIF: Looks up rental tariff details like rates.\n- SR_GWLINK: Generates link to used vehicle system for the rented vehicle.\n\nThe main database files are:\n- VMV: Rental contract master data\n- VMR: Rental contract accounting data \n- VMH: Rental contract history of changes\n\nThe UI files are:\n- VK2100D: Display file format\n- VK2100Cx: Subfile formats\n\nIn summary, the code provides a full business process to manage rental contracts - from creating new contracts, calculating rental costs, updating details, displaying contracts, and logging history. The key steps are validating contracts, looking up relevant data, performing calculations, updating databases, and displaying results.",

'HS0614.txt':"Here is the business logic extracted from the provided RPG code:\n\nOverview:\n- This code is for damage coding on work orders in a workshop management system. It allows entering damage codes by customer and workshop.\n\nKey Files:\n- AUFWKO: Work order header file\n- AUFWSK: Work order damage coding file\n- AUFWSKF: Damage coding file layout \n- CWPMSGF: CWP message file \n- CWPMSRF: CWP message relations file\n\nProcedures:\n\n1. SR_WSK: Displays and maintains damage coding screen\n- Clears damage coding subfile \n- Reads work order damage codes into subfile\n- Allows adding, changing and deleting damage codes\n- Validates codes against CWP message file\n- Displays related CWP messages as search help for codes\n- Writes changed codes back to AUFWSK file\n\n2. SR_HINZU: Adds new damage code\n- Validates code against CWP message file\n- Writes new code to AUFWSK file\n\n3. SR_AENDERN_K: Changes existing customer damage code\n- Validates changed code against CWP message file  \n- Updates code in AUFWSK file\n\n4. SR_AENDERN_W: Changes existing workshop damage code\n- Validates changed code against CWP message file\n- Updates code in AUFWSK file\n\n5. SR_LOESCHEN: Deletes existing damage code\n- Deletes code from AUFWSK file\n\n6. SR_MSG_ID_K: Validates customer damage code against CWP message file\n\n7. SR_MSG_ID_W: Validates workshop damage code against CWP message file\n\n8. SR_AUFPOS: Checks if damage code is assigned to a valid work order position\n\n9. SR_COD_POS: Checks for damage codes without positions\n\n10. SR_POS_COD: Checks for positions without damage codes\n\n11. SR_CODW_OK: Checks if workshop damage coding is complete\n\n12. SR_EPA_I: Displays related extended prices (EPS)\n\n13. SR_EPA_DEL: Deletes related EPS when damage code is deleted\n\n14. SR_JOB: Retrieves related work order job UUID \n\nIn summary, the code provides maintenance of damage coding on work orders, validating codes and related positions, with integration to CWP message file.",

'HS0340.txt':"Here is the extracted business logic from the provided RPG code:\n\n1. String Conversion Procedures\n\n- toUppercase: Converts a given input string to uppercase.\n  - Parameters:\n    - string (Input): The string to convert to uppercase\n  - Logic: \n    - Uses the `%xlate` built-in function to replace lowercase letters with their uppercase counterparts.\n    - Returns the uppercase version of the input string.\n\n- toLowercase: Converts a given input string to lowercase.\n  - Parameters: \n    - string (Input): The string to convert to lowercase\n  - Logic:\n    - Uses the `%xlate` built-in function to replace uppercase letters with their lowercase counterparts. \n    - Returns the lowercase version of the input string.\n      \n2. Memory Management Procedures\n\n- allocSpace: Allocates or reallocates memory space for a pointer variable.\n  - Parameters:\n    - ptr (Input/Output): A pointer variable to allocate or reallocate\n    - bytes (Input): The amount of memory space to allocate/reallocate\n  - Logic:\n    - Checks if ptr is null (unallocated)\n      - If null, allocates memory space of the specified size (bytes) and assigns it to ptr\n      - If not null, reallocates memory space to ptr with the new size (bytes)\n      \n- deallocSpace: Deallocates memory space for a pointer variable if not null\n  - Parameters: \n    - ptr (Input): The pointer variable to potentially deallocate\n  - Logic:\n    - Checks if ptr is not null (allocated)\n      - If not null, deallocates the memory associated with ptr\n        \n3. Part Lookup and Display\n\n- Allows searching for parts by part number, part description, manufacturer part number, or reference part numbers\n- Retrieves and displays inventory information, pricing, replacements, stock levels, etc. for a selected part\n- Includes lookup in local databases and interfaces to external systems like SPAS\n- Handles selection between multiple potential matches on search criteria\n- Navigation between parts using next/previous part number or description\n\n4. Order Status Lookup\n\n- Looks up order status information from external system for a given customer order\n- Displays current order status details relevant to the selected part\n\n5. Subfile Search and Selection\n\n- Builds a subfile result set from a search \n- Allows interactive selection of a record from the subfile search results\n- Navigation through subfile search results\n\n6. Part Replacement Information\n\n- Checks for replacement parts information from SPAS\n- Displays available replacement parts for the selected part\n  \n7. Pricing and Discounts\n\n- Determines pricing, discounts, customer or contract prices for a part\n- Factors in pricing dimensions, product groups, franchises, etc.\n\n8. Inventory Transactions\n\n- Retrieves inventory transaction history for a part across locations\n- Navigation through the transaction history\n\n9. Ordering History\n\n- Gets ordering history for a part \n- Navigation through the order history records\n\n10. Customer Backorder Information\n\n- Checks for and displays backorders for a part by customer\n\nThe code handles database access, user interaction, business logic processing, and integration with external systems to deliver part search and information lookup functionality. The extracted logic provides a high-level view of the core business capabilities supported.",
 
'ESW050.txt':"Here is the extracted business logic from the provided RPG code:\n\nThe code appears to be doing the following:\n\n1. Reading the FARSTAM file (vehicle master data) to blank out certain fields (FAR420 and FAR460) before re-populating them.\n\n2. Reading FARSTAM again to identify vehicles that were never in the workshop and flag them in FAR420:\n  - Check if vehicle chassis number (FAR190) is valid\n  - Search for chassis number in SVASFGST and PIPPMST files \n  - If not found, set 1st position of FAR420 to 'F' for invalid chassis\n  - If found but vehicle owner (PIIMF1) is foreign, set 1st position to 'A' \n  - If not 'F' or 'A', check if ever in workshop (HSAHKLFF)\n  - If not found, set FAR420 to 'L' for never in workshop\n  - Update FARSTAM\n\n3. Build SQL table with duplicate chassis numbers (FAR190) from FARSTAM\n\n4. Read SQL table and flag duplicates:\n  - For each duplicate chassis number:\n    - Set 1st position of FAR420 to 'D' \n\n5. Read FARSTAM again to determine vehicle owners:\n  - For each record:\n    - If FAR420 not 'L', 'F', or 'A'\n      - Get owner data from HSAHKLFF (use longest ownership period)\n      - Lookup owner partner ID in HSBTSLF1\n      - Lookup owner address in HSKUIPF\n        - If found:\n          - Set FAR420 positions 2-3 and 5-6 with owner ID\n          - Set FAR460 with ownership period\n          - Update FARSTAM\n        - Else:\n          - Set FAR420 positions 2-9 to 'XXXXXXXXX'\n          - Clear FAR460\n          - Update FARSTAM\n  \n  - If FAR420 is 'D' (duplicate):\n    - Get ownership data as above\n    - Also get matching chassis number record's owner\n    - If owner found in FARSTAM, clear 1st position of FAR420 and update owner info\n    - Else set FAR420 positions 2-9 to 'XXXXXXXXX' and update\n  \n  - Chain logic on FARSTAM to find next record after updates\n  \n6. Read FARSTAM again:\n  - If FAR420 position 1 is blank:\n    - Lookup owner ID in KUDSTAM \n    - If duplicate found:\n      - Set FAR420 position 1 to 'N'\n    - Else:\n      - Update FAR420 with info from KUDSTAM\n  - Update FARSTAM\n\nFiles used:\n- FARSTAM - Vehicle master data\n- HSAHKLFF - Vehicle ownership periods \n- HSBTSLF1 - Partner master data\n- HSKUIPF - Partner addresses\n- SVBMRELM45 - Vehicle chassis numbers\n- PIPPMST - Vehicle owners\n- KUDSTAM - Customer master data\n\nThe code is doing duplicate checking and linking vehicles to owners by traversing these master data files. The end result is FARSTAM getting updated with flags and owner information."

}

def process_folder_customer_search(parent_folder_id):
    folder_name = "Customer Search Code Module "
    folder_business_logic = ""
    
    folder_structure={"files":['HS0238.txt','HS0900.txt','HS0815.txt','HS0870.txt','HSCVSF.txt','HSCVMCA.txt','HSCVMCK.txt','HS0235.txt',
                               'HS0239.txt','HS0238C.txt','CS0130.txt','HS1061.txt']}
    
    files=['HS0238.txt','HS0900.txt','HS0815.txt','HS0870.txt','HSCVSF.txt','HSCVMCA.txt','HSCVMCK.txt','HS0235.txt','HS0239.txt','HS0238C.txt',
           'CS0130.txt','HS1061.txt']
    
    files_name=[]
    
    for file in files:
        if(folder_business_logic==""):
            folder_business_logic=business_logic_customer[file]
            files_name.append(file)
        else:
            folder_business_logic = combine_business_logic(folder_name,folder_structure,files_name,folder_business_logic,file,business_logic_customer[file])
            files_name.append(file)
    
    logic = folder_business_logic
    return logic

class HigherLevelBLcustomersearch(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]
  
    def post(self, request):
        folder_id = request.data.get('id') 
        business_logic = process_folder_customer_search(folder_id)
        return Response({"response":business_logic}, status=200)   

class HigherLevelMDcustomersearch(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        business_logic = '''
        " Here is the combined high-level business logic overview for the Customer Search Code Module including the new logic from HS1061.txt:\n\nThe module enables searching for customer, supplier, and vehicle records, processing related invoices, converting codes, generating standardized matching codes, maintaining payment guarantees, calling duplicate check programs, maintaining payment terms and print settings, and selecting records for letter writing.\n\nIt contains customer, supplier, vehicle search programs, invoice processing, code conversion, matching code generation, payment guarantee maintenance, duplicate checking, payment terms maintenance, and letter writing selection programs: \n\n1. HS0238 - Customer master search and duplicate check\n\n2. HS0900 - Customer search by multiple criteria \n\n3. HS0815 - Invoice processing\n\n4. HS0870 - Order/invoice analysis and selection\n\n5. HSCVMCA - Customer code conversion \n\n6. HSCVMCK - Matching code generation\n\n7. HS0235 - Payment guarantee maintenance\n\n8. HS0239 - Maintenance of customer bank details\n\n9. HS0238C - Main program that calls HS0238 for duplicate check\n\n10. CS0130 - Payment terms and print settings maintenance per customer/division \n\n11. HS1061 - Customer/supplier/vehicle selection for letter writing\n\n- Allows selection of customers, suppliers or vehicles based on criteria\n- Builds SQL selection statements dynamically based on input\n- Calls HS1061C to retrieve selected records\n- Writes selection criteria to HSBRSPF/HSBRSPR\n- Selection can be done for customers, suppliers or vehicles\n- Displays selection screens HS10610x to get input  \n- Shows selection results in grid for user selection \n- User can select records and call letter writing program HS1062C\n\nKey Files:\n\n- Customer, supplier, vehicle master files\n- Invoice header and lines files  \n- Output subfiles\n- Screen formats\n- Code conversion records\n- Payment guarantee history file\n- Bank detail files\n- Payment terms file CSFALF\n- Division file AXAXTPF\n- HSBRSPF/HSBRSPR - Selection criteria file\n- HSBTSLF1 - Dealer short code file\n- S7L011A - Open campaigns file\n\nIn summary, the module provides comprehensive search, selection, processing, and maintenance capabilities for customer, supplier, and vehicle data, transactions, codes, terms, and bank details. HS1061 specifically enables flexible selection of records for letter writing."
        '''
        mermaid_diagram= higher_level_mermaid_diagram(business_logic)
        return Response(mermaid_diagram, status=400) 
 
class HigherLevelMFcustomersearch(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        business_logic = '''
        " Here is the combined high-level business logic overview for the Customer Search Code Module including the new logic from HS1061.txt:\n\nThe module enables searching for customer, supplier, and vehicle records, processing related invoices, converting codes, generating standardized matching codes, maintaining payment guarantees, calling duplicate check programs, maintaining payment terms and print settings, and selecting records for letter writing.\n\nIt contains customer, supplier, vehicle search programs, invoice processing, code conversion, matching code generation, payment guarantee maintenance, duplicate checking, payment terms maintenance, and letter writing selection programs: \n\n1. HS0238 - Customer master search and duplicate check\n\n2. HS0900 - Customer search by multiple criteria \n\n3. HS0815 - Invoice processing\n\n4. HS0870 - Order/invoice analysis and selection\n\n5. HSCVMCA - Customer code conversion \n\n6. HSCVMCK - Matching code generation\n\n7. HS0235 - Payment guarantee maintenance\n\n8. HS0239 - Maintenance of customer bank details\n\n9. HS0238C - Main program that calls HS0238 for duplicate check\n\n10. CS0130 - Payment terms and print settings maintenance per customer/division \n\n11. HS1061 - Customer/supplier/vehicle selection for letter writing\n\n- Allows selection of customers, suppliers or vehicles based on criteria\n- Builds SQL selection statements dynamically based on input\n- Calls HS1061C to retrieve selected records\n- Writes selection criteria to HSBRSPF/HSBRSPR\n- Selection can be done for customers, suppliers or vehicles\n- Displays selection screens HS10610x to get input  \n- Shows selection results in grid for user selection \n- User can select records and call letter writing program HS1062C\n\nKey Files:\n\n- Customer, supplier, vehicle master files\n- Invoice header and lines files  \n- Output subfiles\n- Screen formats\n- Code conversion records\n- Payment guarantee history file\n- Bank detail files\n- Payment terms file CSFALF\n- Division file AXAXTPF\n- HSBRSPF/HSBRSPR - Selection criteria file\n- HSBTSLF1 - Dealer short code file\n- S7L011A - Open campaigns file\n\nIn summary, the module provides comprehensive search, selection, processing, and maintenance capabilities for customer, supplier, and vehicle data, transactions, codes, terms, and bank details. HS1061 specifically enables flexible selection of records for letter writing."
        '''
        mermaid_diagram= higher_level_mermaid_flowchart(business_logic)
        return Response(mermaid_diagram, status=400)


