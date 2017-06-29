from django.shortcuts import render, redirect

#---------------------------------作业代码（开始）-------------------------------
from website.models import UserProfile

# 登录认证使用django自带的登录模块和认证表单
from django.contrib.auth.models import User # 用于判断是否为注册用户
from django.contrib.auth import login # 用于注册用户的登录
from django.contrib.auth.forms import AuthenticationForm # 用户认证登录信息

#---------------------------------作业代码（结束）-------------------------------

def video_list(request):
    return render(request, 'mobile_list.html', {})

#---------------------------------作业代码（开始）-------------------------------
def user_list_panel_login(request):
    # 不允许登录用户访问，登录用户访问，自动跳转到当前页
    if request.user.is_authenticated:
        return redirect(to='user_list_panel')

    auth_error = ''

    if request.method == "GET":
        form = AuthenticationForm

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if User.objects.filter(username=request.POST["username"]).exists():
            user = User.objects.get(username=request.POST["username"])
            if user.is_superuser:
                if form.is_valid():
                    login(request, form.get_user())
                    return redirect(to="user_list_panel")
                else: auth_error = '您的用户名或密码错误'
            else: auth_error = '您不是超级管理员，无权管理用户'
        else: auth_error = '您尚未注册，请联系超级管理员'
    context = {}
    context['form'] = form
    context['auth_error'] = auth_error

    return render(request, 'userListPanelLogin.html', context)

def user_list_panel(request):
    # 不允许未登录的超级用户用户访问，未登录的超级用户用户访问，自动跳转到首页
    if request.user.is_authenticated:
        user = UserProfile.objects.get(belong_to=request.user)
        if user.belong_to.is_superuser:
            return render(request, 'userListPanel.html', {})

    return redirect(to='user_list_panel_login')

def user_detail(request, id):
    print('user detail! id = ' + id)
    # 不允许未登录的超级用户用户访问，未登录的超级用户用户访问，自动跳转到首页
    if request.user.is_authenticated:
        user = UserProfile.objects.get(belong_to=request.user)
        if user.belong_to.is_superuser:
            # 传过来也渲染不了，脚本可能不支持django模板语言
            return render(request, 'userDetail.html', {'user_id': id})

    return redirect(to='user_list_panel_login')

#---------------------------------作业代码（结束）-------------------------------
