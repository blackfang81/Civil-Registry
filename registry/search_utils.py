from django.db.models import Q


def build_query_filter(q):

    q = q.strip()

    if q.startswith("+") or (q.isdigit() and len(q) >= 4):

        if q.startswith("+"):
            phone = q
            digits = q[1:]
        else:
            digits = q
            phone = "+98" + q

        if not digits.isdigit():
            return None, "فرمت شماره تلفن نامعتبر است"

        if not phone.startswith("+98"):
            phone = "+98" + digits

        rest = phone[3:]
        if len(rest) < 7:
            return None, "برای جستجوی تلفن حداقل ۷ رقم وارد کنید"

        return Q(phone_number__startswith=phone), None

    if q.isdigit():

        if len(q) == 10:
            return Q(national_code=q), None

        if len(q) < 5:
            return None, "برای جستجوی کد ملی حداقل ۵ رقم وارد کنید"

        return Q(national_code__startswith=q), None

    return (
        Q(first_name__icontains=q)
        | Q(last_name__icontains=q)
        | Q(father_name__icontains=q),
        None,
    )
