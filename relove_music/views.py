from django.shortcuts import render


def handler404(request, exception):
    """ view for rendering custom error 404 page for non-existant urls """
    return render(request, 'errors/404.html', status=404)
