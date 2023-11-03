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
from django.shortcuts import redirect
from rest_framework.decorators import permission_classes,authentication_classes
from .newrepo import create_repository,get_git_repo_owner,create_github_branch,push_to_github
import os
from pydantic import BaseModel
from langchain import LLMChain, PromptTemplate
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
    
    
        
# extensions = ['.rpgle', '.sqlrpgle', '.clle', '.RPGLE', '.SQLRPGLE', '.CLLE','.py','.java','.jsx','.tsx','.js','.ts','.sql','.PY','.JAVA','.JSX','.TSX','.JS','.TS','.SQL','.sas','.SAS']
# def get_folder_structure(folder_id):
    
#     folder = FolderUpload.objects.get(folderId=folder_id)
    
#     folder_structure = []

#     # Get subfolders of the parent folder
#     subfolders = FolderUpload.objects.filter(parentFolder=folder)

#     # Get files in the parent folder
#     files = FileUpload.objects.filter(parentFolder=folder)

#     for subfolder in subfolders:
#         # Recursively get the structure of subfolders
#         subfolder_structure = get_folder_structure(subfolder.folderId)
#         folder_structure.append({
#             'folder_name': subfolder.foldername,
#             'type': 'folder',
#             'content': subfolder_structure
#         })

#     for file in files:
#         # Collect information about files
#         folder_structure.append({
#             'file_name': file.filename,
#             'type': 'file'
#         })

#     return folder_structure
# Higher Level Business Logic
# def file_business_logic(code):
#     # with open(file_path, 'rb') as file:
#     #     code = file.read() 
#     # logic= code_to_business_logic(code,source)
#     # return logic
    
#     source="RPG"
#     if source.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas","dspfr","dspfa","assembly"]:
#         return "Invalid source specified."
    
#     # template='''Task: Extract Comprehensive Business Logic for {destination} Code Conversion

#     # In this task, your goal is to meticulously extract the complete business logic, including all variables, function names, class names, 
#     # and their bodies, from the provided {source} code. The objective is to create a comprehensive representation of the business logic to 
#     # ensure it can be seamlessly transformed into {destination} code. This meticulous process involves the following essential steps:

#     # Step 1: Understanding the Source Code
#     # - Begin by thoroughly analyzing the {source} code to grasp its functionality, purpose, and structure. Develop a deep understanding of the underlying business processes and requirements.
#     # - Pay close attention to all variables, functions, classes, and data structures within the code, as they collectively form the basis of the business logic.
    
#     # Step 2: Expressing the Comprehensive Logic
#     #     - Present the extracted logic in a high-level, language-agnostic format. This representation should encompass all variables, function names, class names, function bodies, return statements, and data dependencies.
#     #     - Emphasize the sequential flow of operations, conditional statements, loops, and exceptional cases to ensure that the core business processes are faithfully preserved.
    
#     # Step 3: Identifying all Variables
#     # - List all variables and classes in the code. For each, capture their names, data types, and initial values.
#     # - Distinguish between global and local variables to understand their scope and relevance to the broader business logic.
#     # - Identify data dependencies between variable as this is crucial for preserving the integrity of the logic during translation.
    
#     # Step 4: Identifying each Functions
#     # - For each Function there should be logic of function so that it is easy to convert into another {destination} language code
#     # - For each function in the code, extract the complete body, including all statements, conditions, loops, and other logic contained within.
#     # - Specify the types and purposes of parameters for each function, and describe their significance within the context of the business logic.
#     # - In the case of functions returning values, extract the return statement and elucidate how it contributes to the overall business processes.

#     # The ultimate goal is to deliver a comprehensive and understandable representation of the business logic within the {source} code, 
#     # encompassing all necessary details such as variables, function names, class names, function bodies, return statements, and data 
#     # dependencies. This will make it significantly easier to translate the logic into {destination} language code, minimizing the gap 
#     # between the original {source} code and the eventual {destination} code, thereby ensuring accuracy and efficiency.

#     # Now, the User will provide {source} code. Your task is to generate the full business logic of given code, encompassing all variables,
#     # function names,function bodies, and return statements so that it is easy to converetable into {destination} language code
    
#     # Note We use this business logic into {destination} code so that give business logic according to that.
    
#     # Example_Code

#     # User: {input}
#     # Business Logic:
#     # '''

#     template='''Pretend to be an expert in {source} code and provide a comprehensive explanation of the user-provided {source} code, converting it into
#     understandable business logic. If the destinationiables in the code have values relevant to the business logic, please include them.I am interested 
#     solely in the business logic.Your task also involves analyzing the code, identifying its core functionality, and presenting this functionality 
#     clearly and concisely.Ensure that the extracted business logic is well-documented.
#     This process involves multiple steps:
    
#     1.  Analyze the source code to understand its functionality, purpose, and structure, including variables, functions, classes, and data structures.
#     2.  Identify and abstract the key algorithmic steps and logic used in the {source} code.
#     3.  Express this logic in a high-level, language-agnostic format.
#     4.  Summarize the comprehensive logic, including variables, functions, classes, control flow, and exceptional cases, in a high-level, language-agnostic format.
#     5.  Document all variables and classes by recording their names, data types, initial values, and distinguishing between global and local variables while identifying data dependencies for logic preservation.
#     6.  Extract and document each function's complete body, encompassing all statements, conditions, loops, and logic, along with parameter types and purposes, and clarify the role of return statements in the context of the business logic for higher level logic.
#     7.  Mention all variables and function are called from different file.
#     8.  Identify the type of code and if there is any database, other files or ui interaction.
#     9.  Any important information about the file structure should be identified and added to the interactions. 
#     10. Please specify these interactions towards the end of the generated response in a well formatted manner.
#     11. Be as verbose as needed.
    
