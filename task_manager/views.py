from django.shortcuts import render
import os
import dotenv

dotenv.load_dotenv()


def index(request, status=None):
    creator = str(os.getenv('CREATOR', '%username%'))
    return render(request, 'base.html', context={
        "who": creator,
        "status": status,
    })
