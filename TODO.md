## TODO: 12.06.2024

0. Refactor: Posts stored in Members
1. Research how chatterbot works
[Resource Chatterbot]:(https://chatterbot.readthedocs.io/en/stable/)
	Process flow: 
		Get input ([1,2,3] workout finished)
		Process input
			Questions: what is the highest confidence
					   value?
		Return response (string)

0. Installation

```sh
pip install chatterbot
```

3. Integration wisam_dev to main
4. Integration xtn_dev to main

## DRY!!!!

Save BMI in database [x]

## Admin Panel
	Register Profile and connect it to User

## Implement Argon2 [x]

Documentation:

[Resource: Django documentation](https://docs.djangoproject.com/en/5.0/topics/auth/passwords/)

```sh
# install argon2-cffi package
pip install argon2-cffi

# safe to requirements.txt
pip freeze > requirements.txt
```
Add to settings: 
PASSWORD_HASHERS = 
	["django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

## Implement OAuth
	Google
	
## Tests
	Write tests for views, functions etc..

## Integrate a ChatBot
	Research: 
		Chatter
		Google Bard
		ChatGPT
		Other

## Password Reset
	Force HTTPS
	Customize: registration/custom_password_reset_email.html
	nice to have: function based approach
	def password_reset_viev(request):
 	   token_generator = PasswordResetTokenGenerator()
  	   token = token_generator.make_token()

## Signup
	Handle Error messages
	finish cleaning functions
	Rename FitUserForm in forms.py

## Research
	APIs
	Django REST Framework
	Code:
	```python
	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
    	if created:
    	    Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
	    instance.profile.save()
	```

## Functionality
	Add a Stop workout button
	Add automatic generation of posts with LLM -> integrate ChatBot
	Add Footer: 
		Imprint
		Copyright
		About

## Style
	Add favicon

## Documentation
	Add docstrings
	HOWTO Blogposts
		LoginView
		LogoutView
		SignupForm
		PasswordReset 
		CustomUser
		using dotenv
		Deployment