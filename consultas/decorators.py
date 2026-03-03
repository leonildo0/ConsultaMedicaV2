from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def grupo_required(nome_grupo):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):

           
            if not request.user.is_authenticated:
                return redirect('login')

         
            if request.user.groups.filter(name=nome_grupo).exists():
                return view_func(request, *args, **kwargs)

            
            raise PermissionDenied

        return _wrapped_view
    return decorator