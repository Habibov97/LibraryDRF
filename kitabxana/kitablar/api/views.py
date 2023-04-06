from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from kitablar.api.serializers import YorumSerializers, KitabSerializers
from kitablar.models import Kitab, Yorum
from kitablar.api.permissions import IsAdminUserOrReadOnly, IsYorumSahibiOrReadOnly
from kitablar.api.pagination import SmallPagination, LargePagination

#|CONCRETE VIEWS|

class KitabListCreateAPIView(generics.ListCreateAPIView):    #Biz artiq 'generics.ListCreateAPIView' komekliyi ile herhansisa mixin yazmagimiza ehtiyyac qalmadan yeni her hansisa get , post fucn yazmadan bele datamizi elde ede bilirik.
    queryset = Kitab.objects.all().order_by('-id')    # 'order_by('-id')' her hansi xeta olmasin deye asagidan yuxari idleri sirala deyirik
    serializer_class = KitabSerializers
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = SmallPagination

class KitabDetailAPIView(generics.RetrieveUpdateDestroyAPIView):   #eyni ilede 'generics.RetrieveUpdateDestroyAPIView' komeyi ile pk , get, put, delete ve s. bolmeleride iki setir kodla elde ede bilirik.
    queryset = Kitab.objects.all()
    serializer_class = KitabSerializers
    permission_classes = [IsAdminUserOrReadOnly]

class YorumCreateAPIView(generics.CreateAPIView):
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        kitab_pk = self.kwargs.get('kitab_pk')
        kitab = get_object_or_404(Kitab, pk=kitab_pk)
        kullanici = self.request.user
        yorumlar = Yorum.objects.filter(kitab=kitab, yorum_sahibi=kullanici)
        if yorumlar.exists():
            raise ValidationError('Bir kitaba yalniz bir yorum yapila bilir')
        serializer.save(kitab=kitab, yorum_sahibi=kullanici)

    
class YorumDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializers
    permission_classes = [IsYorumSahibiOrReadOnly]
    






                                
                                
                                
                                
                                
                                
####### SADE OLARAQ GenericAPIView TANIMI #######

##### Bir view ucun class duzelib ona ListModelMixin CreateModelMixin GenericAPIView import edib onu classimiza verdiyimizde elave views kod setirlerine ehtiyyac qalmir. Bizim ucun isi
##### get methodu ucun ListModelMixin , post methodu ucun ise CreateModelMixin mixinlerine hell edir . Bize GenericAPIView >>>> go to definition deyib ''query set, serializer_class'' bolmesini alib
##### viewin icine copy etmek qalir. Daha sonrasi get , post ucun func duzeldib asagidaki bolmede yazilanlari etmek lazimdir. 


# class KitabListCreateAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Kitab.objects.all()                         # genericAPI isletmek ucun querysetine ehtiyyacimiz var. Go to definition deyerek icinden ceke bilerik
#     serializer_class = KitabSerializers

#     #Listelemek
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)          # biz bu 'get' kod line i CreateModelsMixin e  go to definition deyib aldiq. Mixinler views islerini bizim ucun avtomaik edirler 
    
#     #Yaratabilmek
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)        # biz bu 'post' kod line i ListModelsMixin e  go to definition deyib bu bolmeni aldiq. Mixinler views islerini bizim ucun avtomaik edirler 
