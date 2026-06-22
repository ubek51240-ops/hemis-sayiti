"""
Eski qo'shilgan talabalar uchun User, Profile va Application yaratish hamda
status sinxronizatsiyasini ta'minlash uchun management command.

Foydalanish:
    python manage.py sync_students
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Student, Profile, Application


class Command(BaseCommand):
    help = "Eski talabalar uchun User+Profile+Application yaratish va status sinxronizatsiyasi"

    def handle(self, *args, **options):
        created_users = 0
        created_apps = 0
        synced_apps = 0
        skipped = 0

        students = Student.objects.all()
        total = students.count()
        self.stdout.write(f"Topilgan talabalar: {total}")

        for student in students:
            if not student.passport:
                skipped += 1
                continue

            passport = student.passport.strip().upper()

            # 1) User yaratish (login=parol=pasport)
            user = User.objects.filter(username=passport).first()
            if not user:
                try:
                    user = User.objects.create_user(
                        username=passport,
                        password=passport,
                        first_name=student.full_name or '',
                        email=(student.phone or '') + '@temp.local'
                    )
                    created_users += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"  + User yaratildi: {passport} ({student.full_name})"
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"  ! User yaratishda xato {passport}: {e}"
                    ))
                    skipped += 1
                    continue

            # 2) Profile yaratish/yangilash
            profile, p_created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'student',
                    'roles': ['student'],
                    'jshshir': student.jshshir or '',
                    'phone': student.phone or '',
                    'email': user.email,
                }
            )
            if not p_created:
                # Mavjud profile - student rolini qo'shish (boshqa rollar saqlanadi)
                if profile.role not in ['student', 'super_admin', 'admin']:
                    profile.role = 'student'
                roles = profile.roles or []
                if 'student' not in roles:
                    roles.append('student')
                    profile.roles = roles
                if not profile.jshshir and student.jshshir:
                    profile.jshshir = student.jshshir
                if not profile.phone and student.phone:
                    profile.phone = student.phone
                profile.save()

            # 3) Application yaratish/sinxronlash
            app = Application.objects.filter(passport=passport).first()
            if not app:
                Application.objects.create(
                    user=user,
                    full_name=student.full_name,
                    passport=passport,
                    email=user.email,
                    phone=student.phone or '',
                    faculty=student.faculty,
                    specialty=student.specialty,
                    status=student.status,
                    comment=student.comment or '',
                )
                created_apps += 1
                self.stdout.write(self.style.SUCCESS(
                    f"    + Application yaratildi: {passport} status={student.status}"
                ))
            else:
                # Mavjud application status sinxronlash
                changed = False
                if app.status != student.status:
                    app.status = student.status
                    changed = True
                if app.user_id != user.id:
                    app.user = user
                    changed = True
                if student.faculty and app.faculty_id != student.faculty_id:
                    app.faculty = student.faculty
                    changed = True
                if student.specialty and app.specialty_id != student.specialty_id:
                    app.specialty = student.specialty
                    changed = True
                if changed:
                    app.save()
                    synced_apps += 1
                    self.stdout.write(
                        f"    ~ Application sinxronlandi: {passport} -> status={student.status}"
                    )

        # ============================================================
        # 4) Eski Application lardan Student yaratish (o'zi ro'yxatdan
        #    o'tgan, lekin Student modelida hali bo'lmaganlar uchun)
        # ============================================================
        created_students = 0
        existing_passports = set(Student.objects.values_list('passport', flat=True))

        # Faqat talaba arizalari (faculty/specialty mavjud, employee emas)
        self_apps = Application.objects.exclude(passport='') \
            .filter(faculty__isnull=False, specialty__isnull=False)

        for app in self_apps:
            passport = (app.passport or '').strip().upper()
            if not passport or passport in existing_passports:
                continue

            # Profile dan JSHSHIR olish
            jshshir = ''
            if app.user_id and hasattr(app.user, 'profile'):
                jshshir = getattr(app.user.profile, 'jshshir', '') or ''

            # Agar JSHSHIR mavjud bo'lsa va boshqa Student da bo'lsa - skip
            if jshshir and Student.objects.filter(jshshir=jshshir).exists():
                continue

            try:
                Student.objects.create(
                    passport=passport,
                    jshshir=jshshir or f'00000000000{app.id:03d}'[-14:],
                    full_name=app.full_name,
                    course=1,
                    phone=app.phone or '',
                    faculty=app.faculty,
                    specialty=app.specialty,
                    status=app.status,
                    created_by=None,  # O'zi ro'yxatdan o'tgan
                )
                created_students += 1
                existing_passports.add(passport)
                self.stdout.write(self.style.SUCCESS(
                    f"  + Student yaratildi (o'zi ro'yxatdan): {passport} ({app.full_name})"
                ))
            except Exception as e:
                self.stdout.write(self.style.WARNING(
                    f"  ! Student yaratib bo'lmadi {passport}: {e}"
                ))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS(
            f"YAKUN:\n"
            f"  Yangi User-lar:                    {created_users}\n"
            f"  Yangi Application-lar:             {created_apps}\n"
            f"  Sinxronlangan Application:         {synced_apps}\n"
            f"  Yangi Student (o'zi ro'yxatdan):   {created_students}\n"
            f"  O'tkazib yuborilgan:               {skipped}\n"
            f"  Jami talabalar:                    {total}"
        ))
        self.stdout.write(self.style.SUCCESS("=" * 60))
