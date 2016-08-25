from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.views.generic import TemplateView

from buppli.forms import LoginForm, SignUpForm
from buppli.models import BucketList


# Create your views here.


def logout_view(request):
    """Log out user and redirect to homapage."""
    logout(request)
    return redirect('/')


class IndexView(TemplateView):
    """Handles all HTTP request to the homepage.

    Inherits:
        TemplateView
    """
    template_name = 'index.html'
    form_class = LoginForm
    second_form_class = SignUpForm

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['loginform'] = LoginForm()
        context['signupform'] = SignUpForm()
        context['bucketlists'] = (BucketList.objects.filter(is_public=True)
                                  .all())
        return context

    def post(self, request, *args, **kwargs):
        """Checks the submitted form, then deligate to the appropriate func."""
        if "login" in request.POST:
            return self.post_login(request, *args, **kwargs)
        return self.post_new_user(request, *args, **kwargs)

    def post_login(self, request, *args, **kwargs):
        """Handles request from the Login form."""
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

    def post_new_user(self, request, *args, **kwargs):
        """Handles post request from the Sign Up form."""
        form = self.second_form_class(request.POST)
        if form.is_valid():
            new_user = form.save()
            return self.post_login(request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        context["signuperror"] = form.errors
        context["signup"] = form
        return render(request, self.template_name, context)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            response = redirect(
                '/bucketlists',
                context_instance=RequestContext(request)
            )
            return response
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class BucketListView(LoginRequiredMixin, TemplateView):
    """Viewset for the /bucketlists page.

    Inherits:
        LoginRequiredMixin: Ensure all request is authenticated
        TemplateView
    """
    login_url = '/'
    template_name = 'bucketlists.html'

    def get_context_data(self, **kwargs):
        """Get all the bucketlist belonging to the requesting user."""
        context = super(BucketListView, self).get_context_data(**kwargs)
        context['bucketlists'] = self.request.user.bucketlists
        return context


class PublicBucketListView(LoginRequiredMixin, TemplateView):
    """Viewset for the /public-bucketlists page.

    Inherits:
        LoginRequiredMixin: Ensure all request is authenticated
        TemplateView
    """
    login_url = '/'
    template_name = 'public.html'

    def get_context_data(self, **kwargs):
        """Get all the bucketlist belonging to the requesting user."""
        context = super(PublicBucketListView, self).get_context_data(**kwargs)
        context['bucketlists'] = (BucketList.objects.filter(is_public=True)
                                  .all())
        return context
