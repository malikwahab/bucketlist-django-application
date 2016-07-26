from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'username',
                               }))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'password'
                               }))


''' class BucketListView(TemplateView):

    model = BucketList
    template_name = "index.html"
    context_object_name = "bucketlists"
    # get_object_or_404(Model, pk=data)

    def get_context_data(self, **kwargs):
        context = super(BucketListView, self).get_context_data(**kwargs)
        context['bucketlists'] = BucketList.objects.all()
        return context


class BucketListEdit(CreateView):

    model = BucketList
    fields = ['name', 'is_public']
    template_name = "edit.html"

    def get_context_data(self, **kwargs):
        context = super(BucketListEdit, self).get_context_data(**kwargs)
        context['form'] = BucketListForm()
        return context '''
