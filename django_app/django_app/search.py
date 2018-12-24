from django.http import HttpResponse
from django.shortcuts import render_to_response
import base64
import requests
import imagenet_id_to_name

def request_classification(image_url):
    SERVER_URL = 'http://localhost:8501/v1/models/resnet:predict'
    IMAGE_URL = image_url
    # Download the image
    print("download image...")
    try:
        dl_request = requests.get(IMAGE_URL, stream=True)
        dl_request.raise_for_status()    

        # Compose a JSON Predict request (send JPEG image in base64).
        print("Compose a JSON Predict request")
        predict_request = '{"instances" : [{"b64": "%s"}]}' % base64.b64encode(dl_request.content).decode('ascii')

        # Send few requests to warm-up the model.
        #print("warm-up the model")
        #for _ in range(3):
            #response = requests.post(SERVER_URL, data=predict_request)
            #response.raise_for_status()

        # Send few actual requests and report average latency.
        print("send requests")
        total_time = 0
        num_requests = 1
        for _ in range(num_requests):
            response = requests.post(SERVER_URL, data=predict_request)
            response.raise_for_status()
            total_time += response.elapsed.total_seconds()
            prediction = response.json()['predictions'][0]

        print('Prediction class: {},class name: {}, avg latency: {} ms'.format( prediction['classes'],imagenet_id_to_name.imagenet_name_dict[prediction['classes']], (total_time*1000)/num_requests))
    
        return imagenet_id_to_name.imagenet_name_dict[prediction['classes']] 
    except:
        return 'something wrong happend'

# start page
def search_form(request):
    return render_to_response('search_form.html')


# result page
def search(request):
    request.encoding = 'utf-8'
    print(request.GET)
    if len(request.GET)>0:
        message = request.GET['info']+'\n\n'+ request_classification(request.GET['info'])
        #return HttpResponse(message)
        image_url = request.GET['info']
        predict_name = request_classification(request.GET['info'])
        return render_to_response('search_result.html',{'image_url':image_url,'predict_name':predict_name})
    else:
        return render_to_response('search_result.html',{'image_url':'incorrect','predict_name':'Please input right image URL'})
