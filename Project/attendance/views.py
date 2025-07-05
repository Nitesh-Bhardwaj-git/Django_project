from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Student, Subject, Attendance
from django.http import HttpResponse
from django.db.models import Count, Q
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
import base64
import csv
from .import views


# Create your views here.


def mark_attendance(request):
    students = Student.objects.all()
    subjects = Subject.objects.all()
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')
        subject = Subject.objects.get(id=subject_id)
        for student in students:
            present = request.POST.get(f'present_{student.id}') == 'on'
            late = request.POST.get(f'late_{student.id}') == 'on'
            if present:
                Attendance.objects.create(
                    student=student,
                    subject=subject,
                    date=date,
                    time_marked=timezone.now().time(),
                    is_late=late
                )
        return redirect('attendance_success')
    return render(request, 'attendance/mark_attendance.html', {'students': students, 'subjects': subjects})


def attendance_success(request):
    return HttpResponse("Attendance marked successfully!")


def home(request):
    return render(request, 'attendance/home.html')


def student_analytics(request):
    students = Student.objects.all()
    selected_student = None
    attendance_summary = []
    most_attended = None
    most_late = None

    if request.method == 'POST':
        student_id = request.POST.get('student')
        selected_student = Student.objects.get(id=student_id)
        # Attendance per subject
        attendance_summary = (
            Attendance.objects
            .filter(student=selected_student)
            .values('subject__name')
            .annotate(
                total=Count('id'),
                late_count=Count('id', filter=Q(is_late=True))
            )
            .order_by('-total')
        )
        if attendance_summary:
            most_attended = attendance_summary[0]['subject__name']
            most_late = max(attendance_summary, key=lambda x: x['late_count'])['subject__name']

    return render(request, 'attendance/student_analytics.html', {
        'students': students,
        'selected_student': selected_student,
        'attendance_summary': attendance_summary,
        'most_attended': most_attended,
        'most_late': most_late,
    })


def student_qrcodes(request):
    students = Student.objects.all()
    qrcodes = []
    for student in students:
        qr = qrcode.make(student.roll_number)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        qrcodes.append({
            'student': student,
            'img_data': img_str,
        })
    return render(request, 'attendance/student_qrcodes.html', {'qrcodes': qrcodes})


def mark_attendance_by_roll(request):
    subjects = Subject.objects.all()
    message = ''
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')
        is_late = request.POST.get('is_late') == 'on'
        try:
            student = Student.objects.get(roll_number=roll_number)
            subject = Subject.objects.get(id=subject_id)
            Attendance.objects.create(
                student=student,
                subject=subject,
                date=date,
                time_marked=timezone.now().time(),
                is_late=is_late
            )
            message = f"Attendance marked for {student.name}."
        except Student.DoesNotExist:
            message = "Student with this roll number does not exist."
        except Subject.DoesNotExist:
            message = "Selected subject does not exist."
    return render(request, 'attendance/mark_by_roll.html', {'subjects': subjects, 'message': message})


def dashboard(request):
    from django.utils import timezone as dj_timezone
    today = dj_timezone.now().date()
    subjects = Subject.objects.all()
    dashboard_data = []
    for subject in subjects:
        total_present = Attendance.objects.filter(subject=subject, date=today).count()
        total_late = Attendance.objects.filter(subject=subject, date=today, is_late=True).count()
        dashboard_data.append({
            'subject': subject,
            'total_present': total_present,
            'total_late': total_late,
        })
    return render(request, 'attendance/dashboard.html', {'dashboard_data': dashboard_data, 'today': today})


