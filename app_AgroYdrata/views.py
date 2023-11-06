import numpy as np
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Dados
from django.http import HttpResponse
import pandas as pd
import pytz
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa

# Carregar seu conjunto de dados
# Carregar seu conjunto de dados
data = pd.read_csv('app_AgroYdrata/crops1.csv')

# Separar features (dados de entrada) e target (saída desejada)
X = data[['N', 'P', 'K', 'temperature(in degree celsius)', 'humidity(in percentage)', 'ph of soil', 'rainfall( in mm )']]
y = data['water-availability(liters per year)']
labels = data['label']

# Aplicar One-Hot Encoding nas variáveis categóricas (labels)
encoder = OneHotEncoder(sparse=False)
encoded_labels = encoder.fit_transform(labels.values.reshape(-1, 1))

# Combinar as features e as variáveis categóricas codificadas
X = np.hstack((X.values, encoded_labels))

# Criar um dicionário para mapear o nome da planta ao modelo treinado
plant_models = {}

# Treinar um modelo para cada tipo de planta
unique_plants = labels.unique()
for plant in unique_plants:
    # Filtrar os dados para o tipo de planta atual
    plant_X = X[labels == plant]
    plant_y = y[labels == plant]

    # Dividir os dados em conjunto de treinamento e teste (60% treinamento, 40% teste)
    X_train, X_test, y_train, y_test = train_test_split(plant_X, plant_y, test_size=0.4, random_state=42)

    # Modelo de regressão
    model_params = {'n_estimators': 400, 'max_depth': 4, 'min_samples_split': 5, 'learning_rate': 0.01}
    model = GradientBoostingRegressor(random_state=42, **model_params)
    model.fit(X_train, y_train)

    # Armazenar o modelo treinado no dicionário
    plant_models[plant] = model

def fazer_predicao(N, P, K, temperature, humidity, ph, rainfall, tp_planta):
    # Aplicar One-Hot Encoding na variável 'tp_planta'
    tp_planta_encoded = encoder.transform(np.array([[tp_planta]]))

    # Combinar os valores de entrada com a variável categórica codificada
    input_data = np.hstack((np.array([[N, P, K, temperature, humidity, ph, rainfall]]), tp_planta_encoded))

    # Obter o modelo adequado com base no tipo de planta
    selected_model = plant_models.get(tp_planta)
    if selected_model:
        water_needed = selected_model.predict(input_data)[0]
        return water_needed
    else:
        return None

def predicao_agua(request):
    if request.method == 'POST':
        try:
            # Obtenha os valores dos campos do formulário
            nitrogenio = request.POST.get('nitrogenio')
            fosforo = request.POST.get('fosforo')
            potassio = request.POST.get('potassio')
            ph = request.POST.get('ph')
            temperatura = request.POST.get('temperatura')
            umidade = request.POST.get('umidade')
            precipitacao = request.POST.get('precipitacao')
            tp_planta = request.POST.get('tp_planta')  # Manter a seleção do tipo de planta
            sao_paulo_tz = pytz.timezone('America/Sao_Paulo')

            # Verifique se algum dos campos está em branco
            if any(val == '' for val in [nitrogenio, fosforo, potassio, ph, temperatura, umidade, precipitacao]):
                return HttpResponse("Por favor, preencha todos os campos.")

            # Converta os valores para números em ponto flutuante (float)
            nitrogenio = float(nitrogenio)
            fosforo = float(fosforo)
            potassio = float(potassio)
            ph = float(ph)
            temperatura = float(temperatura)
            umidade = float(umidade)
            precipitacao = float(precipitacao)

            resultado = fazer_predicao(nitrogenio, fosforo, potassio, temperatura, umidade, ph, precipitacao, tp_planta)

            if resultado is not None:
                novo_dado = Dados(
                    nitrogenio=nitrogenio,
                    fosforo=fosforo,
                    potassio=potassio,
                    ph=ph,
                    temperatura=temperatura,
                    umidade=umidade,
                    precipitacao=precipitacao,
                    tp_planta=tp_planta,
                    resultado=resultado,
                    horario_insercao=timezone.now().astimezone(sao_paulo_tz),  # Defina o fuso horário
                    usuario=request.user 
                )
                novo_dado.save()
                print("Dados salvos no banco de dados.")

                return render(request, 'predicao/resultado.html', {'resultado': resultado})
            else:
                return HttpResponse("Erro na predição de água.")
        except ValueError:
            return HttpResponse("Por favor, preencha todos os campos com valores numéricos válidos.")
    else:
        return HttpResponse("Método de solicitação não permitido.")
    

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado.")
        return redirect('login')
    return render(request, 'predicao/home.html')

