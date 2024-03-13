from django.shortcuts import render, HttpResponse
import joblib
from django.conf import settings
import os
import joblib
import json
#import pickle

# Mendapatkan jalur lengkap ke direktori model
model_path = os.path.join(settings.STATICFILES_DIRS[0], 'modelgbr_6040_denganpoly2.joblib')

def home(request):
    return render(request, 'home.html')
    # return HttpResponse("ini home")

def search(request):
    return render(request, 'search.html')
    # return HttpResponse("ini home")

def team(request):
    return render(request, 'team.html')
    # return HttpResponse("ini home")

def journal(request):
    return render(request, 'journal.html')
    # return HttpResponse("ini home")

def predict(request) :
    prediction = [0]

    # Memuat model
    print("Memuat Model GBR")
    # Memuat model
    print("Memuat Model GBR")
    # with open(model_path, 'rb') as f:
    #     model = pickle.load(f)
    model = joblib.load(model_path)
    
    # Jika model berhasil dimuat, cetak pesan ke konsol
    print("Model berhasil dimuat.")
    # Jika model berhasil dimuat, cetak pesan ke konsol
    print("Model berhasil dimuat.")

    if request.method == 'POST' :
        input_dict = {
            'Molecular_weight MW (g/mol)' : float(request.POST['MW']),
            'pKa' : float(request.POST['pKa']),
            'Log P' : float(request.POST['logP']),
            'Log S' : float(request.POST['logS']),
            'Polar Surface Area (Å2)' : float(request.POST['PSA']),
            'Polarizability (Å3)' : float(request.POST['polarizability']),
            'HOMO (eV)' : float(request.POST['E-HOMO']),
            'LUMO (eV)' : float(request.POST['E-LUMO']),
            'Electronegativity (eV)' : float(request.POST['electrophilicity']),
            ' ΔN_Fe ' : float(request.POST['fraction_electron_shared'])
        }

        # Define columns to scale
        columns_to_scale = ['Molecular_weight MW (g/mol)', 'pKa', 'Log P', 'Log S', 'Polar Surface Area (Å2)',
                                    'Polarizability (Å3)', 'HOMO (eV)', 'LUMO (eV)', 'Electronegativity (eV)', ' ΔN_Fe ']
        
        normalization_path = os.path.join(settings.STATICFILES_DIRS[0], 'min_max_values.json')
        # Load normalization parameters from JSON
        with open(normalization_path, 'r') as file:
            normalization_params = json.load(file)

        for feature in columns_to_scale:
            min_value = normalization_params[feature]["min"]
            max_value = normalization_params[feature]["max"]
            input_dict[feature] = (
                input_dict[feature] - min_value) / (max_value - min_value)
            
        
        prediction = model.predict(
            [
                [ 
                    input_dict['Molecular_weight MW (g/mol)'],
                    input_dict['pKa'],
                    input_dict['Log P'],
                    input_dict['Log S'],
                    input_dict['Polar Surface Area (Å2)'],
                    input_dict['Polarizability (Å3)'],
                    input_dict['HOMO (eV)'],
                    input_dict['LUMO (eV)'],
                    input_dict['Electronegativity (eV)'],
                    input_dict[' ΔN_Fe '],
                ]
            ]
        )
    
        _max = 99.00
        _min = 67.70
        # pred_invers = (prediction[0] * (_max - _min)) + _min
        # y_new_pred_best = str(y_new_pred_best[0].round(2))
    print(prediction[0])
    prediction = f'{round(prediction[0],2)} %'
    output = {"output": prediction }

    return render(request, 'app.html', output)

    # context = {
    #     'prediction_result' : prediction,
    # }
    # return render(request, 'app.html', output)

