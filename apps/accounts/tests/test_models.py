import pytest
from django.db import IntegrityError

from apps.accounts.models import Business, Membership, User


@pytest.mark.django_db
def test_same_user_cannot_join_business_twice():
    user = User.objects.create_user(username="ricky", password="x")
    shop = Business.objects.create(name="Test Shop", kra_pin="P000000000A")
    Membership.objects.create(user=user, business=shop)

    with pytest.raises(IntegrityError):
        Membership.objects.create(user=user, business=shop)