#     Make sure that the output provides a clear and concise representation of the business logic within the {source} code. If the {source} code is complex,
#     please include comments or explanations to clarify the logic.
    
#     Now the User will provide {source} code, please generate correct buisness logic.
#     Share business logic and related files, functions and variables from different file and files also like for database as part of the response.
#     Business logic of this child file code should be such that contribute in higher level business logic of a parent folder. 
    
#     User: {input}
#     Business_Logic:
#     '''
#     llm_chain = LLMChain(
#         llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
#         prompt=PromptTemplate(input_variables=["input","source"], template=template),
#         verbose=True,
#     )
#     logic= llm_chain.predict(input=code,source=source)
#     return logic
# def combine_business_logic(folder_name,
#                            folder_structure,
#                            previous_business_logic,
#                            current_directory_name,
#                            current_directory_business_logic):
    
    
#     template='''
#     I'd like to generate comprehensive business logic documentation for a specific directory named '{folder_name}' with the following 
#     folder structure: '{folder_structure}'. 

#     To accomplish this, I will aggregate business logic from each directory within this folder one by one. Specifically, I will merge the business 
#     logic from selected directories within the folder structure with the business logic from the current directory named '{current_directory_name}' 
#     within the same folder structure. This process will result in a combined business logic document, which includes the accumulated logic up to the
#     specified directory and the business logic of the current directory. The goal is to create an all-encompassing report that includes any imported
#     statements from other files and all significant statements originating from these files. Additionally, this report will list the names of all
#     files and folders involved and the business logic report for the specified directory and its subdirectories will also include specific variable
#     values relevant to the overall business logic. It will indicate functions imported from other files and specify their sources, maintain consistency
#     in variable and function names, and provide function parameter types for each function.

#     In cases where the previous file's business logic is empty, it signifies that the current file is the first file, and there is no previous file's
#     business logic.
    
#     Now give me only Combined Business Logic of  Previous and Current Directory Logic given below: 
    
#     Previous Business Logic: {previous_business_logic}
#     Current Directory Business Logic: {current_directory_business_logic}
    
#     '''

#     llm_chain = LLMChain(
#         llm=ChatAnthropic(
#             temperature=0.8,
#             model="claude-2.0",
#             max_tokens_to_sample=100000
#         ),
#         prompt=PromptTemplate(
#             input_variables=[
#                 "folder_name",
#                 "folder_structure",
#                 "previous_business_logic",
#                 "current_directory_name",
#                 "current_directory_business_logic"
#             ],
#             template=template
#         ),
#         verbose=True,
#     )

#     logic= llm_chain.predict(folder_name=folder_name,
#                              folder_structure=folder_structure,
#                              previous_business_logic=previous_business_logic,
#                              current_directory_name=current_directory_name,
#                              current_directory_business_logic=current_directory_business_logic)
#     return f"{logic}"
# def process_folder_business_logic(folder_id):
    
#     folder = FolderUpload.objects.get(folderId=folder_id)

#     business_logic = ""
    
#     folder_name = folder.foldername
    
#     folder_structure = get_folder_structure(folder_id)

#     subfolders = FolderUpload.objects.filter(parentFolder=folder)
#     files = FileUpload.objects.filter(parentFolder=folder)
    
#     for subfolder in subfolders:
#         subfolder_business_logic = process_folder_business_logic(subfolder.folderId)
#         if(business_logic==""):
#             business_logic=subfolder_business_logic
#         else:
#             business_logic = combine_business_logic(folder_name, folder_structure, business_logic, subfolder.foldername, subfolder_business_logic)

#     for file in files:
#         file_business_logic_result = file_business_logic(file.file)
        
#         if (business_logic==""):
#             business_logic=file_business_logic
#         else:
#             business_logic = combine_business_logic(folder_name, folder_structure, business_logic, file.filename, file_business_logic_result)

#     return business_logic
# class HigherLevelBusinessLogic(APIView):
#     permission_classes = [CustomIsAuthenticated]
#     authentication_classes = [TokenAuthentication]

#     def post(self, request):
#         folder_id = request.data.get('id') 
#         business_logic = process_folder_business_logic(folder_id)
#         print(business_logic)
#         return Response({"response":business_logic}, status=200)
# Higher Level Mermaid Diagram
# def file_mermaid_diagram(code):
#     # with open(file_path, 'rb') as file:
#     #     code = file.read() 
        
#     source="RPG"
#     destination="JAVA"    
#     logic=code_to_business_logic(code,source)
#     mermaid_diagram = business_logic_to_mermaid_diagram(logic,source,destination)
#     return mermaid_diagram
# def combine_mermaid_diagram(folder_name,
#                            folder_structure,
#                            previous_mermaid_diagram,
#                            current_directory_name,
#                            current_directory_mermaid_diagram):
    
    
#     classDiagram_schema = ResponseSchema(name='mermaid_class_diagram_code',description='This is the mermaid class diagram code which can be rendered by mermaidjs 8.11.0. , converted to a correct json string with new line replaced with \\n.')
#     classDiagram_description_schema = ResponseSchema(name='mermaid_class_diagram_code_description',description='This is the description of the class diagram code generated')

#     response_schema = (classDiagram_schema,classDiagram_description_schema)
#     parser = StructuredOutputParser.from_response_schemas(response_schema)
#     format_instructions = parser.get_format_instructions()
    
