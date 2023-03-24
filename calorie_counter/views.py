from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import QueryForm, BmiCalForm
from django.contrib import messages
from .models import Meal
import requests, json
  
#api_key="6pIp439f4RLIbT7xrfvFCA==cF8G9DbtdP7n5LGU"

def home(request):
    return render(request, 'calorie_counter/home.html')

def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')                       
            messages.success(request, f'Account created for {user}!')  
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/sign_up.html', {'form': form})


def querysearch(request):
    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            request.session['question'] = query
            return redirect('queryresults')
    else:
        form = QueryForm()
        
    return render(request, 'calorie_counter/querysearch.html')


def queryresults(request):
    query = request.session['question']

    if type(query) == list:
        my_list = []
        my_list = request.session['question']
        api_results = []
        
        for query in my_list:
            api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
            api_request = requests.get(api_url + query, headers={'X-Api-Key': '6pIp439f4RLIbT7xrfvFCA==cF8G9DbtdP7n5LGU'})
            
            try:
                api = json.loads(api_request.content)  
                api_results.append(api) 
            
            except Exception as e:
                api = "oops! There was an error"
                print(e)
        total_calories = total_cal_count(api_results)
        results = {'api_results': api_results, 'calories': total_calories}
        return render(request, 'calorie_counter/calorie_count.html', results)
    
    else:
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(api_url + query, headers={'X-Api-Key': '6pIp439f4RLIbT7xrfvFCA==cF8G9DbtdP7n5LGU'})
        
        try:
            api = json.loads(api_request.content)
        
        except Exception as e:
            api = "oops! There was an error"
            print(e)
            
    return render(request, 'calorie_counter/queryresults.html', {'api': api})
    
def total_cal_count(api_results):
    total_cal = 0
    for i in range(0,len(api_results)):
        cal_dict = api_results[i][0]
        total_cal += cal_dict['calories']
    return total_cal
    
       
def bmi_cal(request):
    if request.method == "POST":
        form = BmiCalForm(request.POST)
        
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            ex_type = form.cleaned_data['exercise']
            
            ht = (height/100)
            if age > 18:
                bmi = weight / (ht * ht)
                cal = counter(weight,height,age,gender,ex_type)
                data = {'cal': cal, 'bmi': bmi}   
                return render(request, 'calorie_counter/bmi_result.html', data)
            
            else:
                messages.error(request, f'You are underage to use this BMI calculation!')        
    
    else:
        form = BmiCalForm()
        
    return render(request, 'calorie_counter/bmi_cal.html', {'form': form})


def counter(wt,ht,age,gender,ex_type):
    if gender == 'male':
        bmr = 66.47 + (13.75*wt) + (5.003*ht) - (6.755*age)
    else:
        bmr = 655.1 + (9.563*wt) + (1.85*ht) - (4.676*age)
        
    if ex_type == 'sedentary':
        amr = bmr * 1.2
    elif ex_type == 'light':
        amr = bmr * 1.375
    elif ex_type == 'moderate':
        amr = bmr * 1.55
    elif ex_type == 'active':
        amr = bmr * 1.725
    else:
        amr = bmr * 1.9
        
    return amr
    

class MealCreateView(CreateView):
    model = Meal
    fields = ['breakfast', 'lunch', 'snacks', 'dinner']
    template_name = 'calorie_counter/meal_form.html'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['breakfast'].widget.attrs['placeholder'] = 'eg. sandwich, juice, etc'
        form.fields['lunch'].widget.attrs['placeholder'] = 'eg. rice, sausage etc'
        form.fields['dinner'].widget.attrs['placeholder'] = 'eg. salad, bread, chapati etc'
        form.fields['snacks'].widget.attrs['placeholder'] = 'eg. fruits, nuts, burger etc'
        return form
    
    def post(self, request):
        bf = request.POST.get('breakfast')
        lun = request.POST.get('lunch')
        sna = request.POST.get('snacks')
        din = request.POST.get('dinner')
        food_list = [bf, lun, sna, din]
        request.session['question'] = food_list
        return redirect('queryresults')
     
