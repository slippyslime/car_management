from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Car
from .serializers import CarSerializer, CommentSerializer
from .forms import SignUpForm, CommentForm, CarForm

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def car_comments(request, car_id):
    car = Car.objects.get(id=car_id)

    if request.method == 'GET':
        comments = car.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        data['car'] = car.id

        serializer = CommentSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if car.owner != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот автомобиль.")

    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Автомобиль удален.')
        return redirect('/')

    return redirect('car_detail', car_id=car.id)


def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if car.owner != request.user:
        return HttpResponseForbidden("Вы не можете редактировать этот автомобиль.")

    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация об автомобиле обновлена.')
            return redirect('car_detail', car_id=car.id)
    else:
        form = CarForm(instance=car)

    return render(request, 'cars/edit_car.html', {'form': form, 'car': car})


@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            messages.success(request, 'Автомобиль успешно добавлен!')
            return redirect('/')
    else:
        form = CarForm()
    return render(request, 'cars/add_car.html', {'form': form})

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_list.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    comments = car.comments.all()
    form = None

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.car = car
                comment.author = request.user
                comment.save()
                messages.success(request, 'Комментарий успешно добавлен!')
                return redirect('car_detail', car_id=car.id)
        else:
            form = CommentForm()

    return render(request, 'cars/car_detail.html', {'car': car, 'comments': comments, 'form': form})


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny]

class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')
