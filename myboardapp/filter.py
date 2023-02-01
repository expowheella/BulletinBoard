from django_filters import FilterSet, CharFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Comment



# создаём фильтр
class CommentFilter(FilterSet):

    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Comment
        fields = ('bulletin',)  # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)
        # fields = {
        #     'bulletin': ['exact'],
        # }
    #
    # @property
    # def qs(self):
    #     parent = super().qs
    #     user = getattr(self.request, 'author')
    #     # user = 'body'
    #     return parent.filter(username=user)