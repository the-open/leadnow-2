from django.db import models

class Supporter(models.Model):
  class Meta:
    db_table = 'supporters'
    
  created = models.DateTimeField(db_index=True)
  modified = models.DateTimeField(db_index=True)
  
  postal_code = models.CharField(max_length=25, blank=True, null=True)

class Campaign(models.Model):
  class Meta:
    db_table = 'campaigns'
  
  name = models.CharField(max_length=255, db_index=True)
  campaign_type = models.CharField(max_length=25)
  campaign_status = models.CharField(max_length=1)

class Email(models.Model):
  class Meta:
    db_table = 'emails'
    
  supporter = models.ForeignKey(Supporter)
  campaign = models.ForeignKey(Campaign)
  
  sent = models.DateTimeField(blank=True, null=True)
  opened = models.DateTimeField(blank=True, null=True, db_index=True)
  clicked = models.DateTimeField(blank=True, null=True, db_index=True)
  hard_bounce = models.DateTimeField(blank=True, null=True, db_index=True)
  soft_bounce = models.DateTimeField(blank=True, null=True, db_index=True)
  unsub = models.DateTimeField(blank=True, null=True, db_index=True)

class Action(models.Model):
  class Meta:
    db_table = 'actions'
    
  supporter = models.ForeignKey(Supporter)
  campaign = models.ForeignKey(Campaign)
  
  timestamp = models.DateTimeField(db_index=True)
  
  browser = models.CharField(max_length=255, blank=True, null=True)
  url = models.CharField(max_length=255, blank=True, null=True)
  source = models.CharField(max_length=3, blank=True, null=True, db_index=True)

class Query(models.Model):
  class Meta:
    db_table = 'queries'
    
  creator = models.ForeignKey('auth.User')
  created = models.DateTimeField(auto_now_add=True)
  
  vis_emails = models.BooleanField(default=False)
  vis_actions = models.BooleanField(default=False)
  
