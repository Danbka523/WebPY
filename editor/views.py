import os
import json
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import Http404
from courses.models import Assignment
from users.models import UserProfile

# Create your views here.
def editor(request,assignment_id=0):
    file_content =""
    user_directory = UserProfile.objects.get(user_id=request.user.id).directory_path
    root = settings.MEDIA_ROOT + '\\'+ user_directory
    file =  request.GET.get("file")
    try:
        assignment = get_object_or_404(Assignment, id=assignment_id)
    except Http404:
        assignment = Assignment(id=0)
    if request.POST.get('code_output')!=None:
        code_output = request.POST.get('code_output')
        
        with open(root +'\\'+ file, "w") as f:
            try:
                f.write(json.loads(code_output))
            except IOError:
                print (IOError.errno)          
    try:
        with open(root + "/" + file) as f:
            file_content = f.read()
    except:
        pass
    
    if request.GET.get('isnew')=='true':
        fp=open(root + "\\" + request.GET.get('file'),'w')
        fp.close()
    
    
    if request.GET.get('isdelete')=='true':
        os.remove(root + "\\" + request.GET.get('file'))
    

    files = os.listdir(root)
    return render(request,'editor.html', {'files': files, 'file_content':file_content, 'file':file, 'assignment':assignment})
