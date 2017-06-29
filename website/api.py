from website.models import Video

#---------------------------------作业代码（开始）-------------------------------
from website.models import UserProfile
from website.form import ProfileForm

# 登录认证使用django自带的登录模块和认证表单
from django.contrib.auth.models import User # 用于判断是否为注册用户
from django.contrib.auth import login # 用于注册用户的登录
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # 用户认证登录信息

import random

#---------------------------------作业代码（结束）-------------------------------

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication


class VideoSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=1)

    class Meta:
        model = Video
        fields = '__all__'
        depth = 1

#---------------------------------作业代码（开始）-------------------------------
#开始：定义数据序列化器
class UserSerializer(serializers.ModelSerializer):
    #开始：向数据模型的字段绑定校验器

    #结束：向数据模型的字段绑定校验器

    #开始：绑定数据模型及其字段
    class Meta:
        model = UserProfile
        fields = '__all__'
        depth = 1

    #结束：绑定数据模型及其字段

#结束：定义数据序列化器

@api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
def userlist(request):
    user_list = UserProfile.objects.order_by('-id')

    if request.method == 'GET': #注：到这里已经能成功访问../api/userlist/
        #开始：对data进行序列化，返回序列化后的对象
        serializer = UserSerializer(user_list, many=True)

        #结束：对data进行序列化，返回序列化后的对象

        #开始：对序列化后的对象进行处理（校验，加工，返回等）
        return Response(serializer.data)

        #结束：对序列化后的对象进行处理

    if request.method == 'POST':
        print('new a user here!')
        form = UserCreationForm(request.data)
        print(request.data)
        print(form.errors)
        if form.is_valid(): #注意：is_valid()已经包含了密码校验
            form.save()
            #注意：UserCreationForm has not attribute 'email' and ' ... '
            #     它只存了 username 和 password
            user = User.objects.get(username=request.data['username'])
            user.email = request.data['email']
            user.profile.is_InvitedAuthor = True if request.data['is_InvitedAuthor'] == 'true' else False
            user.profile.profile_image = '/profile_image/' + str(random.sample(range(1,24),1)[0]) +'.png'
            user.save()
            print('successfully new a user here!')
            return Response(None)
        else: return Response('密码还是太简单了', status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
# @authentication_classes((TokenAuthentication,))
def userlist_operation(request, id):
    print('id=' + id)
    # 注意：用Userprofile 而不是 User！因为User没有is_InvitedAuthor属性
    user = UserProfile.objects.get(id=id)
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        # 注意：不要用user = User.objects.get(id=id)
        # 因为 User 的 id 和 UserProfile 的 id 不一样
        user = User.objects.get(id=user.belong_to.id)
        user.delete()
        return Response({'msg': 'A-OK'}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT'])
# @authentication_classes((TokenAuthentication,))
def userdetail(request, id):
    user = UserProfile.objects.get(id=id)
    print('here getting user detail!')

    if request.method == 'GET': #注：到这里已经能成功访问../api/userlist/
        print('here got user detail!')
        #开始：对data进行序列化，返回序列化后的对象
        serializer = UserSerializer(user)

        #结束：对data进行序列化，返回序列化后的对象

        #开始：对序列化后的对象进行处理（校验，加工，返回等）
        return Response(serializer.data)

        #结束：对序列化后的对象进行处理

    if request.method == 'PUT':
        print("here putting user detail!")

        form = ProfileForm(request.data)

        user = User.objects.get(id=user.belong_to.id)

        if request.data['username'] != '':
            print('here put username!')
            # 如果用户有填入“真实姓名”信息，则存入
            user.username = request.data['username']
            user.save()

        if request.data['password'] != '':
            if form.is_valid():
                print('here put password')
                # 如果用户有填入“密码”信息，则存入
                user.password = request.data['password']
                user.save()
            else:
                print('PUT BAD REQUEST!')
                return Response('密码还是太简单了', status=status.HTTP_400_BAD_REQUEST)

        return Response(None)

    return Response(None)

#---------------------------------作业代码（结束）-------------------------------

@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def video(request):
    print(request.user)
    print(request.auth)
    video_list = Video.objects.order_by('-id')
    if request.method == 'GET':
        if request.auth:
            serializer = VideoSerializer(video_list, many=True)
            return Response(serializer.data)
        else:
            serializer = VideoSerializer(video_list[:5], many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        body = {
            'body': serializer.errors,
            'msg': '40001'
        }
        return Response(body, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@authentication_classes((TokenAuthentication,))
def video_card(request, id):
    video_card = Video.objects.get(id=id)
    USER_CAN = {
        "DELETE": request.user.profile == video_card.owner or (
                    request.user == 'admin')
    }
    if request.method == 'PUT':
        serializer = VideoSerializer(video_card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if USER_CAN["DELETE"]:
            video_card.delete()
            return Response({'msg': 'A-OK'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'You cant touch this'}, status=status.HTTP_403_FORBIDDEN)
