from django.shortcuts import render
from .analyzer import analyze_url
from .cosmos import save_scan, get_scans

def index(request):
    result = None

    if request.method == "POST":
        url = request.POST.get("url")
        result = analyze_url(url)
        save_scan(url, result)

    filter_type = request.GET.get("filter")
    scans = get_scans(filter_type)

    return render(request, "index.html", {
        "result": result,
        "scans": scans
    })