from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader

import os
import time
from datetime import datetime
import logging 

from django.core.files.base import File
from .detection import FoodDetector
from .apps import DetectorConfig

logging.basicConfig(
    level=logging.INFO, 
    filename=f'{DetectorConfig.name}.log', 
    filemode='a', 
    format='%(asctime)s %(levelname)s %(message)s'
)

os.makedirs(f'{DetectorConfig.name}/temp', exist_ok=True)

def index(request):
    template = loader.get_template(f'templates/index.html')
    
    if request.method == 'GET' :
        params = request.GET.dict()
    elif request.method == 'POST' :
        params = request.POST.dict()
    else:
        context = {'message': 'something went wrong'}
        return HttpResponse(template.render(context, request), status=400)
    message = 'use <a href="http://127.0.0.1:8000/detector/">detecor</a> to handle image'
    context = {'message': message}
    return HttpResponse(template.render(context, request))

@csrf_exempt 
def img_handler(request):
    
    images = request.FILES.dict()
    logging.info(f'received files: {images.keys()}')
    if 'image' not in images.keys():
        template = loader.get_template(f'templates/index.html')
        context = {'message': 'no image given'}
        return HttpResponse(template.render(context, request), status=400)
    
    img = images['image']
    name = f'{DetectorConfig.name}/temp/img_{datetime.now().strftime(r"%d.%m.%y_%H.%M.%S.%f")}.jpg'
    with open(name, 'wb') as f:
        f.write(img.read())
    
    model = FoodDetector()
    logging.info(f'detection for {name} started')
    detections = model(name)
    logging.info(f'detection for {name} ended with results: {detections}')
    os.remove(name)
    
    return JsonResponse({
        "detections": detections,
    })