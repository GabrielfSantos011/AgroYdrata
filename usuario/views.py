from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from django.contrib import auth   

def cadastro(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        senha1 = request.POST.get("senha1")
        senha2 = request.POST.get("senha2")

        if senha1 != senha2:
            messages.error(request, "Senhas não são iguais.")
            return redirect('cadastro')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Este email já foi cadastrado, por favor digite outro.")
            return redirect('cadastro')

        usuario = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=senha1  
        )
        usuario.save()
        messages.success(request, "Cadastro efetuado com sucesso! :D")
        return redirect('login')

    return render(request, 'usuario/cadastro.html')

def login(request):

  if request.method == 'POST':
        email = request.POST.get("email")
        senha = request.POST.get("senha")

      
        """ email = form['email'].value()
        senha = form['senha'].value() """

        usuario = auth.authenticate(
            request,
            email=email,
            password=senha
        )

        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, f"{email} logado com sucesso!")
            return redirect('predicao')
        else:
            messages.error(request, "Erro ao efetuar login! :(")
            return redirect('login')    
    
  return render(request,'usuario/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request,"Logout efetuado com sucesso")
    return redirect('login')