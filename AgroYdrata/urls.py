from django.urls import path,include
from app_AgroYdrata import views
from django.contrib import admin



urlpatterns = [
    #rota, view responsavel, nome de referencia
    #agroydrata.com
    path('historico/', views.historico_view, name='historico'),

    path('excluir_dado/<int:dado_id>/', views.excluir_dado, name='excluir_dado'),
    path('', include('usuario.urls')),

    path('predicao/',views.home,name='predicao'),
    #agroydrata.com/dados
    path('dados/', views.dados, name='listagem_dados'),

    path('', views.agroydrata, name='agroydrata'),

    # Rota da pagina de predicao agua
    path('predicao_agua/', views.predicao_agua, name='predicao_agua'),
    path('admin/', admin.site.urls),
    path('gerar_relatorio_pdf/', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
 
]



