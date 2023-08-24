from itertools import chain

from .views import index_template

app_name = "Customers"

urlpatterns = list(chain(index_template))