#     template='''
#     I want to generate the complete Mermaid Diagram for the folder named '{folder_name}'. The folder structure of this folder is '{folder_structure}'.
#     To achieve this, I will consolidate the Mermaid Diagram from each directory within it one by one. Specifically, I will merge the Mermaid Diagram
#     from some directories within the folder structure with the current directory's Mermaid Diagram named 
#     '{current_directory_name}'. This process will result in the combined Mermaid Diagram up to the specified directory and the Mermaid Diagram of 
#     the current directory.Remember, in the future, anyone can convert this Mermaid Class diagram code to another language code easily, so provide the 
#     answer in the context of that. Also, give code in the correct syntax so that it can be rendered by MermaidJS 8.11.0. 
    
#     Now give me combined Mermaid Diagram of Previous Mermaid Diagram and Curreny Directory Mermaid Diagram given below.
    
#     Previous Mermaid Diagram:
     
#     {previous_mermaid_diagram}
    
#     Current Directory Mermaid Diagram: 
    
#     {current_directory_mermaid_diagram}
    
#     {format_instructions}

#     '''

#     llm_chain = LLMChain(
#         llm = ChatAnthropic(temperature= 0.8,model = "claude-2.0",max_tokens_to_sample=100000),
#         prompt=PromptTemplate(input_variables=["folder_name","folder_structure","previous_mermaid_diagram",
#                                                "current_directory_name","current_directory_mermaid_diagram"],partial_variables={"format_instructions":format_instructions}, template=template),
#         verbose=True,
#     )
#     logic= llm_chain.predict(folder_name=folder_name,
#                              folder_structure=folder_structure,
#                              previous_mermaid_diagram=previous_mermaid_diagram,
#                              current_directory_name=current_directory_name,
#                              current_directory_mermaid_diagram=current_directory_mermaid_diagram)
#     return f"{logic}"
# def process_folder_mermaid_diagram(folder_id):
    
#     folder = FolderUpload.objects.get(folderId=folder_id)

#     mermaid_diagram = ""
    
#     folder_name = folder.foldername
    
#     folder_structure = get_folder_structure(folder_id)

#     subfolders = FolderUpload.objects.filter(parentFolder=folder)
#     files = FileUpload.objects.filter(parentFolder=folder)
    
#     for subfolder in subfolders:
#         subfolder_mermaid_diagram = process_folder_mermaid_diagram(subfolder.folderId)
#         mermaid_diagram = combine_mermaid_diagram(folder_name, folder_structure, mermaid_diagram, subfolder.foldername, subfolder_mermaid_diagram)

#     for file in files:
#         file_mermaid_diagram_result = file_mermaid_diagram(file.file)
#         mermaid_diagram = combine_mermaid_diagram(folder_name, folder_structure, mermaid_diagram, file.filename, file_mermaid_diagram_result)

#     return mermaid_diagram
# def higher_level_mermaid_diagram(business_logic):
    
#     classDiagram_schema = ResponseSchema(name='mermaid_class_diagram_code', description='This schema represents the Mermaid class diagram code, which is compatible with MermaidJS version 8.11.0. The code should be represented as a valid JSON string with new lines replaced with "\\n".')
#     classDiagram_description_schema = ResponseSchema(name='mermaid_class_diagram_code_description', description='This schema represents the description of the class diagram code generated by MermaidJS.')

#     response_schema = (classDiagram_schema,classDiagram_description_schema)
#     parser = StructuredOutputParser.from_response_schemas(response_schema)
#     format_instructions = parser.get_format_instructions()
    
#     example_code=rpg_example2
    
#     template='''
#     I want to generate code with backticks for a Mermaid Class diagram using the business logic of a full folder. This Mermaid diagram is used to
#     visualize the high-level business logic of a folder's code.
    
#     Note: Also, provide code in the correct syntax so that it can be rendered by mermaidjs version 8.11.0. The code should be represented as a valid 
#     JSON string with new lines replaced with "\n".

#     Example:
#     {example_code}
    
#     Now, the user will provide the business logic of a full folder as well as associated files. Please generate correct and running code for a
#     Mermaid class diagram without any initial text in a JSON format with "mermaid_class_diagram_code" as the key.

#     User:{input}
#     Mermaid_Code:
#     {format_instructions}'''

#     llm_chain = LLMChain(
#         llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
#         prompt=PromptTemplate(input_variables=["input","example_code"],partial_variables={"format_instructions":format_instructions}, template=template),
#         verbose=True,
#     )
    
#     mermaid_diagram= llm_chain.predict(input=business_logic,example_code=example_code)
#     result=parser.parse(mermaid_diagram)
#     return result['mermaid_class_diagram_code']  
# class HigherLevelMermaidDiagram(APIView):
#     permission_classes = [CustomIsAuthenticated]
#     authentication_classes = [TokenAuthentication]

#     def post(self, request):
#         folder_id = request.data.get('id') 
#         folder = FolderUpload.objects.get(folderId=folder_id)
        
#         # business_logic= folder.higherlevelbusinesslogic
#         # mermaid_diagram=higher_level_mermaid_diagram(business_logic)
        
#         # mermaid_diagram = process_folder_mermaid_diagram(folder_id)
        
#         business_logic= '''Based on the provided inputs, here is a high-level summary of the business logic for the Gau folder:

#         The code in this folder relates to an ERP system handling various business functions like inventory management, sales order processing,
#         customer relationship management, and analytics. 

