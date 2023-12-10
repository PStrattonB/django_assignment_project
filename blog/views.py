# blog/views.py

from django.shortcuts import render
from . import models, forms
from django.views.generic import DetailView, FormView, ListView, CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.


class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # get parent context
        context = super().get_context_data(**kwargs)

        latest_posts = models.Post.objects.published() \
            .order_by('-published')[:3]

        # update the context with our context variables
        context.update({
            'latest_posts': latest_posts
        })

        return context


class AboutView(TemplateView):
    template_name = 'blog/about.html'


def terms_and_conditions(request):
    return render(request, 'blog/terms_and_conditions.html')


class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')  # Customized queryset


class TopicListView(ListView):
    model = models.Topic
    context_object_name = 'topics'
    queryset = models.Topic.objects.order_by('name')


class PostDetailView(DetailView):
    model = models.Post

    def get_queryset(self):
        # Get base queryset
        queryset = super().get_queryset().published()

        # if this is a 'pk' lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )


class TopicDetailView(DetailView):
    model = models.Topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.get_object()

        posts = topic.blog_posts.filter(status='published').order_by('-published')

        context.update({
            'posts': posts
        })
        return context


def form_example(request):
    # Handle the POST
    if request.method == 'POST':
        # Pass the POST data in to a new form instance for validation
        form = forms.ExampleSignupForm(request.POST)

        # If the form is valid, return different template
        if form.is_valid():
            # form.cleaned_data is a dict with valid form data
            cleaned_data = form.cleaned_data

            return render(
                request,
                'blog/form_example_success.html',
                context={'data': cleaned_data}
            )

    # If not a POST, return a blank form
    else:
        form = forms.ExampleSignupForm()

    # Return if either an invalid POST or a GET
    return render(request, 'blog/form_example.html', context={'form': form})


class FormViewExample(FormView):
    template_name = 'blog/form_example.html'
    form_class = forms.ExampleSignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Create a "success" message
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you for signing up!'
        )
        # Continue with default behaviour
        return super().form_valid(form)


class ContactFormView(CreateView):
    model = models.Contact
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'message',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you very much! Your message has been sent to the appropriate party'
        )
        return super().form_valid(form)


class PhotoContestView(CreateView):
    template_name = 'blog/photo_contest_form.html'
    model = models.PhotoContestSubmission
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'photo_contest_entry',
    ]

    def form_valid(self, form):
        form.fields['photo_contest_entry'].required = True
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your photo contest submission has been received. Good luck!'
        )
        return super().form_valid(form)
