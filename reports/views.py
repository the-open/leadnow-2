import csv
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import connections
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from forms import ImportCsvForm, QueryForm
from models import Supporter, Campaign, Email, Action, Query

def home(request):
  return render(request, 'home.html', {})

# Display a list of saved queries, plus an area to enter a new custom query
def query(request):
  campaigns = Campaign.objects.all()
  email_campaigns = campaigns.filter(campaign_type='EBC')
  action_campaigns = campaigns.filter(campaign_type='ETT')
  queries = Query.objects.all()
  return render(request, 'query.html', {'queries': queries,
                                         'email_campaigns': email_campaigns,
                                         'action_campaigns': action_campaigns,
                                        })


# When we have saved queries, this will let you see the details of a saved query
def query_details(request, query_id):
  return render(request, 'query.html', {})


# AJAX call to save a query
def query_save(request):
  name = request.POST.get('name', None)
  qry = request.POST.get('qry', None)
  can_email = request.POST.get('viz_email', None)
  can_action = request.POST.get('viz_action', None)

  if name and qry:
    saved_query = Query()
    saved_query.name = name
    saved_query.qry = qry
    if can_email:
      saved_query.vis_emails = True
    if can_action:
      saved_query.vis_actions = True
    saved_query.save()

    return HttpResponse("Query saved!")

  else:
    return HttpResponse("Unable to save")


# Run an actual query!
def report(request, query_id=None):

  saved_query = None
  if query_id:
    saved_query = Query.objects.get(id=query_id)

  # eventually we won't use direct access to the POST param for this...
  elif not saved_query and not request.POST.get('qry', None):
    messages.add_message(request, messages.ERROR, 'No query provided!')
    return HttpResponseRedirect(reverse('query'))

  # TODO: validate, ensure they don't attempt an INSERT/UPDATE/DELETE operation!
  # this code is an injection attack waiting to happen; good thing we trust our users!
  # (famous last words?)

  # We've solved this with a readonly database user, yay!
  # But still TODO: catch the permissions error if they try to write and
  # handle it gracefully.
  if saved_query:
    qry = saved_query.qry
  else:
    qry = request.POST['qry']

  cursor = connections['readonly'].cursor()

  cursor.execute(qry)

  headings = [col[0] for col in cursor.description]
  results = cursor.fetchall()

  # TODO: paginate results, maybe... just maybe... =)

  return render(request, 'report.html', {'qry': qry, 'headings': headings, 'results': results, 'saved_query': saved_query})


# Import a spreadsheet of data
def import_csv(request):
  # Get the uploaded CSV
  if request.method == 'POST':
    form = ImportCsvForm(request.POST, request.FILES)

    if form.is_valid():
      reader = csv.reader(form.cleaned_data['file_name'])
      i = 0
      headings = {}

      for row in reader:
        # skip headers
        if i == 0:
          for idx, column in enumerate(row):
            headings[column] = idx


        # insert objects
        else:

          # build supporter object
          try:
            supporter = Supporter.objects.get(id=row[1])
          except Supporter.DoesNotExist:
            supporter = Supporter()
            supporter.id = row[headings['Supporter ID']]
            supporter.created = row[headings['Date Created']]
            supporter.modified = row[headings['Date Modified']]
            supporter.postal_code = row[headings['Postal Code']]
            supporter.save()

          # build campaign object
          campaign, created = Campaign.objects.get_or_create(name=row[6])
          if created:
            campaign.campaign_type = row[headings['Campaign Type']]
            campaign.campaign_status = row[headings['Campaign Status']]
            campaign.save()

          # build email object
          if form.cleaned_data['file_type'] == 'e':
            e = Email()
            e.supporter = supporter
            e.campaign = campaign

            if row[headings['Campaign Data 1']]:
              e.opened = row[headings['Campaign Date']] + " " + row[headings['Campaign Time']]
            if row[headings['Campaign Data 2']]:
              e.clicked = row[headings['Campaign Date']] + " " + row[headings['Campaign Time']]
            if row[headings['Campaign Data 4']]:
              e.hard_bounce = row[headings['Campaign Date']] + " " + row[headings['Campaign Time']]
            if row[headings['Campaign Data 5']]:
              e.soft_bounce = row[headings['Campaign Date']] + " " + row[headings['Campaign Time']]
            if row[headings['Campaign Data 6']]:
              e.unsub = row[headings['Campaign Date']] + " " + row[headings['Campaign Time']]

            e.save()

          # build action object
          else:
            a = Action()
            a.supporter = supporter
            a.campaign = campaign


            a.timestamp = row[headings['Campaign Date']] + " " + row[headings['Campaign Time']]
            a.browser = row[headings['Campaign Data 32']]
            a.url = row[headings['Campaign Data 33']]
            a.source = row[headings['Campaign Data 34']]

            a.save()

        i += 1

      messages.add_message(request, messages.INFO, 'Import complete!')
      return HttpResponseRedirect(reverse('home'))


  else:
    form = ImportCsvForm()

  return render(request, 'import_csv.html', {'form': form})