#         Key capabilities include:
#         - User and rights management - Adding, editing, deleting user records and access rights
#         - Master data maintenance - Updating inventory item master data, customer master records, partner records
#         - Pricing and discounts - Determining pricing, discounts, and net prices based on complex hierarchical rules and customer attributes 
#         - Order processing - Handling sales document types like quotes, orders, deliveries along with statuses, dates, quantities
#         - Inventory transactions - Posting inventory movements, serial numbers, batches triggered by sales, purchase etc.
#         - Batch management - Controlling, monitoring background jobs and batches
#         - Reporting and analytics - Customer survey analysis, sales analytics, inventory reports
#         - Auditing - Tracking changes to configuration and master data 
#         - System configuration - Managing system parameters, defaults, schemas across various screens
#         The programs leverage physical and logical database files, APIs, data structures, andbuilt-in RPG functions.
#         The code demonstrates common RPG constructs - file I/O, data structures, modular procedures, calculations, branching, looping, error handling. 
#         In summary, the folder contains a range of business logic required in an ERP system, interacting with databases, programs, interfaces and
#         users. The logic covers both transaction processing as well as reporting/analytics capabilities.'''
        
#         mermaid_diagram=higher_level_mermaid_diagram(business_logic)
#         print(mermaid_diagram)
#         return Response({"response":mermaid_diagram}, status=200)
# Higher Level Mermaid Flowchart
# def file_mermaid_flowchart(code):
#     # # with open(file_path, 'rb') as file:
#     # #     code = file.read() 
    
#     source="RPG"
#     destination="JAVA" 
#     logic=code_to_business_logic(code,source)
#     mermaid_flowchart = business_logic_to_mermaid_flowchart(logic,source,destination)
#     return mermaid_flowchart
# def combine_mermaid_flowchart(folder_name,
#                            folder_structure,
#                            previous_mermaid_flowchart,
#                            current_directory_name,
#                            current_directory_mermaid_flowchart):
    
    
#     flowchart_schema = ResponseSchema(name='mermaid_flowchart_code',description='This is the mermaid flowchart code with properly linked nodes which can be rendered by mermaidjs 8.11.0. ,converted to a correct json string with new line replaced with \\n. Also all the nodes should contain strings so that any special characters do not cause problems')
#     flowchart_description_schema = ResponseSchema(name='flowchart_code_description',description='This is the description of the flowchart code generated')

#     response_schema = (flowchart_schema,flowchart_description_schema)
#     parser = StructuredOutputParser.from_response_schemas(response_schema)
#     format_instructions = parser.get_format_instructions()

    
#     template='''
#     I want to generate the complete Mermaid Diagram for the folder named '{folder_name}'. The folder structure of this folder is '{folder_structure}'.
#     To achieve this, I will consolidate the Mermaid Diagram from each directory within it one by one. Specifically, I will merge the Mermaid Diagram
#     from directories some within the folder structure with the current directory's Mermaid Diagram named 
#     '{current_directory_name}'. This process will result in the combined Mermaid Diagram up to the specified directory and the Mermaid Diagram of 
#     the current directory.and the remember in future anyone can convert this mermaid diagram code to business logic easily.Also give code in correct
#     syntax so that it can be rendered by mermaidjs 8.11.0 . Make sure the blocks are properly linked .Mermaid flow chart diagram that visually
#     represents this logic.Now give me combined Mermaid Flowchart Code using Previous Memaid Flowchart and Current Directory Mermaid Flowchart given below:

#     Previous Mermaid Flowchart:
     
#     {previous_mermaid_flowchart}
    
#     Current Directory Mermaid Flowchart: 
    
#     {current_directory_mermaid_flowchart}

#     {format_instructions}
#     '''

#     llm_chain = LLMChain(
#         llm = ChatAnthropic(temperature= 0.8,model = "claude-2.0",max_tokens_to_sample=100000),
#         prompt=PromptTemplate(input_variables=["folder_name","folder_structure","previous_mermaid_flowchart",
#                                                "current_directory_name","current_directory_mermaid_flowchart"],partial_variables={"format_instructions":format_instructions}, template=template),
#         verbose=True,
#     )
#     mermaid_flowchart= llm_chain.predict(folder_name=folder_name,
#                              folder_structure=folder_structure,
#                              previous_mermaid_flowchart=previous_mermaid_flowchart,
#                              current_directory_name=current_directory_name,
#                              current_directory_mermaid_flowchart=current_directory_mermaid_flowchart)
#     return f"{mermaid_flowchart}"
# def process_folder_mermaid_flowchart(folder_id):
    
#     folder = FolderUpload.objects.get(folderId=folder_id)

#     mermaid_flowchart = ""
    
#     folder_name = folder.foldername
    
#     folder_structure = get_folder_structure(folder_id)

#     subfolders = FolderUpload.objects.filter(parentFolder=folder)
#     files = FileUpload.objects.filter(parentFolder=folder)
    
#     for subfolder in subfolders:
#         subfolder_mermaid_flowchart = process_folder_mermaid_flowchart(subfolder.folderId)
#         mermaid_flowchart = combine_mermaid_flowchart(folder_name, folder_structure, mermaid_flowchart, subfolder.foldername, subfolder_mermaid_flowchart)

#     for file in files:
#         file_mermaid_flowchart_result = file_mermaid_flowchart(file.file)
#         mermaid_flowchart = combine_mermaid_flowchart(folder_name, folder_structure, mermaid_flowchart, file.filename, file_mermaid_flowchart_result)

#     return mermaid_flowchart
# def higher_level_mermaid_flowchart(business_logic):
    
#     flowchart_schema = ResponseSchema(name='mermaid_flowchart_code', description='This schema represents the Mermaid flowchart code, designed to generate properly linked nodes that can be rendered by MermaidJS version 8.11.0. The code must be formatted as a valid JSON string, with newline characters replaced by "\\n". All nodes within the code should contain strings to ensure compatibility and avoid issues with special characters.')
#     flowchart_description_schema = ResponseSchema(name='flowchart_code_description', description='This schema provides a description of the flowchart code generated by MermaidJS. It includes details about the structure and relationships of the nodes within the flowchart, as well as any additional information relevant to understanding the flowchart.')

