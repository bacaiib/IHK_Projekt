from django.contrib.auth.models import User
from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from .models import LoginAttempt
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect

LOCKOUT_THRESHOLD = 3
LOCKOUT_DURATION = 30

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if not User.objects.filter(username=username).exists():
                messages.error(request, "Benutzer existiert nicht.")
                return render(request, 'login.html', {'form': self.get_form()})
            else:

                login_attempt, created = LoginAttempt.objects.get_or_create(
                    user__username=username,
                    defaults={'user': User.objects.get(username=username)} if User.objects.filter(username=username).exists() else {}
                )

            if user is not None:
                login_attempt.attempt_count = 0
                login_attempt.is_locked = False
                login_attempt.save()
                login(request, user)
                return redirect('index')
            else:
                if not login_attempt.user:
                    messages.error(request, "Benutzer existiert nicht.")
                    return render(request, 'login.html', {'form': self.get_form()})

                login_attempt.attempt_count += 1
                login_attempt.last_attempt_time = timezone.now()
                login_attempt.save()

                if login_attempt.attempt_count >= LOCKOUT_THRESHOLD:
                    login_attempt.is_locked = True
                    login_attempt.lock_time = timezone.now() + timedelta(seconds=LOCKOUT_DURATION)
                    login_attempt.save()
                    messages.error(request, "Zu viele fehlgeschlagene Versuche. Zugang für 3 Minuten gesperrt.")
                else:
                    messages.error(request, f"Falsche Anmeldedaten. Noch {LOCKOUT_THRESHOLD - login_attempt.attempt_count} Versuche übrig.")
                return render(request, 'login.html', {'form': self.get_form()})

        username = request.GET.get('username') or request.session.get('last_username')
        if username:
            login_attempt = LoginAttempt.objects.filter(user__username=username).first()
            if login_attempt and login_attempt.is_locked:
                remaining_time = (login_attempt.lock_time - timezone.now()).total_seconds()
                if remaining_time > 0:
                    messages.error(request, f"Zugang gesperrt. Warte {int(remaining_time)} Sekunden.")
                    return render(request, 'login.html', {'form': self.get_form()})

        return super().dispatch(request, *args, **kwargs)