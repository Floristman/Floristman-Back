from collections import OrderedDict


def categoryFormat(data):
    return OrderedDict({
        "name": data.name,
        "img": data.img.url,
        "slug": data.slug,

    })


def subctgFormat(data):
    return OrderedDict({
        "name": data.name
    })


def productFormat(data):
    return OrderedDict({
        "sub_ctg": data.sub_ctg.id,
        "name": data.name,
        "img": data.img.url,
        "view": data.view,
        "price": data.price,
    })


def basketFormat(data):
    return OrderedDict({
        "product": data.product.name,
        "quentity": data.quantity,
        "price": data.price
    })
