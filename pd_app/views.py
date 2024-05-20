from django.shortcuts import render, redirect
import os
from collections import defaultdict
from pd_app.pd_model import predict_plagiarism

def upload_folder(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for file in files:
            handle_uploaded_file(file)

        uploaded_files = [os.path.join('media', f) for f in os.listdir('media') if os.path.isfile(os.path.join('media', f))]
        uploaded_files.sort()

        if len(uploaded_files) < 2:
            return render(request, 'upload.html', {'error': 'Please upload at least two files.'})

        pairwise_scores = []

        for i in range(len(uploaded_files)):
            for j in range(i + 1, len(uploaded_files)):
                file1 = uploaded_files[i]
                file2 = uploaded_files[j]
                score = predict_plagiarism(file1, file2)
                pairwise_scores.append({
                    'file1': os.path.basename(file1),
                    'file2': os.path.basename(file2),
                    'score': score
                })

        context = {
            'pairwise_scores': pairwise_scores
        }

        return render(request, 'result.html', context)
    return render(request, 'upload.html')

def handle_uploaded_file(f):
    file_path = os.path.join('media', f.name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def result(request):
    return render(request, 'result.html')
