from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import UserRegisterForm, ProfileUpdateForm
from .models import Profile


def register(request):
    """Регистрация нового пользователя с обработкой ошибок"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Безопасное создание профиля
                Profile.objects.get_or_create(user=user)

                username = form.cleaned_data.get('username')
                messages.success(
                    request,
                    f'✅ Аккаунт {username} успешно создан! Теперь вы можете войти.'
                )
                return redirect('login')

            except IntegrityError:
                messages.warning(
                    request,
                    '⚠️ Профиль для этого пользователя уже существует'
                )
                return redirect('login')

            except Exception as e:
                messages.error(
                    request,
                    '❌ Произошла ошибка при создании профиля'
                )
                logger.error(f"Registration error: {str(e)}")
                return redirect('register')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Обновление профиля пользователя"""
    try:
        if request.method == 'POST':
            profile_form = ProfileUpdateForm(
                request.POST,
                request.FILES,  # Для обработки загружаемых изображений
                instance=request.user.profile
            )
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, '✅ Ваш профиль успешно обновлен!')
                return redirect('profile')
        else:
            profile_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'profile_form': profile_form,
            'user_listings': request.user.listings.all()  # Предполагается, что есть related_name='listings'
        }
        return render(request, 'users/profile.html', context)

    except Exception as e:
        messages.error(request, '❌ Ошибка при загрузке профиля')
        logger.error(f"Profile view error: {str(e)}")
        return redirect('home')
        return redirect('home')