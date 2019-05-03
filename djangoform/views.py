from django.shortcuts import render
from djangoform.models import Recipes, Author
from djangoform.forms import AuthorForm, RecipeForm
from django.contrib.auth.models import User


def list_view(request):
    html = 'list_view.html'
    items = Recipes.objects.all().order_by('title')
    return render(request, html, {'list': items})


def create_recipe(request):
    html = "create_recipe.html"
    form = None
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipes.objects.create(
                title=data["title"],
                author=data["author"],
                description=data["description"],
                time=data["time"],
                instructions=data["instructions"],
            )
        return render(request, "created_recipe.html")
    else:
        form = RecipeForm()
    return render(request, html, {"form": form})


def recipe_info(request, id):
    html = 'recipe_info.html'
    items = Recipes.objects.all().filter(id=id)
    instructions = items[0].instructions.split('\n')
    return render(request, html,
                  {'recipes': items, 'instructions': instructions})


def create_author(request):
    html = "create_author.html"
    form = None
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create(username=data["name"])
            Author.objects.create(
                name=data["name"],
                bio=data["bio"],
                user=user
            )
        return render(request, "created_author.html")
    else:
        form = AuthorForm()
    return render(request, html, {"form": form})


def author_info(request, id):
    html = 'author_info.html'
    authors = Author.objects.all().filter(id=id)
    items = Recipes.objects.all().filter(author_id=id)
    return render(request, html, {'authors': authors, 'recipes': items})
