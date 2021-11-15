from django.conf import settings


def convert_to_decimal(amount):

    amount = amount / settings.TNBC_MULTIPLICATION_FACTOR
    rounded_amount = round(amount, 4)
    return rounded_amount


def convert_to_int(amount):

    return int(amount / settings.TNBC_MULTIPLICATION_FACTOR)
