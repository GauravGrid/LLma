
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatAnthropic
from langchain.chains import ConversationChain
from rest_framework.decorators import api_view
import keys
from .service import convert_rpg_to_java
from django.http import JsonResponse
from .service import business_logic
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from .service import mermaid_dig
from .service import generateJava,generateFlowChart,generateClassDiagram,javaCompiler
from django.http import JsonResponse

import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FolderUpload, FileUpload,User,Logic,JavaCode,MermaidDiagrams
import zipfile
from django.core.files import File
from .authorisation import CustomIsAuthenticated,TokenAuthentication
import tempfile
from .serializers import FileSerializer,LogicSerializer,JavaCodeSerializer,MermaidDiagramSerializer
from django.http import Http404



def index(request):
    return JsonResponse({'Message':'Hello World. Welcome to CodeBridge'})

@csrf_exempt
def claude_call(request):
    llm_fe = ChatAnthropic(
        temperature=0.1, 
        anthropic_api_key=keys.anthropic_key,
        model='claude-instant-v1.1-100k',
        max_tokens_to_sample=100000  
    )   

    conversionToLogic = ConversationChain(
    llm=llm_fe, 
    verbose=True, 
    memory=ConversationBufferMemory()
    )
    uploaded_file = request.FILES['file']
    file_contents = uploaded_file.read()
    print(file_contents)
    # code=request.file()
    #storing 1st output in output1
    output1 = conversionToLogic.predict(input = '''Translate the following RPG code to business logic:
        {}
        like for the following code:
        **free
        dsply 'Hello World';
        return;
        the following is the business logic:
        Display the message "Hello World".
        '''.format(file_contents))
    print(output1)
    output2=conversionToLogic.predict(input= 'Critically Analyse the above business logic')
    print(output2)
    output3 = conversionToLogic.predict(input = 'keeping above points in mind regenerate the business logic' )
    print(output3)
    return JsonResponse({'BusinessLogic' : output1,
                         'Updated BusinessLogic': output3})


def upload_rpg_code(request):
     if request.method == 'POST':
          if  request.content_type=='text/plain':
            # Retrieve the RPG code from the request data
            rpg_code = request.body.decode('utf-8')
            if not rpg_code:
             return HttpResponse('RPG code not found', status=400, content_type='text/plain')
            
          elif 'rpg_file' in request.FILES:
            # Get the uploaded file from the request
            uploaded_file = request.FILES['rpg_file']

            # Read the content of the uploaded file
            rpg_code = uploaded_file.read().decode('utf-8')
          else:
            return HttpResponseBadRequest('No RPG code or file provided.')
          
        
          Blogic= business_logic(rpg_code)
          request.session['blogic'] = Blogic
          #java_code = convert_rpg_to_java(rpg_code)
          data= {'Business Logic': Blogic}
         
         
          return JsonResponse(data)
          # return JsonResponse(data1)
          
          
     return JsonResponse({'error': 'Invalid request method'}, status=405)
       

          # response = HttpResponse(f"Business logic:{logic}", content_type='text/plain')
          # return response
          #   Return an error response if the request method is not POST
          #  return HttpResponse('Invalid request method', status=405, content_type='text/plain')
          #return JsonResponse(data)
         # return JsonResponse({'error': 'Invalid request method'}, status=405)

          


def mermaid_diagram(request):
     if request.method == 'GET':
        Blogic = request.session.get('blogic', '')
        mermaid_code = mermaid_dig(Blogic)
        # Create a dictionary containing the mermaid code
        data = {'mermaid_code':mermaid_code}

        # Return the dictionary as a JSON response
        return JsonResponse(data)
     return JsonResponse({'error': 'Invalid request method'}, status=405)
       



class FolderUploadView(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        project_name = request.POST.get('project_name') 
        username = request.user
        user = User.objects.get(username=username)

        
        parent_folder = FolderUpload.objects.create(foldername=project_name, parentFolder=None, user=user)

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
                self.process_folder(temp_dir, parent_folder,request)  

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

    def process_folder(self, folder_path, parent_folder,request):
        username = request.user
        user = User.objects.get(username=username)
        for item in os.listdir(folder_path): 
            item_path = os.path.join(folder_path, item) 
            if os.path.isdir(item_path):  
                subfolder = FolderUpload.objects.create(foldername=item, parentFolder=parent_folder, user=user)
                self.process_folder(item_path, subfolder,request) 
            else:
                rpg_extensions = ['.rpgle', '.sqlrpgle', '.clle', '.RPGLE', '.SQLRPGLE', '.CLLE']
                if any(item.endswith(ext) for ext in rpg_extensions):
                    with open(item_path, 'rb') as file:
                        print('fileSelected',item)
                        file_contents = file.read().decode('utf-8')
                        file_upload = FileUpload(
                            filename=item,
                            file=file_contents,
                            parentFolder=parent_folder,
                            user=user
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
            return Response(project_list)


class FileContentAPIView(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, file_id):
        try:
            file = FileUpload.objects.get(fileId=file_id, user=request.user)
            serializer = FileSerializer(file)
            return Response(serializer.data)
        except FileUpload.DoesNotExist:
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

    
class MermaidAPIView(APIView):
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

    def generate_diagrams(self, file_id, logic_id):
        file = self.get_object(file_id)
        logic = self.get_object(file_id, logic_id)
        logic_str = logic.logic
        mermaidDiagramClass = generateClassDiagram(logic_str)
        mermaidDiagramFlow = generateFlowChart(logic_str)
        
        diagram_data = {
            'classDiagram': mermaidDiagramClass,
            'flowChart': mermaidDiagramFlow,
            'logic': logic_id,
            'user': self.request.user,
            'file': file_id
        }
        
        existing_diagram = MermaidDiagrams.objects.filter(file=file, logic=logic, user=self.request.user).first()
        
        if existing_diagram:
            serializer = MermaidDiagramSerializer(existing_diagram, data=diagram_data)
        else:
            serializer = MermaidDiagramSerializer(data=diagram_data)
        
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            return None

    def get(self, request, file_id, logic_id):
        file = self.get_object(file_id)
        logic = self.get_object(file_id, logic_id)
        diagram = MermaidDiagrams.objects.get(file=file, logic=logic, user=request.user)
        serializer = MermaidDiagramSerializer(diagram)
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
            new_diagram_data = self.generate_diagrams(file_id, logic_id)
            if new_diagram_data:
                return Response(new_diagram_data, status=201)
            else:
                return Response({'error': 'Failed to generate diagrams'}, status=400)

    def put(self, request, file_id, logic_id):
        
        new_diagram_data = self.generate_diagrams(file_id, logic_id)
        if new_diagram_data:
            return Response(new_diagram_data)
        else:
            return Response({'error': 'Failed to generate diagrams'}, status=400)
    
    def delete(self, request, file_id, logic_id):
        logic = self.get_object(file_id, logic_id)
        file = self.get_object(file_id)
        code = MermaidDiagrams.objects.filter(file=file, logic=logic, user=request.user).first()
        code.delete()
        return Response(status=204)    
        
        
class JavaCompilerView(APIView):
    permission_classes = [CustomIsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self,request):
        javaCompiler()
        return Response(status=200)
