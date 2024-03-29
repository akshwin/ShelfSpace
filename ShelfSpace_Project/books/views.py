from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from .models import UploadedFile
from .forms import FileUploadForm
from storages.backends.s3boto3 import S3Boto3Storage
from django.db.models import Sum

@login_required
def book_list(request):
    files = UploadedFile.objects.all()
    return render(request, 'books/file_list.html', {'files': files})


@login_required
def upload_book(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.save()
            files = UploadedFile.objects.filter(user=request.user)
            return redirect('books:file_list')
    else:
        form = FileUploadForm()
    return render(request, 'books/upload_file.html', {'form': form})

@login_required
def download_book(request, unique_token):
    file_instance = get_object_or_404(UploadedFile, unique_token=unique_token)
    response = HttpResponse(file_instance.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename={file_instance.file.name}'
    return response

# views.py

@login_required
def delete_book(request, unique_token):
    # Try to find the file by unique_token
    file_instance = get_object_or_404(UploadedFile, unique_token=unique_token)

    # If file_instance is not found, try to find by hashed_file_id
    if not file_instance:
        hashed_file_id = unique_token
        try:
            file_instance = UploadedFile.objects.get(hashed_file_id=hashed_file_id)
        except UploadedFile.DoesNotExist:
            return HttpResponse("File not found.", status=404)

    storage = S3Boto3Storage()
    file_path = file_instance.file.name

    if storage.exists(file_path):
        storage.delete(file_path)

    file_instance.delete()

    files = UploadedFile.objects.filter(user=request.user)
    return redirect('books:file_list')



@login_required
def view_book(request, unique_token):
    file_instance = get_object_or_404(UploadedFile, unique_token=unique_token)
    file_path = file_instance.file.name
    file_extension = file_path.split('.')[-1].lower()
    
    if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
        return FileResponse(file_instance.file, content_type='image/'+file_extension)
    elif file_extension == 'pdf':
        response = FileResponse(file_instance.file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename={file_instance.file.name}'
        return response
    else:
        return redirect('books:download_file', file_id=file_instance.id)
    
    
def share_book(request, unique_token):
    file_instance = get_object_or_404(UploadedFile, unique_token=unique_token)
    file_path = file_instance.file.name
    file_extension = file_path.split('.')[-1].lower()
    if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
        return FileResponse(file_instance.file, content_type='image/'+file_extension)
    elif file_extension == 'pdf':
        response = FileResponse(file_instance.file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename={file_instance.file.name}'
        return response
    else:
        return redirect('books:download_file', unique_token=unique_token)