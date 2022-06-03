from rest_framework.generics import ListAPIView
from apis.serializers import MyHomeSerializer
from apis.models import MyHome


class MyHomeListView(ListAPIView):
    serializer_class = MyHomeSerializer
    queryset = MyHome

    def get_queryset(self):
        request = self.request
        target = request.GET.get("target")
        region = request.GET.get("region")
        if target and region:
            queryset = MyHome.objects.filter(target=target, region=region)
            return queryset
        else:
            queryset = MyHome.objects.all()
        return queryset