def historico_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado.")
        return redirect('login')

    # Filtrar os dados com base no usuário logado
    dados = Dados.objects.filter(usuario=request.user)

    search_query = request.GET.get('search', '')  # Obtenha o parâmetro de pesquisa da URL ou use uma string vazia como padrão
    if search_query:
        # Se houver uma pesquisa, filtre os dados com base na pesquisa
        dados = dados.filter(tp_planta__icontains=search_query)

    return render(request, 'predicao/historico.html', {'dados': dados, 'search_query': search_query})


def excluir_dado(request, dado_id):
    if request.method == 'POST':
        try:
            dado = Dados.objects.get(id_dados=dado_id)
            dado.delete()
            return redirect('historico')  # Redirecionar de volta para a página de histórico após a exclusão
        except Dados.DoesNotExist:
            return HttpResponse("Dado não encontrado.")
    else:
        return HttpResponse("Método de solicitação não permitido.")

def dados(request):
    if request.method == 'POST':
        # Salvar os dados da tela no banco de dados
        novo_dado = Dados()
        novo_dado.nitrogenio = request.POST.get('nitrogenio')
        novo_dado.fosforo = request.POST.get('fosforo')
        novo_dado.potassio = request.POST.get('potassio')
        novo_dado.ph = request.POST.get('ph')
        novo_dado.temperatura = request.POST.get('temperatura')
        novo_dado.umidade = request.POST.get('umidade')
        novo_dado.precipitacao = request.POST.get('precipitacao')
        novo_dado.tp_planta = request.POST.get('tp_planta')
        novo_dado.save()

        # Exibe os dados cadastrados na tela
        dados = {
            'dados': Dados.objects.all()
        }

        return render(request, 'predicao/dados.html', dados)
    else:
        # Se a solicitação não for POST, você pode redirecionar o usuário de volta à página inicial ou fazer outra coisa adequada.
        return HttpResponse("Método de solicitação não permitido.")
    
def gerar_relatorio_pdf(request):
    dado_id = request.GET.get('dado_id')

    try:
        dado = Dados.objects.get(id_dados=dado_id)
    except Dados.DoesNotExist:
        return HttpResponse("Dado não encontrado.")

    # Adicione 'resultado' ao contexto
    context = {
        'dado': dado,
        'resultado': dado.resultado  # Adicione a variável 'resultado' ao contexto
    }

    template = get_template('predicao/historico_pdf.html')
    html = template.render(context)  # Passe o contexto ao renderizar o modelo

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="historico.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response

# Verificar esse bloco abaixo e deletar(Parece que esta duplicado as 2 def abaixo)
def home (request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado.")
        return redirect('login')
    return render(request,'predicao/home.html')

def agroydrata (request):
    return render(request,'predicao/agroydrata.html')


def dados(request):
    if request.method == 'POST':
        # Salvar os dados da tela no banco de dados
        novo_dado = Dados()
        novo_dado.nitrogenio = request.POST.get('nitrogenio')
        novo_dado.fosforo = request.POST.get('fosforo')
        novo_dado.potassio = request.POST.get('potassio')
        novo_dado.ph = request.POST.get('ph')
        novo_dado.temperatura = request.POST.get('temperatura')
        novo_dado.umidade = request.POST.get('umidade')
        novo_dado.precipitacao = request.POST.get('precipitacao')
        novo_dado.tp_planta = request.POST.get('tp_planta')
        novo_dado.save()

        # Exibe os dados cadastrados na tela
        dados = {
            'dados': Dados.objects.all()
        }

        return render(request, 'predicao/dados.html', dados)
    else:
        # Se a solicitação não for POST, você pode redirecionar o usuário de volta à página inicial ou fazer outra coisa adequada.
        return HttpResponse("Método de solicitação não permitido.")
