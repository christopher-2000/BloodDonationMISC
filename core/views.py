from django.shortcuts import redirect, render

from .forms import DonorForm
from .models import Donor, Initiative, OfficeBearer, image_url


def home(request):
    initiatives = Initiative.objects.prefetch_related("images").all()
    donors = Donor.objects.filter(is_approved=True)
    stats = {
        "donors": donors.count(),
        "groups": donors.values("blood_group").distinct().count(),
        "locations": donors.values("current_location").distinct().count(),
    }
    # Data for the initiative detail popup (enlarged carousel + description).
    initiatives_json = [
        {
            "title": item.title,
            "description": item.description,
            "link": item.link,
            "images": [image_url(img.image) for img in item.images.all()],
        }
        for item in initiatives
    ]
    return render(
        request,
        "home.html",
        {
            "initiatives": initiatives,
            "initiatives_json": initiatives_json,
            "stats": stats,
        },
    )


def about(request):
    bearers = OfficeBearer.objects.all()
    return render(request, "about.html", {"bearers": bearers})


def register_donor(request):
    # Only signed-in admins may register donors; visitors are told to contact
    # an admin/coordinator instead of being bounced to the login page.
    if not (request.user.is_active and request.user.is_staff):
        return render(request, "register.html", {"restricted": True})

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
    donors = Donor.objects.filter(is_approved=True)
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
