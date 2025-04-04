from django.urls import path
from datashow.views import center_data, head, centerLeft1, centerLeft2, centerRight2, centerRight1, bottomLeft, \
    bottomRight

urlpatterns = [
    path("centerData/", center_data, name="centerData"),
    path("head/", head, name="head"),
    path("centerLeft1/", centerLeft1, name="centerLeft1"),
    path("centerLeft2/", centerLeft2, name="centerLeft2"),
    path("centerRight1/", centerRight1, name="centerRight1"),
    path("centerRight2/", centerRight2, name="centerRight2"),
    path("bottomLeft/", bottomLeft, name="bottomLeft"),
    path("bottomRight/", bottomRight, name="bottomRight"),
]
