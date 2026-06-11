import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from registry.models import Citizen


FIRST_NAMES = [
    "علی", "محمد", "رضا", "حسین", "امیر", "مهدی", "سارا", "زهرا", "فاطمه", "مریم",
    "نیما", "پارسا", "آرین", "سینا", "کیان", "نازنین", "الهام", "نگین", "بهنام", "کامران",
]

LAST_NAMES = [
    "احمدی", "محمدی", "رضایی", "حسینی", "کریمی", "موسوی", "جعفری", "نوری", "صادقی", "اکبری",
    "رحیمی", "قاسمی", "زارعی", "ملکی", "شریفی", "باقری", "فتحی", "امینی", "کاظمی", "یوسفی",
]

FATHER_NAMES = [
    "احمد", "محمد", "رضا", "حسین", "علی", "مهدی", "حسن", "جواد", "مجید", "سعید",
]

CITIES = [
    "تهران", "اصفهان", "شیراز", "مشهد", "تبریز", "کرج", "اهواز", "قم", "رشت", "یزد",
]


def random_birth_date():

    start = date(1950, 1, 1)
    end = date(2005, 12, 31)
    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


def random_national_code(used):

    while True:
        code = "".join(str(random.randint(0, 9)) for _ in range(10))
        if code not in used:
            used.add(code)
            return code


def random_phone(used):

    while True:
        phone = "+98912" + "".join(str(random.randint(0, 9)) for _ in range(7))
        if phone not in used:
            used.add(phone)
            return phone


class Command(BaseCommand):

    help = "ایجاد رکوردهای نمونه شهروند"

    def add_arguments(self, parser):

        parser.add_argument(
            "--count",
            type=int,
            default=100000,
            help="تعداد رکورد (پیش‌فرض: 100000)",
        )

    def handle(self, *args, **options):

        count = options["count"]
        batch_size = 2000
        used_codes = set(Citizen.objects.values_list("national_code", flat=True))
        used_phones = set(Citizen.objects.values_list("phone_number", flat=True))
        batch = []
        created = 0

        self.stdout.write(f"Creating {count} records...")

        for i in range(count):

            city = random.choice(CITIES)
            batch.append(Citizen(
                first_name=random.choice(FIRST_NAMES),
                last_name=random.choice(LAST_NAMES),
                national_code=random_national_code(used_codes),
                phone_number=random_phone(used_phones),
                father_name=random.choice(FATHER_NAMES),
                birth_date=random_birth_date(),
                address=f"{city}، خیابان {random.randint(1, 200)}، پلاک {random.randint(1, 500)}",
            ))

            if len(batch) >= batch_size:
                Citizen.objects.bulk_create(batch)
                created += len(batch)
                batch = []
                self.stdout.write(f"{created} records created...")

        if batch:
            Citizen.objects.bulk_create(batch)
            created += len(batch)

        self.stdout.write(self.style.SUCCESS(f"Done. Total: {created} records"))
