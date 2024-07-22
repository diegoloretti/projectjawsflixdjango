from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from .forms import CriarContaForm, FormHomepage
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs)  # Redireciona para homepage.html
        
    def get_success_url(self):
        email = self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)
        if usuarios.exists():
            return reverse('filme:login') + f'?email={email}&from_homepage=true'
        else:
            return reverse('filme:criarconta') + f'?email={email}&from_homepage=true'

class Homefilmes(LoginRequiredMixin, ListView):
    model = Filme
    template_name = 'homefilmes.html'

class DetalhesFilme(LoginRequiredMixin, DetailView):
    model = Filme
    template_name = 'detalhes_filme.html'

    def get(self, request, *args, **kwargs):
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filmes_relacionados'] = self.model.objects.filter(categoria=self.get_object().categoria)
        return context

class Pesquisa(LoginRequiredMixin, ListView):
    model = Filme
    template_name = 'pesquisa.html'

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            return self.model.objects.filter(titulo__icontains=termo_pesquisa)
        else:
            return None
        
class PaginaPerfil(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'editar_perfil.html'
    fields = ['first_name', 'last_name', 'email']

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.id != self.kwargs['pk']:
                return self.redirect_to_own_profile()
        else:
            return redirect('filme:login')
        return super().dispatch(request, *args, **kwargs)

    def redirect_to_own_profile(self):
        own_profile_url = reverse('filme:editarperfil', kwargs={'pk': self.request.user.id})
        return redirect(own_profile_url)

    def get_success_url(self):
        return reverse('filme:homefilmes')
    
class Criarconta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')
    
    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get('from_homepage') == 'true':
            email = self.request.GET.get('email', '')
            initial['email'] = email
        return initial