def ml_ops(request) :
    result = ""
    model_name = "models/"+ str(request.POST.get('algorithm_option')) +"_"+ str(request.POST.get('split_option')) +"_"+ str(request.POST.get('normalization_option')) + ".joblib"

    if request.method == 'POST' :
        model = joblib.load(model_name)
        input_dict = {
            'Molecular_weight MW (g/mol)' : float(request.POST['MW']),
            'pKa' : float(request.POST['pKa']),
            'Log P' : float(request.POST['logP']),
            'Log S' : float(request.POST['logS']),
            'Polar Surface Area (Å2)' : float(request.POST['PSA']),
            'Polarizability (Å3)' : float(request.POST['polarizability']),
            'HOMO (eV)' : float(request.POST['E-HOMO']),
            'LUMO (eV)' : float(request.POST['E-LUMO']),
            'Electronegativity (eV)' : float(request.POST['electrophilicity']),
            ' ΔN_Fe ' : float(request.POST['fraction_electron_shared'])
        }

        # Define columns to scale
        columns_to_scale = ['Molecular_weight MW (g/mol)', 'pKa', 'Log P', 'Log S', 'Polar Surface Area (Å2)',
                                    'Polarizability (Å3)', 'HOMO (eV)', 'LUMO (eV)', 'Electronegativity (eV)', ' ΔN_Fe ']
        
        input_normalization = str(request.POST.get('normalization_option'))

        if input_normalization != "None" :
            normalization_path = "models/normalization_scalers/" + input_normalization

            # Load normalization parameters from JSON
            with open(f"{normalization_path}.json", 'r') as file:
                normalization_params = json.load(file)

            if input_normalization == "MinMaxScaler()" :
                for feature in columns_to_scale:
                    min_value = normalization_params[feature]["min"]
                    max_value = normalization_params[feature]["max"]
                    input_dict[feature] = (
                        input_dict[feature] - min_value) / (max_value - min_value)
                    
            elif input_normalization == "StandardScaler()" :
                for feature in columns_to_scale:
                    mean_value = normalization_params[feature]["mean"]
                    std_value = normalization_params[feature]["std"]
                    input_dict[feature] = (
                        input_dict[feature] - mean_value) / std_value
                    
            elif input_normalization == "RobustScaler()" :
                for feature in columns_to_scale:
                    center_value = normalization_params[feature]["center"]
                    scale_value = normalization_params[feature]["scale"]
                    input_dict[feature] = (
                        input_dict[feature] - center_value) / scale_value
            
        prediction = model.predict(
            [
                [ 
                    input_dict['Molecular_weight MW (g/mol)'],
                    input_dict['pKa'],
                    input_dict['Log P'],
                    input_dict['Log S'],
                    input_dict['Polar Surface Area (Å2)'],
                    input_dict['Polarizability (Å3)'],
                    input_dict['HOMO (eV)'],
                    input_dict['LUMO (eV)'],
                    input_dict['Electronegativity (eV)'],
                    input_dict[' ΔN_Fe '],
                ]
            ]
        )

        result = f'{float(prediction[0])} %'
    context = {"result" : result }

    return render(request, 'manual_app.html', context)

def view_pdf(request,orang):
    if orang == "Nicholaus":
        pdf_path = "/static/filepdf/Nicholaus.pdf"
    elif orang =="Dzaki":
        pdf_path = "/static/filepdf/Dzaki.pdf"
    elif orang =="Nibras":
        pdf_path = "/static/filepdf/Nibras.pdf"
    elif orang =="Cornell":
        pdf_path = "/static/filepdf/Cornell.pdf"
    elif orang=="paktotok1":
        pdf_path = "/static/filepdf/paktotok1.pdf"
    elif orang=="pakakrom1":
        pdf_path = "/static/filepdf/pakakrom1.pdf"
    elif orang=="pakakrom2":
        pdf_path = "/static/filepdf/pakakrom2.pdf"
    elif orang=="pakbudi1":
        pdf_path = "/static/filepdf/pakbudi1.pdf"
    elif orang=="2022 - Experimental investigation":
        pdf_path = "/static/filepdf/2022 - Experimental investigation.pdf"
    elif orang=="2023 - CTC":
        pdf_path = "/static/filepdf/2023 - CTC.pdf" 
    elif orang=="2023 - Jommit":
        pdf_path = "/static/filepdf/2023 - Jommit.pdf" 
    elif orang=="2023 - JPCS":
        pdf_path = "/static/filepdf/2023 - JPCS.pdf" 
    elif orang=="2023 - MTC":
        pdf_path = "/static/filepdf/2023 - MTC.pdf" 

    return render(request, 'view_pdf.html', {'pdf_path': pdf_path})
    # return HttpResponse("ini home")


# Create your views here.
