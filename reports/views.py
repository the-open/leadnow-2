import csv
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from forms import ImportCsvForm
from models import Supporter, Campaign, Email, Action

def home(request):
  return render(request, 'home.html', {})
  
def query(request):
  return render(request, 'query.html', {})
  
def import_csv(request):
  # Get the uploaded CSV
  if request.method == 'POST':
    form = ImportCsvForm(request.POST, request.FILES)
    
    if form.is_valid():
      reader = csv.reader(form.cleaned_data['file_name'])
      i = 0

      # TODO: what if the ordering of headers changes?

      for row in reader:
        # skip headers
        if i == 0:
          pass
          
        # insert objects
        else:
        
          # build supporter object
          try:
            supporter = Supporter.objects.get(id=row[1])
          except Supporter.DoesNotExist:
            supporter = Supporter()
            supporter.id = row[1]
            supporter.created = row[2]
            supporter.modified = row[3]
            supporter.postal_code = row[45]
            supporter.save()
            
          # build campaign object
          campaign, created = Campaign.objects.get_or_create(name=row[6])
          if created:
            campaign.campaign_type = row[5]
            campaign.campaign_status = row[9]
            campaign.save()
          
          # build email object
          if form.cleaned_data['file_type'] == 'e':
            e = Email()
            e.supporter = supporter
            e.campaign = campaign
            
            if row[10]:
              e.opened = row[7] + " " + row[8]
            if row[11]:
              e.clicked = row[7] + " " + row[8]
            if row[13]:
              e.hard_bounce = row[7] + " " + row[8]
            if row[14]:
              e.soft_bounce = row[7] + " " + row[8]
            if row[15]:
              e.unsub = row[7] + " " + row[8]

            e.save()

          # build action object            
          else:
            a = Action()
            a.supporter = supporter
            a.campaign = campaign
            
            a.timestamp = row[7] + " " + row[8]
            a.browser = row[41]
            a.url = row[42]
            a.source = row[43]

            a.save()
        
        i += 1
        
      messages.add_message(request, messages.INFO, 'Import complete!')
      return HttpResponseRedirect(reverse('home'))
  
  
  else:
    form = ImportCsvForm()
    
  return render(request, 'import_csv.html', {'form': form})
  
