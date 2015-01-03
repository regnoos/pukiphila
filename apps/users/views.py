from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core import urlresolvers
from django.forms.util import ErrorList, format_html
from apps.albumes.models import Membership

from .models import User
from .forms import UserCreationForm


class UlErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_ul(self):
        if not self:
            return ''
        return format_html('<ul class="parsley-error-list">%s</ul>' % ''.join(['<li class="required">%s</li>' % e for e in self]))


class SignupView(CreateView):
    template_name = 'users/signup.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_invalid(self, form):
        # form = UserCreationForm()
        return super(SignupView, self).form_invalid(form)

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)

        return super(SignupView, self).form_valid(form)


# def register(request, template_name="registration/register.html"):
#     if request.method == 'POST':
#         postdata = request.POST.copy()
#         form = UserCreationForm(postdata)
#         if form.is_valid():
#             form.save()
#             un = postdata.get('username','')
#             pw = postdata.get('password1','')
#             from django.contrib.auth import login, authenticate
#                 new_user = authenticate(username=un, password=pw)
#                 if new_user and new_user.is_active:
#                     login(request, new_user)
#                     url = urlresolvers.reverse('my_account')
#                     return HttpResponseRedirect(url)
#     else:
#         form = UserCreationForm()
#     page_title = 'User Registration'
#     return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def signup(request, template_name="users/signup.html"):
    if request.method == 'POST':
        postdata = request.POST.copy()
        un = postdata.get('username', '')
        # if MyUser.objects.filter(username=un).exists():
        #     raise forms.ValidationError(u'Username "%s" is already in use.' % un)

        form = UserCreationForm(postdata)
        if form.is_valid():
            form.save()
            pw = postdata.get('password1', '')
            from django.contrib.auth import login, authenticate
            new_user = authenticate(username=un, password=pw)

            if new_user and new_user.is_active:
                login(request, new_user)
            #     #Esta parte add al user a un grupo...
            #     gn = postdata.get('account_type', '')
            #     group = Group.objects.get(id=gn)
            #     user = MyUser.objects.get(username=un)
            #     user.groups.add(group)
            #     user.save()
            #     url = urlresolvers.reverse('my_account')
            #     return HttpResponseRedirect(url)
                url = urlresolvers.reverse('/')
                return HttpResponseRedirect(url)
    else:
        form = UserCreationForm()
    page_title = 'User Registration'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


class ArtistListView(ListView):
    template_name = 'users/artist_list.html'
    context_object_name = 'artist'
    queryset = Membership.objects.filter(role=1)

    paginate_by = 10

    def get_queryset(self):
        artists = [a.user for a in self.queryset]

        return artists

    # def get_context_data(self, **kwargs):
    #     context = super(ArtistListView, self).get_context_data(**kwargs)
    #
    #     context['artists'] = artists
    #
    #     return context


class ArtistProfileView(DetailView):
    model = User
    template_name = 'users/artist_detail.html'
    context_object_name = 'user'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super(ArtistProfileView, self).get_context_data(**kwargs)
        artist = User.objects.get(username=context['object'].username)
        context['artist'] = artist

        return context


class UserProfileView(DetailView):
    model = User
    context_object_name = 'user'
    slug_field = 'username'
