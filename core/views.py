from django.shortcuts import redirect, render

from .forms import DonorForm
from .models import Donor, Initiative, OfficeBearer


def home(request):
    initiatives = Initiative.objects.all()
    donors = Donor.objects.all()
    stats = {
        "donors": donors.count(),
        "groups": donors.values("blood_group").distinct().count(),
        "locations": donors.values("current_location").distinct().count(),
    }
    return render(
        request, "home.html", {"initiatives": initiatives, "stats": stats}
    )


def about(request):
    bearers = OfficeBearer.objects.all()
    return render(request, "about.html", {"bearers": bearers})


def register_donor(request):
    if request.method == "POST":
        form = DonorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("register_success")
    else:
        form = DonorForm()
    return render(request, "register.html", {"form": form})


def register_success(request):
    return render(request, "success.html")


def search_donors(request):
    donors = Donor.objects.all()
    blood_group = request.GET.get("blood_group", "")
    location = request.GET.get("location", "").strip()

    if blood_group:
        donors = donors.filter(blood_group=blood_group)
    if location:
        donors = donors.filter(current_location__icontains=location)

    return render(
        request,
        "search_donors.html",
        {
            "donors": donors,
            "blood_group": blood_group,
            "location": location,
            "blood_groups": Donor.BLOOD_GROUPS,
        },
    )
