from django.shortcuts import render
from django.shortcuts import render,HttpResponse,get_object_or_404
from . import sort_date_time
import json
def home(request):
	return render(request,'track/abcd.html')
def track_it(request):
	t=request.GET['tracking_id']
	json_file=sort_date_time.solve(t,request.GET['company'])
	return HttpResponse(json.dumps(json_file), content_type="application/json")
	