from itertools import chain
from .views import sales_templates

app_name = "Sales"

urlpatterns = list(chain(sales_templates))