from django.shortcuts import render
import markdown2
import random
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

# Home page


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Find and display an entry page


def entry(request, name):
    # First, get all the articles
    entries = util.list_entries()
    # Get the spesific queried article
    article = util.get_entry(name)
    # Check if the queried article is in articles
    if name in entries:
        # Convert to Markdown
        mdPage = markdown2.markdown(article)
        return render(request, "encyclopedia/entry.html", {
            "page": mdPage,
            "title": name
        })
    else:
        # It's not in entries
        return render(request, "encyclopedia/error.html", {
            "message": "Page does not exist"
        })

# Search for an entry


def search(request):
    # Get the request from the text input in the form
    query = request.POST["q"]
    entries = util.list_entries()

    # Check if the query is in entries
    if query in entries:
        return HttpResponseRedirect(reverse("entry", kwargs={"entry": query}))
    else:
        newList = []
        for entry in entries:
            if query.lower() in entry.lower():
                newList.append(entry)

        return render(request, "encyclopedia/search-results.html", {
            "newList": newList
        })

# Create new page


def newPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new-page.html")

    if request.method == "POST":
        # Get the page title and info
        pageTitle = request.POST["pageTitle"]
        pageInfo = request.POST["pageInfo"]

        # Get all entries to check if the page already exists
        entries = util.list_entries()
        if pageTitle in entries:
            return render(request, "encyclopedia/error.html", {
                "message": "Page already exists"})

        # If we got here - the page does not yet exist
        util.save_entry(pageTitle, pageInfo)

        return HttpResponseRedirect(reverse("entry", kwargs={"name": pageTitle}))

# Edit an existing page


def edit(request, entry):
    if request.method == "GET":
        # We need to get the page to send to the edit page
        content = util.get_entry(entry)
        return render(request, "encyclopedia/edit-page.html", {
            "title": entry,
            "content": content
        })

    # Update page
    if request.method == "POST":
        updatedTitle = request.POST["pageTitle"]
        updatedInfo = request.POST["pageInfo"]
        util.save_entry(updatedTitle, updatedInfo)
        print(updatedTitle)
        return HttpResponseRedirect(reverse("entry", kwargs={"name": updatedTitle}))


# Get a random page
def randomPage(request):
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", kwargs={"name": entry}))
