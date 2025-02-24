from datetime import datetime

from models.Event import Event
from models.Notification import Notification
from models.NotificationEvent import NotificationEvent
from models.Place import Place
from models.User import User
from mixer.backend.peewee import mixer
from utils.database import db

from models.Subscription import Subscription
from crons.notifier import notify
from utils.email import EmailUtils
from pytest_mock import MockerFixture
import pytest
import faker

faker = faker.Faker()


@pytest.mark.integration
def test_send_notification_email(mocker: MockerFixture):
    spy = mocker.spy(EmailUtils, "send_email")
    place = mixer.blend(Place)
    another_place = mixer.blend(Place)
    user = mixer.blend(User)
    another_user = mixer.blend(User)
    subscription = mixer.blend(Subscription, place=place, user=user, is_active=True)

    with db.atomic():
        Event.bulk_create(
            [
                Event(
                    location="asdasd",
                    price=1.1,
                    url="",
                    image_url="",
                    date=datetime.now().date(),
                    place=place,
                    stillPlacesLeft=True,
                    id=1,
                    name=faker.name(),
                ),
                Event(
                    location="asdasd",
                    price=1.1,
                    url="",
                    image_url="",
                    date=datetime.now().date(),
                    place=place,
                    stillPlacesLeft=True,
                    id=2,
                    name=faker.name(),
                ),
                Event(
                    location="asdasd",
                    price=1.1,
                    url="",
                    image_url="",
                    date=datetime(2022, 1, 1).date(),
                    place=place,
                    stillPlacesLeft=True,
                    id=3,
                    name=faker.name(),
                ),
                Event(
                    location="asdasd",
                    price=1.1,
                    url="",
                    image_url="",
                    date=datetime.now().date(),
                    place=place,
                    stillPlacesLeft=False,
                    id=4,
                    name=faker.name(),
                ),
                Event(
                    location="asdasd",
                    price=1.1,
                    url="",
                    image_url="",
                    date=datetime.now().date(),
                    place=another_place,
                    stillPlacesLeft=True,
                    id=5,
                    name=faker.name(),
                ),
            ]
        )

    notify()

    assert spy.call_count == 1
    calls = spy.call_args
    assert calls.args[1] == [user.email]
    assert len(calls.args[2]) == 2
    assert calls.args[2][0].id == 1
    assert calls.args[2][1].id == 2

    notifications = list(
        Notification.select().where(Notification.user == user).execute()
    )

    assert len(notifications) == 1
    assert notifications[0].user == user

    notification_events = NotificationEvent.select().where(
        NotificationEvent.notification == notifications[0]
    )
    assert len(notification_events) == 2
    assert notification_events[0].event == Event.get_by_id(1)
    assert notification_events[1].event == Event.get_by_id(2)
