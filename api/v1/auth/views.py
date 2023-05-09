import datetime
import random
import uuid

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import Products, Likes
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
                "Error": "Bunday foydalanuvch yoq"
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
        user = User.objects.create_user(
            gmail=gmail,
            password=password
        )
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
        if token.key[-6:] != str(data['parol']):
            token.tries += 1
            return Response({
                "Error": "Kod xato"
            })

        return Response({
            "result": "succes"
        })


class LikeDislike(GenericAPIView):
    authentication_classes = TokenAuthentication,
    permission_classes = IsAuthenticated,

    def post(self, requests, *args, **kwargs):
        data = requests.data
        user = requests.data

        if ('like' not in data and 'dislike' not in data) or "product_id" not in data:
            return Response({"Error": 'malumot toliq emas'})

        pro = Products.objects.filter(pk=data['product-id']).first()
        if not pro:
            return Response({'Error': "bunday produk yoq"})

        likes = Likes.objects.get_or_create(product=pro, user=requests.user)[0]

        if 'like' in data and 'dislike' in data:
            return Response({"Error": 'Malumot xato'})

        like = likes.like
        dislike = likes.dislike

        if 'like' in data and data['like']:
            like = True
            dislike = False

        if 'dislike' in data and data['dislike']:
            like = False
            dislike = True

        likes.like = like
        likes.dislike = dislike
        likes.save()
        return Response({'succes'})