#     response_schema = (flowchart_schema,flowchart_description_schema)
#     parser = StructuredOutputParser.from_response_schemas(response_schema)
#     format_instructions = parser.get_format_instructions()
    
#     example_code=rpg_example3
    
#     template='''
#     Convert Business Logic to Mermaid Flow chart Diagram of a folder.
#     I want to generate code for Mermaid Flow chart diagram using business logic of a folder and Remember this mermaid class diagram code is used by
#     developers to visualize the folder's code logic. Also give code in correct syntax so that it can be rendered by mermaidjs 8.11.0 . Make sure the
#     blocks are properly linked . Here is also an example how to generate mermaid class diagram using the business logic. and remember also don't give
#     any inital word and sentence like here is mermaid flow chart diagram of this business logic.Mermaid flow chart diagram that visually represents 
#     this logic.The Mermaid flow chart diagram also should visually represent the flow and sequence of the business logic,including key decision points
#     and data dependencies. Ensure that the resulting diagram is comprehensive and self-explanatory. 
#     Follow these steps:
#         1. Review the provided business logic.
#         2. Identify key components, decisions, and flow control in the logic.
#         3. Create a Mermaid flow chart diagram that illustrates the flow of logic, including decisions, loops, and data flow.
#         4. Ensure that the files , databases and other UI elements which might be present are properly shown.
#         5. Ensure the Mermaid flow chartdiagram is clear, well-structured, and accurately represents the business logic.
        
#     Example:
#     {example_code}
    
#     Now the User will provide business logic,generate correct and running code for mermaid Flowchart diagram as shown in above example without any 
#     initial text in a JSON format with "mermaid_flowchart_code" as the key and make sure that the blocks areproperly linked in the code.
    
#     User: {input}
#     Mermaid_Flowchart_Code:
#     {format_instructions}'''

#     llm_chain = LLMChain(
#         llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
#         prompt=PromptTemplate(input_variables=["input","example_code"],partial_variables={"format_instructions":format_instructions}, template=template),
#         verbose=True,
#     )
    
#     mermaid_flowchart= llm_chain.predict(input=business_logic,example_code=example_code)
#     result=parser.parse(mermaid_flowchart)
#     return result['mermaid_flowchart_code']
# class HigherLevelMermaidFlowchart(APIView):
#     permission_classes = [CustomIsAuthenticated]
#     authentication_classes = [TokenAuthentication]

#     def post(self, request):
#         folder_id = request.data.get('id') 
#         folder = FolderUpload.objects.get(folderId=folder_id)
        
#         # mermaid_flowchart = process_folder_mermaid_flowchart(folder_id)
        
#         # business_logic= folder.higherlevelbusinesslogic
#         # mermaid_flowchart=higher_level_mermaid_flowchart(business_logic)
        
#         business_logic= '''Based on the provided inputs, here is a high-level summary of the business logic for the Gau folder:

#         The code in this folder relates to an ERP system handling various business functions like inventory management, sales order processing,
#         customer relationship management, and analytics. 

#         Key capabilities include:
#         - User and rights management - Adding, editing, deleting user records and access rights
#         - Master data maintenance - Updating inventory item master data, customer master records, partner records
#         - Pricing and discounts - Determining pricing, discounts, and net prices based on complex hierarchical rules and customer attributes 
#         - Order processing - Handling sales document types like quotes, orders, deliveries along with statuses, dates, quantities
#         - Inventory transactions - Posting inventory movements, serial numbers, batches triggered by sales, purchase etc.
#         - Batch management - Controlling, monitoring background jobs and batches
#         - Reporting and analytics - Customer survey analysis, sales analytics, inventory reports
#         - Auditing - Tracking changes to configuration and master data 
#         - System configuration - Managing system parameters, defaults, schemas across various screens
#         The programs leverage physical and logical database files, APIs, data structures, andbuilt-in RPG functions.
#         The code demonstrates common RPG constructs - file I/O, data structures, modular procedures, calculations, branching, looping, error handling. 
#         In summary, the folder contains a range of business logic required in an ERP system, interacting with databases, programs, interfaces and
#         users. The logic covers both transaction processing as well as reporting/analytics capabilities.'''
            
#         mermaid_flowchart=higher_level_mermaid_flowchart(business_logic)
        
#         print(mermaid_flowchart)
#         return Response({"response":mermaid_flowchart}, status=200)

    
        
#     def file_mermaid_flowchart(file_path):
#         with open(file_path, 'rb') as file:
#             code = file.read() 
        
#         source=""
#         destination=""
#         logic=code_to_business_logic(code,source)
#         mermaid_flowchart = business_logic_to_mermaid_flowchart(logic,source,destination)
#         return mermaid_flowchart
        
#     def combine_mermaid_flowchart(folder_name,
#                             folder_structure,
#                             previous_mermaid_flowchart,
#                             current_directory_name,
#                             current_directory_mermaid_flowchart):
        
        
#         flowchart_schema = ResponseSchema(name='mermaid_flowchart_code',description='This is the mermaid flowchart code with properly linked nodes which can be rendered by mermaidjs 8.11.0. ,converted to a correct json string with new line replaced with \\n. Also all the nodes should contain strings so that any special characters do not cause problems')
#         flowchart_description_schema = ResponseSchema(name='flowchart_code_description',description='This is the description of the flowchart code generated')

