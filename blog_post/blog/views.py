from .models import Post, Comment, Tag
from django.urls import reverse_lazy
from blog.form import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin

# Create your views here.
from django.views.generic.list import ListView

from django.views.generic import DetailView

# View for listing posts with pagination
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 5
    ordering = ["-id"]


# Create Post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    fields = ["title", "content", "tags"]
    template_name = "blog/add_post.html"

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author to the current user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})


# Update Post
class PostUpdateView(LoginRequiredMixin, UpdateView, UserPassesTestMixin):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # User can only update their own posts


# Delete Post
class PostDeleteView(LoginRequiredMixin, DeleteView, UserPassesTestMixin):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")  # Redirect to the post list after deleting

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Detail Post with Add Comment
class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()  # Include the comment form
        # Include the list of comments for the post
        context["comments"] = self.object.comments.order_by("-created_at")
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the Post object
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)
