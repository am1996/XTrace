from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from EPCISEvent.models import EPCISEvent

class EPCISEventIndex(LoginRequiredMixin, ListView):
    model = EPCISEvent
    template_name = 'EPCISEvent/index.html'
    context_object_name = 'epcis_events'
    paginate_by = 20

class EPCISEventDetails(LoginRequiredMixin, DetailView):
    model = EPCISEvent
    template_name = 'EPCISEvent/details.html'
    context_object_name = 'event'

class EPCISEventCreate(LoginRequiredMixin, CreateView):
    model = EPCISEvent
    template_name = 'EPCISEvent/create.html'
    success_url = '/web/epcis-events/'
    fields = ['event_type', 'event_time', 'event_timezone_offset', 'action', 'biz_step', 'disposition', 'read_point', 'biz_location', 'epc_list']

class EPCISEventUpdate(LoginRequiredMixin, UpdateView):
    model = EPCISEvent
    template_name = 'EPCISEvent/update.html'
    success_url = '/web/epcis-events/'
    fields = ['event_type', 'event_time', 'event_timezone_offset', 'action', 'biz_step', 'disposition', 'read_point', 'biz_location', 'epc_list']

class EPCISEventDelete(LoginRequiredMixin, DeleteView):
    model = EPCISEvent
    template_name = 'EPCISEvent/epcisevent_confirm_delete.html'
    success_url = '/web/epcis-events/'
