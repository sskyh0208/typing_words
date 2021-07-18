from botocore.exceptions import ClientError
from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from .forms import PasswordResetForm, RegistForm
from .models import PasswordRestToken, Users
import os
import boto3


class HomeView(TemplateView):
    template_name = os.path.join('accounts', 'home.html')


class PasswordResetView(FormView):
    template_name = os.path.join('accounts', 'password_reset.html')
    form_class = PasswordResetForm
    success_url = reverse_lazy('accounts:regist_complete')

    def get(self, request, *args, **kwargs):
        # トークンの存在しないアドレスの場合、Englishのホームへリダイレクト
        user = PasswordRestToken.objects.get_user(kwargs.get('token'))
        if user:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('english:home')

    def form_valid(self, form):
        token = self.kwargs.get('token')
        if form.is_valid():
            user = form.save(token)
            # 登録完了後トークン削除
            PasswordRestToken.objects.filter(token=token).delete()
            # 登録完了通知メール送信
            send_register_email(user)
        return super().form_valid(form)


class RegistComplete(TemplateView):
    template_name = os.path.join('accounts', 'regist_complete.html')


def user_login(request):
    if request.method == 'POST':
        if request.is_ajax:
            username = request.POST.get('login-username')
            password = request.POST.get('login-password')
            user = authenticate(request, username=username, password=password)
            
            if user and user.is_active:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'ユーザ名またはパスワードが正しくありません'})

    return redirect('english:home')

def user_regist(request):
    if request.method == 'POST':
        if request.is_ajax:
            user = Users.objects.filter(email=request.POST.get('email')).first()
            if user:
                # 既にメールアドレスが登録されている
                return JsonResponse({'success': False, 'message': ['入力されたメールアドレスは既に存在します']})
            else:
                form = RegistForm(request.POST)
                if form.is_valid():
                    try:
                        # 新規ユーザ作成
                        new_user = form.save()
                        token = PasswordRestToken.objects.publish_token(new_user)
                        # print(f'http://127.0.0.1:8000/accounts/password_reset/{token}')
                        # 仮登録メール送信
                        send_tmp_register_email(new_user, token)
                        return JsonResponse({'success': True, 'message': ['メールアドレスに送信されたメッセージより', '本登録を完了させてください。']})
                    except ValidationError as e:
                        # エラー内容を配列で渡す
                        return JsonResponse({'success': False, 'message': e.messages})
                else:
                    # ValidationErrorを配列で渡す
                    error_msgs = []
                    for error in form.errors.as_data().values():
                        for e in error:
                            error_msgs += e.messages
                    return JsonResponse({'success': False, 'message': error_msgs})

    return redirect('english:home')

def send_tmp_register_email(user, access_token):
    to_address = user.email
    subject = '【TYPING】仮登録完了通知'
    msg = (
        '※このメールはシステムからの自動返信です\r\n'
        f'{user.username}様\r\n'
        '24時間以内に以下のURLより本登録を完了させてください。\r\n'
        # f'http://127.0.0.1:8000/accounts/password_reset/{access_token}'
        f'http://typing-words.eba-sw6vqj27.ap-northeast-1.elasticbeanstalk.com/accounts/password_reset/{access_token}'

    )
    send_email(to_address, subject, msg)

def send_register_email(user):
    to_address = user.email
    subject = '【TYPING】本登録完了通知'
    msg = (
        '※このメールはシステムからの自動返信です\r\n'
        f'{user.username}様\r\n'
        '本登録が完了いたしました。\r\n'
        '引き続き、下記URLよりサービスをお楽しみください。\r\n'
        '\r\n'
        f'http://typing-words.eba-sw6vqj27.ap-northeast-1.elasticbeanstalk.com/'
    )
    send_email(to_address, subject, msg)
    
def send_email(to_address, subject, msg):
    SENDER = 'sskyh0208@gmail.com'
    CHARSET = 'UTF-8'
    client = boto3.client('ses', region_name='ap-northeast-1')
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [to_address]
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': msg
                    }
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject
                }
            },
            Source=SENDER
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        raise
    else:
        print(f'Email sent! Message ID: {response["MessageId"]}')