#         response_schema = (flowchart_schema,flowchart_description_schema)
#         parser = StructuredOutputParser.from_response_schemas(response_schema)
#         format_instructions = parser.get_format_instructions()

        
#         template='''
#         I want to generate the complete Mermaid Diagram for the folder named '{folder_name}'. The folder structure of this folder is '{folder_structure}'.
#         To achieve this, I will consolidate the Mermaid Diagram from each directory within it one by one. Specifically, I will merge the Mermaid Diagram
#         from directories some within the folder structure with the current directory's Mermaid Diagram named 
#         '{current_directory_name}'. This process will result in the combined Mermaid Diagram up to the specified directory and the Mermaid Diagram of 
#         the current directory.and the remember in future anyone can convert this mermaid diagram code to business logic easily.Also give code in correct
#         syntax so that it can be rendered by mermaidjs 8.11.0 . Make sure the blocks are properly linked .Mermaid flow chart diagram that visually
#         represents this logic.Now give me combined Mermaid Flowchart Code using Previous Memaid Flowchart and Current Directory Mermaid Flowchart given below:

#         Previous Mermaid Flowchart:
        
#         {previous_mermaid_flowchart}
        
#         Current Directory Mermaid Flowchart: 
        
#         {current_directory_mermaid_flowchart}

#         {format_instructions}
#         '''

#         llm_chain = LLMChain(
#             llm = ChatAnthropic(temperature= 0.8,model = "claude-2.0",max_tokens_to_sample=100000),
#             prompt=PromptTemplate(input_variables=["folder_name","folder_structure","previous_mermaid_flowchart",
#                                                 "current_directory_name","current_directory_mermaid_flowchart"],partial_variables={"format_instructions":format_instructions}, template=template),
#             verbose=True,
#         )
#         mermaid_flowchart= llm_chain.predict(folder_name=folder_name,
#                                 folder_structure=folder_structure,
#                                 previous_mermaid_flowchart=previous_mermaid_flowchart,
#                                 current_directory_name=current_directory_name,
#                                 current_directory_mermaid_flowchart=current_directory_mermaid_flowchart)
#         return f"{mermaid_flowchart}"
                
#     def process_folder_mermaid_flowchart(self,folder_path):
#         mermaid_flowchart=""
#         folder_name=os.path.basename(folder_path)
#         folder_structure=os.listdir(folder_path)
#         src_path = os.path.join(folder_path, "src")

#         if os.path.exists(src_path) and os.path.isdir(src_path):
#             for item in os.listdir(src_path): 
                
#                 if item in (".DS_Store", ".gitignore","_pycache_","README.md","pom.xml",".idea",".mvn","mvnw.cmd","HELP.md","target","data","Data"):
#                     continue
#                 item_path = os.path.join(src_path, item) 
#                 if os.path.isdir(item_path):  
#                     Mermaid_Flowchart = self.process_folder_mermaid_flowchart(item_path) 
#                 else:
#                     Mermaid_Flowchart = self.file_mermaid_flowchart(item_path)
                
#                 mermaid_flowchart= self.combine_mermaid_flowchart(folder_name,folder_structure,mermaid_flowchart,
#                                                         item,Mermaid_Flowchart)
#         else:
#             for item in os.listdir(folder_path): 
                
#                 if item in (".DS_Store", ".gitignore","_pycache_","README.md","pom.xml",".idea",".mvn","mvnw.cmd","HELP.md","target","data","Data"):
#                     continue
#                 item_path = os.path.join(folder_path, item) 
#                 if os.path.isdir(item_path):  
#                     Mermaid_Flowchart = self.process_folder_mermaid_flowchart(item_path) 
#                 else:
#                     Mermaid_Flowchart = self.file_mermaid_flowchart(item_path)   
                
#                 mermaid_flowchart= self.combine_mermaid_flowchart(folder_name,folder_structure,mermaid_flowchart,
#                                                         item,Mermaid_Flowchart)
        
#         return mermaid_flowchart

# Github 

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
        




# Higher Level Business Logic

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
    understandable business logic. If the destinationiables in the code have values relevant to the business logic, please include them.I am interested 
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

