import datetime
import random
import uuid

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from sayt.models import User, OTP


class LoginViev(GenericAPIView):

    def post(self, requests, *args, **kwargs):
        data = requests.data

        password = data.get("password")
        gmail = data.get("gmail")

        if not password or not gmail:
            return Response({
                "Error": "Malumot toliq kiritilmadi"
            })

        user = User.objects.filter(gmail=gmail).first()
        if not user:
            return Response({
                "Error": "Bumday foydalanuvch yoq"
            })

        if not user.check_password(password):
            return Response({
                "Error": "Parol notogri"
            })

        token = Token.objects.get_or_create(user=user)[0]
        return Response({
            'token': token.key
        })


class RegisView(GenericAPIView):

    def post(self, requests, *args, **kwargs):
        data = requests.data
        gmail = data.get("gmail")
        password = data.get("password")
        user = User.objects.filter(gmail=gmail).first()

        if user:
            return Response({
                "Error": "Bunday foydalanuvch bor"
            })

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save
        user.set_password(password)
        user.save()

        token = Token.objects.create(user=user)

        return Response({
            "token": token.key
        })


class StepOne(GenericAPIView):
    def post(self, requests, *args, **kwargs):
        data = requests.data

        if 'gmail' not in data:
            return Response({
                "Error": "Gmail raqam kiritilmadi"
            })

        parol = random.randint(100000, 999999)

        token = uuid.uuid4().__str__() + str(parol)

        otp_token = OTP.objects.create(
            key=token,
            gmail=data['gmail'],

        )

        return Response({
            "otp": parol,  # one time password
            "otp-token": otp_token.key
        })


class StepTwo(GenericAPIView):
    def post(self, requests, *args, **kwargs):
        data = requests.data

        if "parol" not in data or 'token' not in data:
            return Response({
                "Error": "malumot toliq emas"
            })

        if len(str(data["parol"])) != 6:
            return Response({
                "Error": "Xato parol"
            })

        token = OTP.objects.filter(key=data['token']).first()
        if not token:
            return Response({
                "Error": "Xato token"
            })

        if token.is_expired:

            return Response({
                "Error": "Eski token"
            })

        now = datetime.datetime.now(datetime.timezone.utc)
        cr = token.create_at

        if (now - cr).total_seconds() > 60:
            token.is_expired = True
            token.save()
            return Response({
                "Error": "Token eskirgan"
            })

        if token.key[-6] != str(data['parol']):
            token.tries += 1
            return Response({
                "Error": "Kod xato"
            })

        return Response({
            "result": "succes"
        })
