import json
from bson import json_util
from django.http import HttpResponse
from datashow.models import cars_data

# Create your views here.
def center_data(request):
    data = cars_data.objects.all().only('center_data')

    # 提取为字典列表（仅包含指定字段）
    documents = [doc.to_mongo().to_dict() for doc in data]
    documents = documents[0]['center_data']

    # 转换为 JSON
    json_data = json.dumps(documents, default=json_util.default,ensure_ascii=False)
    return HttpResponse(json_data, content_type='application/json')

def head(request):
    data = cars_data.objects.all().only('head_info')

    # 提取为字典列表（仅包含指定字段）
    documents = [doc.to_mongo().to_dict() for doc in data]
    documents = documents[0]['head_info']

    # 转换为 JSON
    json_data = json.dumps(documents, default=json_util.default,ensure_ascii=False)
    return HttpResponse(json_data, content_type='application/json')

def centerLeft1(request):
    data = cars_data.objects.all().only('center_left1')

    # 提取为字典列表（仅包含指定字段）
    documents = [doc.to_mongo().to_dict() for doc in data]
    documents = documents[0]['center_left1']

    # 转换为 JSON
    json_data = json.dumps(documents, default=json_util.default,ensure_ascii=False)
    return HttpResponse(json_data, content_type='application/json')

def centerLeft2(request):
    data = cars_data.objects.all().only('center_left2')

    # 提取为字典列表（仅包含指定字段）
    documents = [doc.to_mongo().to_dict() for doc in data]
    documents = documents[0]['center_left2']


    # 转换为 JSON
    json_data = json.dumps(documents, default=json_util.default,ensure_ascii=False)
    return HttpResponse(json_data, content_type='application/json')

def centerRight1(request):
    data = cars_data.objects.all().only('center_right1')

    # 提取为字典列表（仅包含指定字段）
    documents = [doc.to_mongo().to_dict() for doc in data]
    documents = documents[0]['center_right1']


    # 转换为 JSON
    json_data = json.dumps(documents, default=json_util.default,ensure_ascii=False)
    return HttpResponse(json_data, content_type='application/json')

def centerRight2(request):
    data = cars_data.objects.all().only('center_right2')

    # 提取为字典列表（仅包含指定字段）
    documents = [doc.to_mongo().to_dict() for doc in data]
    documents = documents[0]['center_right2']


    # 转换为 JSON
    json_data = json.dumps(documents, default=json_util.default,ensure_ascii=False)
    return HttpResponse(json_data, content_type='application/json')

def bottomLeft(request):
    data = cars_data.objects.all().only('bottom_left')

    # 提取为字典列表（仅包含指定字段）
    documents = [doc.to_mongo().to_dict() for doc in data]
    documents = documents[0]['bottom_left']


    # 转换为 JSON
    json_data = json.dumps(documents, default=json_util.default,ensure_ascii=False)
    return HttpResponse(json_data, content_type='application/json')

def bottomRight(request):
    data = cars_data.objects.all().only('bottom_right')

    # 提取为字典列表（仅包含指定字段）
    documents = [doc.to_mongo().to_dict() for doc in data]
    documents = documents[0]['bottom_right']


    # 转换为 JSON
    json_data = json.dumps(documents, default=json_util.default,ensure_ascii=False)
    return HttpResponse(json_data, content_type='application/json')
