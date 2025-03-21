from django.shortcuts import redirect

def unauthenticated_customer(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('customer_id'):
            return redirect('Index')
        return view_func(request, *args, **kwargs)
    return wrapper