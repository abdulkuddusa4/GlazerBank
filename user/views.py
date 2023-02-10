from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from user.models import Profile
from user.forms import UserRegistrationForm, ProfileCreationForm, LoginForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages


class Registration(View):
	def get(self, request):
		form = UserRegistrationForm
		form.heading = 'Registration Form'
		context = {
			'form': form,
		}
		return render(request, 'registration_form.html', context)

	def post(self, request):

		form = UserRegistrationForm(request.POST)
		form.heading = "Additional Information"
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			print(username)
			print(password)
			user = authenticate(username=username, password=password)
			if user:
				login(request,user)
			return redirect('user-profile-create')
		else:
			return render(request, 'registration_form.html', {'form': form})


class CreateProfile(View):

	def get(self, request):
		profile = Profile.objects.get(user_account_id=request.user.id)
		form = ProfileCreationForm(instance=profile)
		form.heading = "Lets Complete Your Profile"
		return render(request, 'registration_form.html', {'form': form})

	def post(self, request):
		print(request.FILES)
		profile = Profile.objects.get(user_account_id=request.user.id)
		form = ProfileCreationForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			form.save()
			return redirect('home-view')

		return render(request, 'registration_form.html', {'form': form})


	@classmethod
	def as_view(cls):
		return login_required(super().as_view())


class UserLogin(View):
	def get(self, request):
		form = LoginForm()
		return render(request, 'index.html', {'form': form})

	def post(self, request):
		form = LoginForm(request.POST)
		next = request.GET.get('next')
		if form.is_valid():
			user = authenticate(
				username=form.cleaned_data.get('username'),
				password=form.cleaned_data.get('password')
			)
			if user:
				login(request, user=user)
				if next:
					return redirect(next)
				return redirect('home-view')
			messages.error(request, "Invalid username or password :(", extra_tags='danger')
			return render(request, 'index.html', {'form': form})
		return HttpResponse("sfs")


class UserProfile(View):
	def get(self, request):
		edit = request.GET.get('edit')
		form = UserRegistrationForm(instance=request.user)
		profile_form = ProfileCreationForm(instance=request.user.profile)
		context = {
			'EDIT':True,
			'form': form,
			'profile_form': profile_form,
		}
		if edit:
			return render(request, 'user_profile.html', context)
		return render(request, 'user_profile.html')

	def post(self, request):
		form = UserRegistrationForm(request.POST, request.FILES, instance=request.user)
		profile_form = ProfileCreationForm(request.POST, request.FILES, instance=request.user.profile)
		context = {
			'form': form,
			'profile_form': profile_form,
		}
		if form.is_valid() and profile_form.is_valid():
			form.save()
			profile_form.save()
			messages.success(request, 'profile updated succesfully', extra_tags='profile_update_msg')
			return redirect('user-profile')
		else:
			context['EDIT'] = True
			return render(request, 'user_profile.html', context)

	@classmethod
	def as_view(cls, **initkwargs):
		return login_required(super().as_view())


def user_logout(request):
	if request.user.is_authenticated:
		logout(request)
		next = request.GET.get('next')
		if not next:
			next = 'home-view'
		return redirect(next)
	else:
		url = reverse('user-login')
		return redirect(url+'?next=home-view')

