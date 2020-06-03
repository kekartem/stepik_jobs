from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View

from djumanji.models import Company, Speciality, Vacancy


class MainView(View):
    def get(self, request):

        data = {}

        specialities = Speciality.objects.all()
        companies = Company.objects.all()

        data['companies'] = companies
        data['specialities'] = specialities

        for obj in specialities:
            obj.count = obj.vacancies.count()

        for obj in companies:
            obj.count = obj.vacancies.count()

        return render(request, 'index.html', context=data)


class VacanciesView(View):
    def get(self, request):
        data = {}
        vacancies = Vacancy.objects.all()
        data['vacancies'] = vacancies
        data['amount'] = len(vacancies)
        return render(request, 'vacancies.html', context=data)


class CategoryView(View):
    def get(self, request, code):
        data = {'vacancies': Vacancy.objects.filter(speciality__code=code)}
        data['amount'] = len(data['vacancies'])
        data['title'] = Speciality.objects.get(code=code).title
        return render(request, 'category.html', context=data)


class CompanyView(View):
    def get(self, request, id):
        all_id = []
        for obj in Company.objects.all():
            all_id.append(obj.id)
        if id not in all_id:
            raise Http404

        data = {}
        data['vacancies'] = Vacancy.objects.filter(company_id=id)
        data['amount'] = len(data['vacancies'])
        data['company'] = Company.objects.get(id=id)
        data['vacancies'] = Vacancy.objects.filter(company_id=id)
        return render(request, 'company.html', context=data)


class VacancyView(View):
    def get(self, request, id):
        data = {}
        data['vacancy'] = Vacancy.objects.get(id=id)
        return render(request, 'vacancy.html', context=data)
