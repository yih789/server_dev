from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LoginUser
from django.contrib.auth.hashers import make_password, check_password
from .serialize import LoginUserSerializer

# Create your views here.
class RegistUser(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(request.data)

        # 아이디에 한글, 특수문자 등이 포함되는 경우 불가능 표시 등등.. 더 추가
        user = LoginUser.objects.filter(user_id=serializer.data['user_id']).first()

        if user is not None:
            data = {
                'msg': '동일한 아이디가 있습니다.'
            }
            return Response(data)

        ''' serializer 사용 전 코드
        LoginUser.objects.create(user_id=user_id, user_pw=user_pw_encrypted, \
                                 birth_day=birth_day, gender=gender, email=email, name=name, age=age)
        '''
        user = serializer.create(request.data)

        data = LoginUserSerializer(user).data
        return Response(data)

class AppLogin(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        user_pw = request.data.get('user_pw')

        user = LoginUser.objects.filter(user_id=user_id).first()
        if user is None:
            data = { 'msg': '해당 사용자가 없습니다.' }
            return Response(data)

        if check_password(user_pw, user.user_pw):
            data = LoginUserSerializer(user).data
            return Response(data)
        else:
            data = {'msg': '비밀번호 틀림.'}
            return Response(data)