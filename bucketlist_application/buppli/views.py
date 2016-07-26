from django.shortcuts import render, redirect
from buppli.forms import LoginForm
from django.views.generic import View, TemplateView
from buppli.models import BucketList
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template import RequestContext

# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('/')


class IndexView(TemplateView):
    template_name = 'index.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['loginform'] = LoginForm()
        context['bucketlists'] = (BucketList.objects.filter(is_public=True)
                                  .all())
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            context = self.get_context_data(**kwargs)
            context['loginform'] = form
            return render(request, self.template_name, context)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if not user:
            context = self.get_context_data(**kwargs)
            context['loginform'] = form
            context['error'] = "Username of password Incorrect"
            return render(request, self.template_name, context)
        login(request, user)
        response = redirect(
            '/bucketlists',
            context_instance=RequestContext(request)
        )
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            response = redirect(
                '/bucketlists',
                context_instance=RequestContext(request)
            )
            return response
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class BucketListView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'bucketlists.html'

    def get_context_data(self, **kwargs):
        context = super(BucketListView, self).get_context_data(**kwargs)
        context['bucketlists'] = self.request.user.bucketlists
        return context
