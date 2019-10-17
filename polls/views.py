from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from polls.Serializer import QuestionSerializer, UserSerializer
from .models import Question, Choice
from rest_framework.views import exception_handler


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data
        response.data = {}
        errors = []
        for field, value in data.items():
            errors.append("{} : {}".format(field, " ".join(value)))

        response.data['code'] = status.HTTP_401_UNAUTHORIZED
        response.data['status'] = False
        response.data['data'] = None

        response.data['message'] = str(exc)

    return response



def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class questionList(APIView):

    def get(self, request):
        book1 = Question.objects.all()
        serializer = QuestionSerializer(book1, many=True)
        return Response({'message':'Successfully data save ',"status": True,'code':status.HTTP_200_OK,'data':serializer.data}, status = status.HTTP_200_OK)  # Return JSON

class addQuestion(APIView):

        def post(self, request):
            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Successfully data save ',"status": True,'code':'201','data':serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class login(APIView):

        permission_classes = [AllowAny]

        def post(self, request):

            username = request.data.get("username")
            password = request.data.get("password")
            if username is None or password is None:
                return Response({'error': 'Please provide both username and password'},
                                status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(username=username, password=password)
            if not user:
                return Response({'error': 'Invalid Credentials'},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user)

            token, _ = Token.objects.get_or_create(user=user)
            return Response({'message':'Successfully login',"status": True,'code':status.HTTP_200_OK,'token': token.key, 'data': serializer.data},
                            status=status.HTTP_200_OK)


class registration(APIView):

                permission_classes = [AllowAny]

                def post(self, request):
                    username = request.data.get("username")
                    if User.objects.filter(username=username).exists() and User.objects.filter(email=request.data.get("email")).exists() :

                        return Response({'message': 'This user already in database ', "status": False, 'code': '400',
                                         'data': None}, status=status.HTTP_400_BAD_REQUEST)

                    serializer = UserSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'message': 'Successfully user create ', "status": True, 'code': '201',
                                         'data': serializer.data}, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


