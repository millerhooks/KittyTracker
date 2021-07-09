from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, ListView
from .models import Medication, Litter, Cat, CareLog, FosterAlert, VetVisit
from django.urls import reverse_lazy
from .forms import CatForm


class DashboardView(TemplateView):
    template_name = "pages/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['medications']  = Medication.objects.all()
        context['litters']      = Litter.objects.all()
        context['cats']         = Cat.objects.all()
        context['logs']         = CareLog.objects.all()
        context['alerts']       = FosterAlert.objects.all()
        context['visits']       = VetVisit.objects.all()
        return context



class MedicationCreate(CreateView):
    model = Medication
    fields = ['name',
               'manufacturer',
               'duration',
               'frequency',
               'dosage_unit',
               'dosage_guidelines',
               'notes']

class MedicationUpdate(UpdateView):
    model = Medication
    fields = ['name',
              'manufacturer',
              'duration',
              'frequency',
              'dosage_unit',
              'dosage_guidelines',
              'notes']

class MedicationDelete(DeleteView):
    model = Medication
    success_url = reverse_lazy('meds-list')

class MedicationList(ListView):
    model = Medication
    # paginate_by = 100



class LitterCreate(CreateView):
    model = Litter
    fields = ['name',
               'slug',
               'foster_manager',
               'notes']

    def form_valid(self, form):
        form.instance.foster_manager = self.request.user
        return super().form_valid(form)

class LitterUpdate(UpdateView):
    model = Litter
    fields = ['name',
              'slug',
              'foster_manager',
              'notes']


class LitterDelete(DeleteView):
    model = Litter
    success_url = reverse_lazy('litter-list')

class LitterList(ListView):
    model = Litter
    # paginate_by = 100



class CatCreate(CreateView):
    model = Cat
    form_class = CatForm

    def form_valid(self, form):
        form.instance.foster_manager = self.request.user
        return super().form_valid(form)

class CatUpdate(UpdateView):
    model = Cat
    form_class = CatForm


class CatDelete(DeleteView):
    model = Cat
    success_url = reverse_lazy('cat-list')

class CatList(ListView):
    model = Cat
    # paginate_by = 100



class CareLogCreate(CreateView):
    model = CareLog
    exclude = ['created']

    def form_valid(self, form):
        form.instance.foster_manager = self.request.user
        return super().form_valid(form)

class CareLogUpdate(UpdateView):
    model = CareLog
    exclude = ['created']

class CareLogDelete(DeleteView):
    model = CareLog
    success_url = reverse_lazy('log-list')

class CareLogList(ListView):
    model = CareLog
    # paginate_by = 100



from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass

