from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import Products, Basket
from api.v1.base.format import basketFormat


class BasketView(GenericAPIView):
    authentication_classes = TokenAuthentication,
    permission_classes = IsAuthenticated,

    def post(self, requests, *args, **kwargs):
        data = requests.data

        if "product_id" not in data:
            return Response({
                "Error": "Product id berilmagan"
            })

        product = Products.objects.filter(pk=data["produvt_id"]).First

        if product:
            basket = Basket.objects.get_or_create(
                user=requests.user,
                product=product
            )[0]

            basket.quantity = data.get("quantity", 1)
            basket.save()

            return Response({"result":basketFormat(basket)})


        else:
            return Response({"Error":"Notogri product berilgan"})







