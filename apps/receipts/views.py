from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    memberships = request.user.memberships.select_related("business")
    return render(request, "receipts/home.html", {"memberships": memberships})
