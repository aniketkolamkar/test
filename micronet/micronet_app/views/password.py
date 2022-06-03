from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
import requests
import json
from django.contrib.sites.shortcuts import get_current_site
from ..tokens  import password_reset_token



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					url = "https://api.sendinblue.com/v3/smtp/email"

					payload = json.dumps({
                        "sender": {
                            "name": "6Simplex",
                            "email": "butler@6simplex.co.in"
                        },
                        "to": [
                            {
                            "email": request.POST.get('email')
                            }
                        ],
                        "subject": "Verification Link",
                        "textContent": render_to_string('commons/password-reset/password_reset_mail.html', {'user': user,'domain': get_current_site(request).domain,'uid': urlsafe_base64_encode(force_bytes(user.pk)),'token': password_reset_token.make_token(user),})
                        })
					headers = {
                            'accept': 'application/json',
                            'api-key': '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',
                            'content-type': 'application/json'
                        } 
					try:
						response = requests.request("POST", url, headers=headers, data=payload)
        
                            
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})