def advanced_analytics(request):
    from django.db.models.functions import TruncMonth, TruncYear
    from django.db.models import Count
    subjects = Subject.objects.all()
    students = Student.objects.all()
    # Subject-wise attendance stats
    subject_stats = []
    for subject in subjects:
        total_attendance = Attendance.objects.filter(subject=subject).count()
        total_late = Attendance.objects.filter(subject=subject, is_late=True).count()
        subject_stats.append({
            'subject': subject,
            'total_attendance': total_attendance,
            'total_late': total_late,
        })
    # Late entry logs (last 30 entries)
    late_logs = Attendance.objects.filter(is_late=True).order_by('-date', '-time_marked')[:30]
    # Monthly and yearly reports
    monthly_report = (
        Attendance.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    yearly_report = (
        Attendance.objects
        .annotate(year=TruncYear('date'))
        .values('year')
        .annotate(count=Count('id'))
        .order_by('year')
    )
    return render(request, 'attendance/advanced_analytics.html', {
        'subject_stats': subject_stats,
        'late_logs': late_logs,
        'monthly_report': monthly_report,
        'yearly_report': yearly_report,
    })


def student_profile(request):
    students = Student.objects.all()
    selected_student = None
    subject_stats = []
    overall_attendance = 0
    total_classes = 0
    total_attended = 0
    total_late = 0
    if request.method == 'POST':
        student_id = request.POST.get('student')
        selected_student = Student.objects.get(id=student_id)
        subjects = Subject.objects.all()
        for subject in subjects:
            total = Attendance.objects.filter(subject=subject).count()
            attended = Attendance.objects.filter(subject=subject, student=selected_student).count()
            late = Attendance.objects.filter(subject=subject, student=selected_student, is_late=True).count()
            percent = (attended / total * 100) if total > 0 else 0
            subject_stats.append({
                'subject': subject,
                'attended': attended,
                'late': late,
                'percent': percent,
                'total': total,
            })
            total_classes += total
            total_attended += attended
            total_late += late
        overall_attendance = (total_attended / total_classes * 100) if total_classes > 0 else 0
    return render(request, 'attendance/student_profile.html', {
        'students': students,
        'selected_student': selected_student,
        'subject_stats': subject_stats,
        'overall_attendance': overall_attendance,
        'total_attended': total_attended,
        'total_late': total_late,
    })


def attendance_history(request):
    students = Student.objects.all()
    subjects = Subject.objects.all()
    records = Attendance.objects.select_related('student', 'subject').order_by('-date', '-time_marked')
    selected_student = request.GET.get('student')
    selected_subject = request.GET.get('subject')
    selected_date = request.GET.get('date')
    if selected_student:
        records = records.filter(student_id=selected_student)
    if selected_subject:
        records = records.filter(subject_id=selected_subject)
    if selected_date:
        records = records.filter(date=selected_date)
    return render(request, 'attendance/attendance_history.html', {
        'students': students,
        'subjects': subjects,
        'records': records,
        'selected_student': selected_student,
        'selected_subject': selected_subject,
        'selected_date': selected_date,
    })


def export_attendance_history_csv(request):
    records = Attendance.objects.select_related('student', 'subject').order_by('-date', '-time_marked')
    selected_student = request.GET.get('student')
    selected_subject = request.GET.get('subject')
    selected_date = request.GET.get('date')
    if selected_student:
        records = records.filter(student_id=selected_student)
    if selected_subject:
        records = records.filter(subject_id=selected_subject)
    if selected_date:
        records = records.filter(date=selected_date)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_history.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Time', 'Student', 'Subject', 'Late'])
    for record in records:
        writer.writerow([
            record.date,
            record.time_marked,
            record.student.name,
            record.subject.name,
            'Yes' if record.is_late else 'No',
        ])
    return response

def export_student_profile_csv(request):
    student_id = request.GET.get('student')
    if not student_id:
        return HttpResponse('Student not specified.', content_type='text/plain')
    student = Student.objects.get(id=student_id)
    subjects = Subject.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="student_profile_{student_id}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Subject', 'Classes Attended', 'Total Classes', 'Attendance %', 'Times Late'])
    for subject in subjects:
        total = Attendance.objects.filter(subject=subject).count()
        attended = Attendance.objects.filter(subject=subject, student=student).count()
        late = Attendance.objects.filter(subject=subject, student=student, is_late=True).count()
        percent = (attended / total * 100) if total > 0 else 0
        writer.writerow([
            subject.name,
            attended,
            total,
            f'{percent:.2f}',
            late,
        ])
    return response

def export_advanced_analytics_csv(request):
    subjects = Subject.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="advanced_analytics.csv"'
    writer = csv.writer(response)
    writer.writerow(['Subject', 'Total Attendance', 'Total Late'])
    for subject in subjects:
        total_attendance = Attendance.objects.filter(subject=subject).count()
        total_late = Attendance.objects.filter(subject=subject, is_late=True).count()
        writer.writerow([
            subject.name,
            total_attendance,
            total_late,
        ])
    return response

def bulk_attendance_upload(request):
    import csv
    from django.utils.dateparse import parse_date
    message = ''
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        created = 0
        errors = []
        for i, row in enumerate(reader, start=2):
            roll_number = row.get('roll_number')
            subject_id = row.get('subject_id')
            date = row.get('date')
            is_late = row.get('is_late', '').strip().lower() in ['1', 'true', 'yes', 'y']
            try:
                student = Student.objects.get(roll_number=roll_number)
                subject = Subject.objects.get(id=subject_id)
                Attendance.objects.create(
                    student=student,
                    subject=subject,
                    date=parse_date(date),
                    time_marked=timezone.now().time(),
                    is_late=is_late
                )
                created += 1
            except Exception as e:
                errors.append(f"Row {i}: {str(e)}")
        if errors:
            message = f"{created} records created. Errors: " + '; '.join(errors)
        else:
            message = f"Successfully created {created} attendance records."
    return render(request, 'attendance/bulk_attendance_upload.html', {'message': message})
