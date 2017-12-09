from django.shortcuts import render
from django.http import HttpResponse


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
    return HttpResponse(
        "Hello World. We will build the inventory management site here."
    )



