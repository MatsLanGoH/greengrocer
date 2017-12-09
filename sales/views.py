from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Fruit

# TODO
# TODO: All views need the user to be logged in (except for login site)


# Create views here
def top(request):
    """
    販売管理View（TOP）を返す

    :param request:
    :return:
    """
    # TODO: Add login_required decorator or mixin.
    return render(request,
                  'top.html')


class FruitListView(generic.ListView):
    model = Fruit

    # TODO: Make sure these are ordered by reverse creation date!
    def get_queryset(self):
        return Fruit.objects.order_by('-created_at')





