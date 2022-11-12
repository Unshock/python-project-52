from django.shortcuts import render
from django.views.generic import View
import os
import dotenv

dotenv.load_dotenv()


class MainPageView(View):
    creator = str(os.getenv('CREATOR', '%username%'))

    def get(self, request, *args, **kwargs):
        creator = str(os.getenv('CREATOR', '%username%'))
        return render(request, 'base.html', context={
            "who": creator
        })