class HigherLevelBusinessLogic(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        folder_id = request.data.get('id') 
        existing_logic = HighLevel.objects.filter(user=request.user,folder_id=folder_id).first()
       
        if existing_logic:
            # logicData = {
            #     'logic':business_logic,
            #     'user':request.user,
            #     'folder_id':folder_id,
            #     'classDiagram':existing_logic.classDiagram,
            #     'flowChart':existing_logic.flowChart
            # }
            serializer = HighLevelSerializer(existing_logic)
            return Response(serializer.data, status=201)

        else:
            business_logic = process_folder_business_logic(folder_id)

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

def process_folder_mermaid_diagram(folder_id):
    
    folder = FolderUpload.objects.get(folderId=folder_id)

    mermaid_diagram = ""
    
    folder_name = folder.foldername
    
    folder_structure = get_folder_structure(folder_id)

    subfolders = FolderUpload.objects.filter(parentFolder=folder)
    files = FileUpload.objects.filter(parentFolder=folder)
    
    for subfolder in subfolders:
        subfolder_mermaid_diagram = process_folder_mermaid_diagram(subfolder.folderId)
        mermaid_diagram = combine_mermaid_diagram(folder_name, folder_structure, mermaid_diagram, subfolder.foldername, subfolder_mermaid_diagram)

    for file in files:
        file_mermaid_diagram_result = file_mermaid_diagram(file.file)
        mermaid_diagram = combine_mermaid_diagram(folder_name, folder_structure, mermaid_diagram, file.filename, file_mermaid_diagram_result)

    return mermaid_diagram

def higher_level_mermaid_diagram(business_logic):
    
    classDiagram_schema = ResponseSchema(name='mermaid_class_diagram_code', description='This schema represents the Mermaid class diagram code, which is compatible with MermaidJS version 8.11.0. The code should be represented as a valid JSON string with new lines replaced with "\\n".')
    classDiagram_description_schema = ResponseSchema(name='mermaid_class_diagram_code_description', description='This schema represents the description of the class diagram code generated by MermaidJS.')

    response_schema = (classDiagram_schema,classDiagram_description_schema)
    parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = parser.get_format_instructions()
    
    example_code=rpg_example2
    
    template='''
    I want to generate code with backticks for a Mermaid Class diagram using the business logic of a full folder. This Mermaid diagram is used to
    visualize the high-level business logic of a folder's code.
    
    Note: Also, provide code in the correct syntax so that it can be rendered by mermaidjs version 8.11.0. The code should be represented as a valid 
    JSON string with new lines replaced with "\n".

    Example:
    {example_code}
    
    Now, the user will provide the business logic of a full folder as well as associated files. Please generate correct and running code for a
    Mermaid class diagram without any initial text in a JSON format with "mermaid_class_diagram_code" as the key.

    User:{input}
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

        # business_logic= folder.higherlevelbusinesslogic
        # mermaid_diagram=higher_level_mermaid_diagram(business_logic)
        
        # mermaid_diagram = process_folder_mermaid_diagram(folder_id)
        
        # business_logic= '''Based on the provided inputs, here is a high-level summary of the business logic for the Gau folder:

        # The code in this folder relates to an ERP system handling various business functions like inventory management, sales order processing,
        # customer relationship management, and analytics. 

        # Key capabilities include:
        # - User and rights management - Adding, editing, deleting user records and access rights
        # - Master data maintenance - Updating inventory item master data, customer master records, partner records
        # - Pricing and discounts - Determining pricing, discounts, and net prices based on complex hierarchical rules and customer attributes 
        # - Order processing - Handling sales document types like quotes, orders, deliveries along with statuses, dates, quantities
        # - Inventory transactions - Posting inventory movements, serial numbers, batches triggered by sales, purchase etc.
        # - Batch management - Controlling, monitoring background jobs and batches
        # - Reporting and analytics - Customer survey analysis, sales analytics, inventory reports
        # - Auditing - Tracking changes to configuration and master data 
        # - System configuration - Managing system parameters, defaults, schemas across various screens
        # The programs leverage physical and logical database files, APIs, data structures, andbuilt-in RPG functions.
        # The code demonstrates common RPG constructs - file I/O, data structures, modular procedures, calculations, branching, looping, error handling. 
        # In summary, the folder contains a range of business logic required in an ERP system, interacting with databases, programs, interfaces and
        # users. The logic covers both transaction processing as well as reporting/analytics capabilities.'''
#         business_logic = '''
#         The Test 2 folder contains RPG programs and data files related to an HR/payroll system. Key capabilities include:

# User Management
# - Maintain user records in physical file HSAMNPR (keys: user ID, personnel no)  
# - Functions to add, edit, delete, copy, display users
# - Validate required fields on add/edit 
# - Allow adding user to all users or one personnel no
# - Display users in subfile on screen

# Job Configuration
# - Store job-specific settings in HSHSSPF file (keys: short code, param type, user, flag type)
# - Read/update job settings by passing key fields 
# - Add new records if not found
# - Blank fields before writing

# Batch Processing
# - Program to clean up job status records
#    - Read HSHSSPF file 
#    - Delete matching records from HSHSSPR where status = 'M'

# Reporting
# - Program to sum order line amounts
#    - Read order details from AUFWAR
#    - Sum amount field for given order/plant/week/split
#    - Return total sum amount
   
# - Program to print customer survey analysis
#    - Read responses from HSCSSLR1 into data structures
#    - Summarize responses overall and by partner
#    - Calculate average ratings
#    - Print overall and partner reports
   
# Additional Capabilities:   
# - String handling procedures (uppercase, lowercase, memory allocate/deallocate)
# - Printer selection - retrieve and display printers based on user location
# - Menu/selection screen - populate options from file, allow selection, pass to subroutine

# Physical Files:
# - HSAMNPR - User master file
# - HSHSSPF - Job settings file
# - HSHSSPR - Job status file 
# - AUFWAR - Order details file
# - HSCSSLR1 - Survey responses file
#         '''
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
        # print(mermaid_diagram)
        # return Response({"response":mermaid_diagram}, status=200)

# Higher Level Mermaid Flowchart    
  
def process_folder_mermaid_flowchart(folder_id):
    
    folder = FolderUpload.objects.get(folderId=folder_id)

    mermaid_flowchart = ""
    
    folder_name = folder.foldername
    
    folder_structure = get_folder_structure(folder_id)

    subfolders = FolderUpload.objects.filter(parentFolder=folder)
    files = FileUpload.objects.filter(parentFolder=folder)
    
    for subfolder in subfolders:
        subfolder_mermaid_flowchart = process_folder_mermaid_flowchart(subfolder.folderId)
        mermaid_flowchart = combine_mermaid_flowchart(folder_name, folder_structure, mermaid_flowchart, subfolder.foldername, subfolder_mermaid_flowchart)

    for file in files:
        file_mermaid_flowchart_result = file_mermaid_flowchart(file.file)
        mermaid_flowchart = combine_mermaid_flowchart(folder_name, folder_structure, mermaid_flowchart, file.filename, file_mermaid_flowchart_result)

    return mermaid_flowchart

def higher_level_mermaid_flowchart(business_logic):
    
    flowchart_schema = ResponseSchema(name='mermaid_flowchart_code', description='This schema represents the Mermaid flowchart code, designed to generate properly linked nodes that can be rendered by MermaidJS version 8.11.0. The code must be formatted as a valid JSON string, with newline characters replaced by "\\n". All nodes within the code should contain strings to ensure compatibility and avoid issues with special characters.')
    flowchart_description_schema = ResponseSchema(name='flowchart_code_description', description='This schema provides a description of the flowchart code generated by MermaidJS. It includes details about the structure and relationships of the nodes within the flowchart, as well as any additional information relevant to understanding the flowchart.')

    response_schema = (flowchart_schema,flowchart_description_schema)
    parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = parser.get_format_instructions()
    
    example_code=rpg_example3
    
    template='''
    Convert Business Logic to Mermaid Flow chart Diagram of a folder.
    I want to generate code for Mermaid Flow chart diagram using business logic of a folder and Remember this mermaid class diagram code is used by
    developers to visualize the folder's code logic. Also give code in correct syntax so that it can be rendered by mermaidjs 8.11.0 . Make sure the
    blocks are properly linked . Here is also an example how to generate mermaid class diagram using the business logic. and remember also don't give
    any inital word and sentence like here is mermaid flow chart diagram of this business logic.Mermaid flow chart diagram that visually represents 
    this logic.The Mermaid flow chart diagram also should visually represent the flow and sequence of the business logic,including key decision points
    and data dependencies. Ensure that the resulting diagram is comprehensive and self-explanatory. 
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
        
        # mermaid_flowchart = process_folder_mermaid_flowchart(folder_id)
        
        # business_logic= folder.higherlevelbusinesslogic
        # mermaid_flowchart=higher_level_mermaid_flowchart(business_logic)
        
        # business_logic= '''Based on the provided inputs, here is a high-level summary of the business logic for the Gau folder:

        # The code in this folder relates to an ERP system handling various business functions like inventory management, sales order processing,
        # customer relationship management, and analytics. 

        # Key capabilities include:
        # - User and rights management - Adding, editing, deleting user records and access rights
        # - Master data maintenance - Updating inventory item master data, customer master records, partner records
        # - Pricing and discounts - Determining pricing, discounts, and net prices based on complex hierarchical rules and customer attributes 
        # - Order processing - Handling sales document types like quotes, orders, deliveries along with statuses, dates, quantities
        # - Inventory transactions - Posting inventory movements, serial numbers, batches triggered by sales, purchase etc.
        # - Batch management - Controlling, monitoring background jobs and batches
        # - Reporting and analytics - Customer survey analysis, sales analytics, inventory reports
        # - Auditing - Tracking changes to configuration and master data 
        # - System configuration - Managing system parameters, defaults, schemas across various screens
        # The programs leverage physical and logical database files, APIs, data structures, andbuilt-in RPG functions.
        # The code demonstrates common RPG constructs - file I/O, data structures, modular procedures, calculations, branching, looping, error handling. 
        # In summary, the folder contains a range of business logic required in an ERP system, interacting with databases, programs, interfaces and
        # users. The logic covers both transaction processing as well as reporting/analytics capabilities.'''
#         business_logic = '''
#         The Test 2 folder contains RPG programs and data files related to an HR/payroll system. Key capabilities include:

# User Management
# - Maintain user records in physical file HSAMNPR (keys: user ID, personnel no)  
# - Functions to add, edit, delete, copy, display users
# - Validate required fields on add/edit 
# - Allow adding user to all users or one personnel no
# - Display users in subfile on screen

# Job Configuration
# - Store job-specific settings in HSHSSPF file (keys: short code, param type, user, flag type)
# - Read/update job settings by passing key fields 
# - Add new records if not found
# - Blank fields before writing

# Batch Processing
# - Program to clean up job status records
#    - Read HSHSSPF file 
#    - Delete matching records from HSHSSPR where status = 'M'

# Reporting
# - Program to sum order line amounts
#    - Read order details from AUFWAR
#    - Sum amount field for given order/plant/week/split
#    - Return total sum amount
   
# - Program to print customer survey analysis
#    - Read responses from HSCSSLR1 into data structures
#    - Summarize responses overall and by partner
#    - Calculate average ratings
#    - Print overall and partner reports
   
# Additional Capabilities:   
# - String handling procedures (uppercase, lowercase, memory allocate/deallocate)
# - Printer selection - retrieve and display printers based on user location
# - Menu/selection screen - populate options from file, allow selection, pass to subroutine

# Physical Files:
# - HSAMNPR - User master file
# - HSHSSPF - Job settings file
# - HSHSSPR - Job status file 
# - AUFWAR - Order details file
# - HSCSSLR1 - Survey responses file
#         '''    
#         business_logic='''
# The code in this folder deals with various aspects of customer and pricing data management, including:

# - Rebate code handling - converting old rebate codes to new codes, linking customers to rebate codes, producing outputs for research and auditing (HSHI12.txt)

# - Customer master data updates - updating customer numbers and branch codes, deleting and recreating customer number records (HSHI17.txt) 

# - Pricing and discounts - looking up pricing, discounts, surcharges, etc. based on customer, product, quantity, and other criteria (HS0095.txt)

# - Account master updates - converting account types, updating associated G/L accounts (HSHI_KL.txt) 

# - Sales data integration - transferring sales data from Excel to CSV, merging into a database file (HSHI_ESZ.txt)

# The core themes are:

# - Master data management - updating critical master data like customer records, accounts, pricing

# - Sales integration - bringing in external sales data and merging into databases

# - Rebate processing - converting rebate codes and linking to customers

# - Pricing/discount logic - applying pricing rules and discounts 

# - Reporting/auditing - generating outputs for research, auditing, debugging 

# - Data validation - type checking, error handling, duplicate checking

# Key files used include customer masters, account ledgers, sales orders, pricing tables, and rebate codes.

# The programs focus on batch processing and data integration. There is some interactivity via displays and subfiles. But core logic is file-based processing, merging data sources, master data management.'''
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
