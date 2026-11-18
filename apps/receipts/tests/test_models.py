import pytest
from django.db import IntegrityError

from apps.accounts.models import Business
from apps.receipts.models import Receipt


@pytest.mark.django_db
def test_same_invoice_twice_for_one_business_is_rejected():
    shop = Business.objects.create(name="Test Shop", kra_pin="P000000000A")
    Receipt.objects.create(business=shop, invoice_number="INV001")

    with pytest.raises(IntegrityError):
        Receipt.objects.create(business=shop, invoice_number="INV001")


@pytest.mark.django_db
def test_same_invoice_for_different_businesses_is_allowed():
    shop_a = Business.objects.create(name="Elvaso", kra_pin="P000000004A")
    shop_b = Business.objects.create(name="LockApoint", kra_pin="P000000005A")
    Receipt.objects.create(business=shop_a, invoice_number="INV001")
    Receipt.objects.create(business=shop_b, invoice_number="INV001")

    assert Receipt.objects.count() == 2


@pytest.mark.django_db
def test_blank_invoice_numbers_are_allowed_twice():
    shop_c = Business.objects.create(name="Test", kra_pin="P00000000BA")
    Receipt.objects.create(business=shop_c, invoice_number="")
    Receipt.objects.create(business=shop_c, invoice_number="")

    assert Receipt.objects.count() == 2
