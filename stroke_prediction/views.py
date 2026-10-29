from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
# FILE UPLOAD AND VIEW
from  django.core.files.storage import FileSystemStorage
# SESSION
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import secrets
from django.db.models import Q
from .models import *


def first(request):
    return render(request,'index.html')
def index(request):
    return render(request,'index.html')
def addreg(request):
    """Handle user registration with validation"""
    if request.method=="POST":
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone_number', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Validation checks
        error_message = None

        if not name or not phone or not email or not password:
            error_message = 'Please fill in all required fields.'
        elif len(password) < 6:
            error_message = 'Password must be at least 6 characters long.'
        elif password != confirm_password:
            error_message = 'Passwords do not match.'
        elif regtable.objects.filter(email=email).exists():
            error_message = 'Email address is already registered. Please use a different email or try logging in.'
        elif '@' not in email:
            error_message = 'Please enter a valid email address.'
        elif not phone.isdigit() or len(phone) < 10:
            error_message = 'Please enter a valid phone number (at least 10 digits).'

        if error_message:
            return render(request, 'register.html', {
                'error_message': error_message,
                'form_data': {'name': name, 'email': email, 'phone': phone}
            })

        # Create new user
        try:
            user = regtable(name=name, phone_number=phone, email=email, password=password)
            user.save()
            return render(request, 'register.html', {
                'success_message': 'Registration successful! You can now login.'
            })
        except Exception as e:
            return render(request, 'register.html', {
                'error_message': 'An error occurred during registration. Please try again.'
            })

    return render(request, 'register.html')

def register(request):
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')

def addlogin(request):
    """Handle user login with specific error messages"""
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()

    if not email or not password:
        return render(request, 'login.html', {
            'error_message': 'Please enter both email and password.'
        })

    # Check for admin login
    if email == 'admin@gmail.com':
        if password == 'admin':
            request.session['admin'] = 'admin'
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {
                'error_message': 'Incorrect password. Please try again.'
            })

    # Check if email exists in database
    user_exists = regtable.objects.filter(email=email).exists()

    if not user_exists:
        return render(request, 'login.html', {
            'error_message': 'Email address not found. Please check your email or register a new account.'
        })

    # Email exists, check password
    if regtable.objects.filter(email=email, password=password).exists():
        userdetails = regtable.objects.get(email=email, password=password)
        request.session['uid'] = userdetails.id
        request.session['user_name'] = userdetails.name
        return render(request, 'index.html')
    else:
        return render(request, 'login.html', {
            'error_message': 'Incorrect password. Please try again.'
        })
    



def v_users(request):
    """Admin view for managing all users"""
    # Get search query if provided
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-id')  # Default sort by newest first
    
    # Get all users
    users = regtable.objects.all()
    
    # Apply search filter
    if search_query:
        users = users.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    # Apply sorting
    users = users.order_by(sort_by)
    
    # Get statistics
    total_users = regtable.objects.count()
    total_predictions = Prediction.objects.count()
    
    # Get list of users with predictions
    users_with_predictions = Prediction.objects.values_list('user_id', flat=True).distinct()
    users_with_predictions_list = list(users_with_predictions)
    users_with_predictions_count = len(users_with_predictions_list)
    
    context = {
        'users': users,
        'total_users': total_users,
        'total_predictions': total_predictions,
        'users_with_predictions': users_with_predictions_count,
        'users_with_predictions_list': users_with_predictions_list,
        'search_query': search_query,
        'current_sort': sort_by
    }
    
    return render(request, 'all_users.html', context)


def logout(request):
    session_keys=list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(first)

def get_risk_level(probability):
    """Determine risk level based on stroke probability"""
    if probability >= 70:
        return 'High'
    elif probability >= 40:
        return 'Medium'
    else:
        return 'Low'

def generate_health_advice(age, hypertension, heart_disease, glucose, bmi, smoking_status):
    advice = []

    if hypertension == 1 or hypertension == "Yes":
        advice.append("🔴 Control blood pressure with regular monitoring and medication.")

    if heart_disease == 1 or heart_disease == "Yes":
        advice.append("🔴 Consult a cardiologist and follow heart healthy lifestyle.")

    if glucose > 140:
        advice.append("⚠️  Your glucose level is high. Reduce sugar intake and check blood sugar regularly.")

    if bmi >= 30:
        advice.append("⚠️  Your BMI indicates obesity. Maintain healthy weight through exercise and balanced diet.")

    if smoking_status != "never smoked" and smoking_status != "Unknown":
        advice.append("🚭 Avoid smoking to reduce stroke risk.")

    if age > 50:
        advice.append("📋 Schedule regular medical checkups and health monitoring.")

    if not advice:
        advice.append("✅ Maintain a balanced diet and regular exercise to keep stroke risk low.")

    return advice

def get_employment_type_display(work_type):
    """Convert work type code to professional display name"""
    employment_types = {
        'Private': '🏢 Private Sector',
        'Self-employed': '💼 Self-employed / Entrepreneur',
        'Govt_job': '🏛️ Public Sector / Government',
        'children': '👨‍🎓 Student',
        'Never_worked': '📋 Unemployed / Job Seeker'
    }
    return employment_types.get(work_type, work_type)

def user_profile(request):
    if 'uid' in request.session:
        user = regtable.objects.get(id=request.session['uid'])
        return render(request, 'profile.html', {'user': user})
    else:
        return redirect('login')

def predict_stroke(request):
    if request.method == 'POST':
        # Get form data
        gender = request.POST.get('gender')
        age = int(request.POST.get('age'))
        hypertension = int(request.POST.get('hypertension'))
        heart_disease = int(request.POST.get('heart_disease'))
        ever_married = request.POST.get('ever_married')
        work_type = request.POST.get('work_type')
        residence_type = request.POST.get('residence_type')
        avg_glucose_level = float(request.POST.get('avg_glucose_level'))
        bmi = float(request.POST.get('bmi'))
        smoking_status = request.POST.get('smoking_status')

        # Prepare data for prediction
        data = {
            'gender': gender,
            'age': age,
            'hypertension': hypertension,
            'heart_disease': heart_disease,
            'ever_married': ever_married,
            'work_type': work_type,
            'Residence_type': residence_type,
            'avg_glucose_level': avg_glucose_level,
            'bmi': bmi,
            'smoking_status': smoking_status
        }

        # Import and use the inference function
        import sys
        import os
        ml_path = os.path.join(settings.BASE_DIR, 'ML')
        sys.path.append(ml_path)
        from inference import predict_stroke as ml_predict

        # Get prediction from XGBoost (as it's mentioned in the filename)
        result = ml_predict(data, model='xgboost')

        prediction = 'Yes' if result['prediction'] == 1 else 'No'
        # Convert probabilities to percentage (multiply by 100)
        prob_no = result['probability_no_stroke'] * 100
        prob_yes = result['probability_stroke'] * 100

        # Determine risk level
        risk_level = get_risk_level(prob_yes)

        # Generate personalized health advice based on prediction
        advice = generate_health_advice(
            age=age,
            hypertension=hypertension,
            heart_disease=heart_disease,
            glucose=avg_glucose_level,
            bmi=bmi,
            smoking_status=smoking_status
        )

        # Save prediction to database
        prediction_obj = None
        if 'uid' in request.session:
            user = regtable.objects.get(id=request.session['uid'])
            prediction_obj = Prediction.objects.create(
                user=user,
                gender=gender,
                age=age,
                hypertension=hypertension,
                heart_disease=heart_disease,
                ever_married=ever_married,
                work_type=work_type,
                residence_type=residence_type,
                avg_glucose_level=avg_glucose_level,
                bmi=bmi,
                smoking_status=smoking_status,
                prediction_result=prediction,
                probability_no_stroke=prob_no,
                probability_stroke=prob_yes
            )

        return render(request, 'predict.html', {
            'prediction': prediction,
            'prob_no': prob_no,
            'prob_yes': prob_yes,
            'risk_level': risk_level,
            'form_data': data,
            'advice': advice,
            'last_prediction_id': prediction_obj.id if prediction_obj else None,
            'work_type_display': get_employment_type_display(work_type)
        })
    else:
        return render(request, 'predict.html')

def prediction_history(request):
    if 'uid' in request.session:
        user = regtable.objects.get(id=request.session['uid'])
        predictions = Prediction.objects.filter(user=user).order_by('-created_at')
        return render(request, 'prediction_history.html', {'predictions': predictions})
    else:
        return redirect('login')

def admin_predictions(request):
    if 'admin' in request.session:
        predictions = Prediction.objects.all().select_related('user').order_by('-created_at')
        return render(request, 'admin_predictions.html', {'predictions': predictions})
    else:
        return redirect('login')


# Consultation Views
def request_consultation(request, prediction_id):
    """Handle consultation request submission"""
    if 'uid' not in request.session:
        return redirect('login')
    
    user = regtable.objects.get(id=request.session['uid'])
    
    try:
        prediction = Prediction.objects.get(id=prediction_id, user=user)
    except Prediction.DoesNotExist:
        return redirect('predict_stroke')

    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ConsultationRequest.objects.create(
            user=user,
            prediction=prediction,
            patient_name=patient_name,
            email=email,
            message=message
        )
        
        return render(request, 'consultation_form.html', {
            'success_message': 'Consultation request submitted successfully! The admin will review your request.',
            'prediction_id': prediction_id
        })
    
    return render(request, 'consultation_form.html', {
        'prediction': prediction,
        'prediction_id': prediction_id,
        'user': user
    })


def view_consultation_status(request):
    """View all consultation requests for logged-in user"""
    if 'uid' not in request.session:
        return redirect('login')
    
    user = regtable.objects.get(id=request.session['uid'])
    consultations = ConsultationRequest.objects.filter(user=user).order_by('-created_at')
    
    return render(request, 'consultation_status.html', {
        'consultations': consultations
    })
def admin_consultations(request):
    if 'admin' in request.session:
        consultations = ConsultationRequest.objects.all().select_related('user').order_by('-created_at')
        return render(request, 'admin_consultations.html', {'consultations': consultations})
    else:
        return redirect('login')


def admin_consultation_requests(request):
    """Admin view for all consultation requests"""
    if 'admin' not in request.session:
        return redirect('login')
    
    consultations = ConsultationRequest.objects.all().select_related('user', 'prediction').order_by('-created_at')
    
    return render(request, 'admin_consultations.html', {
        'consultations': consultations
    })


def approve_consultation(request, consultation_id):
    """Approve a consultation request and assign a doctor"""
    if 'admin' not in request.session:
        return redirect('login')
    
    try:
        consultation = ConsultationRequest.objects.get(id=consultation_id)
    except ConsultationRequest.DoesNotExist:
        return redirect('admin_consultation_requests')

    available_doctors = Doctor.objects.filter(is_approved=True).order_by('name')

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        consultation_message = request.POST.get('consultation_message', '')
        meeting_link = request.POST.get('meeting_link', '')

        try:
            doctor = Doctor.objects.get(id=doctor_id, is_approved=True)
        except Doctor.DoesNotExist:
            return render(request, 'approve_consultation.html', {
                'consultation': consultation,
                'available_doctors': available_doctors,
                'error_message': 'Please select a valid doctor.'
            })

        consultation.doctor = doctor
        consultation.doctor_name = doctor.name
        consultation.consultation_message = consultation_message
        consultation.meeting_link = meeting_link if meeting_link else None
        consultation.status = 'Approved'
        consultation.save()

        return redirect('admin_consultation_requests')
    
    return render(request, 'approve_consultation.html', {
        'consultation': consultation,
        'available_doctors': available_doctors
    })


def reject_consultation(request, consultation_id):
    """Reject a consultation request"""
    if 'admin' not in request.session:
        return redirect('login')
    
    try:
        consultation = ConsultationRequest.objects.get(id=consultation_id)
    except ConsultationRequest.DoesNotExist:
        return redirect('admin_consultation_requests')

    if request.method == 'POST':
        consultation.status = 'Rejected'
        consultation.save()
        return redirect('admin_consultation_requests')
    
    return render(request, 'reject_consultation.html', {
        'consultation': consultation
    })


# Doctor Views
def doctor_register(request):
    """Handle doctor registration with proof document and validation"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        qualification = request.POST.get('qualification', '').strip()
        specialization = request.POST.get('specialization', '').strip()
        experience_str = request.POST.get('years_of_experience', '').strip()
        proof_document = request.FILES.get('proof_document')

        # Validation
        error_message = None

        # Required fields check
        if not all([name, email, phone_number, password, qualification, specialization, experience_str, proof_document]):
            error_message = 'Please fill in all required fields including proof document.'
        
        # Password validation
        elif len(password) < 6:
            error_message = 'Password must be at least 6 characters long.'
        elif password != confirm_password:
            error_message = 'Passwords do not match.'
        
        # Email validation
        elif Doctor.objects.filter(email=email).exists():
            error_message = 'Email is already registered as a doctor. Please use a different email.'
        elif '@' not in email:
            error_message = 'Please enter a valid email address.'
        
        # Phone validation
        elif not phone_number.isdigit() or len(phone_number) < 10:
            error_message = 'Please enter a valid phone number (at least 10 digits).'
        
        # Experience validation
        elif not experience_str.isdigit() or int(experience_str) < 0:
            error_message = 'Years of experience must be a valid number.'
        
        # File validation
        elif proof_document.size > 5 * 1024 * 1024:  # 5MB limit
            error_message = 'Proof document must be less than 5MB.'

        if error_message:
            return render(request, 'doctor_register.html', {
                'error_message': error_message,
                'form_data': {
                    'name': name,
                    'email': email,
                    'phone': phone_number,
                    'qualification': qualification,
                    'specialization': specialization,
                    'experience': experience_str
                }
            })

        try:
            years_of_experience = int(experience_str)
            
            # Create doctor record (pending approval)
            doctor = Doctor.objects.create(
                name=name,
                email=email,
                phone_number=phone_number,
                password=password,
                qualification=qualification,
                specialization=specialization,
                years_of_experience=years_of_experience,
                proof_document=proof_document,
                is_approved=False
            )

            return render(request, 'doctor_register.html', {
                'success_message': 'Registration successful! Your credentials will be reviewed by admin. You will receive approval notification soon.'
            })
        except Exception as e:
            return render(request, 'doctor_register.html', {
                'error_message': 'An error occurred during registration. Please try again.'
            })

    return render(request, 'doctor_register.html')


def doctor_login(request):
    """Handle doctor login - only approved doctors can login with specific error messages"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not email or not password:
            return render(request, 'doctor_login.html', {
                'error_message': 'Please enter both email and password.'
            })

        # Check if doctor email exists
        doctor_exists = Doctor.objects.filter(email=email).exists()

        if not doctor_exists:
            return render(request, 'doctor_login.html', {
                'error_message': 'Email address not found in our doctor database. Please check your email.'
            })

        # Check password
        try:
            doctor = Doctor.objects.get(email=email)
            if doctor.password != password:
                return render(request, 'doctor_login.html', {
                    'error_message': 'Incorrect password. Please try again.'
                })
        except Doctor.DoesNotExist:
            return render(request, 'doctor_login.html', {
                'error_message': 'Email address not found in our doctor database.'
            })

        # Check if doctor is approved
        if not doctor.is_approved:
            return render(request, 'doctor_login.html', {
                'error_message': 'Your account has not been approved yet. Please wait for admin approval or contact support.'
            })

        # Set session
        request.session['doctor_id'] = doctor.id
        request.session['doctor_name'] = doctor.name
        return redirect('doctor_dashboard')

    return render(request, 'doctor_login.html')


def doctor_dashboard(request):
    """Doctor dashboard - view assigned consultations"""
    if 'doctor_id' not in request.session:
        return redirect('doctor_login')

    doctor = Doctor.objects.get(id=request.session['doctor_id'])
    consultations = ConsultationRequest.objects.filter(
        doctor=doctor,
        status='Approved'
    ).select_related('user', 'prediction').order_by('-created_at')

    return render(request, 'doctor_dashboard.html', {
        'doctor': doctor,
        'consultations': consultations
    })


def update_consultation_response(request, consultation_id):
    """Doctor updates consultation response"""
    if 'doctor_id' not in request.session:
        return redirect('doctor_login')

    doctor = Doctor.objects.get(id=request.session['doctor_id'])

    try:
        consultation = ConsultationRequest.objects.get(id=consultation_id, doctor=doctor)
    except ConsultationRequest.DoesNotExist:
        return redirect('doctor_dashboard')

    if request.method == 'POST':
        consultation_message = request.POST.get('consultation_message')
        meeting_link = request.POST.get('meeting_link', '')

        consultation.consultation_message = consultation_message
        consultation.meeting_link = meeting_link if meeting_link else None
        consultation.save()

        return render(request, 'doctor_consultation_detail.html', {
            'consultation': consultation,
            'success_message': 'Response updated successfully!'
        })

    return render(request, 'doctor_consultation_detail.html', {
        'consultation': consultation
    })


def admin_doctor_approvals(request):
    """Admin view for pending doctor registrations"""
    if 'admin' not in request.session:
        return redirect('login')

    pending_doctors = Doctor.objects.filter(is_approved=False).order_by('-created_at')
    approved_doctors = Doctor.objects.filter(is_approved=True).order_by('-created_at')

    return render(request, 'admin_doctor_approvals.html', {
        'pending_doctors': pending_doctors,
        'approved_doctors': approved_doctors
    })


def approve_doctor(request, doctor_id):
    """Admin approves a doctor registration"""
    if 'admin' not in request.session:
        return redirect('login')

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return redirect('admin_doctor_approvals')

    if request.method == 'POST':
        from datetime import datetime
        doctor.is_approved = True
        doctor.approval_date = datetime.now()
        doctor.save()

        return redirect('admin_doctor_approvals')

    return render(request, 'approve_doctor.html', {
        'doctor': doctor
    })


def reject_doctor(request, doctor_id):
    """Admin rejects a doctor registration"""
    if 'admin' not in request.session:
        return redirect('login')

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return redirect('admin_doctor_approvals')

    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason', '')
        doctor.rejection_reason = rejection_reason
        doctor.delete()  # Delete the doctor record
        return redirect('admin_doctor_approvals')

    return render(request, 'reject_doctor.html', {
        'doctor': doctor
    })


def doctor_logout(request):
    """Logout doctor"""
    session_keys = list(request.session.keys())
    for key in session_keys:
        if key.startswith('doctor'):
            del request.session[key]
    return redirect('doctor_login')


# Forgot Password Views - Token Based Security
def forgot_password(request):
    """User forgot password - Generate secure token"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = regtable.objects.get(email=email)
            # Generate secure token (32 bytes = 256 bits)
            token = secrets.token_urlsafe(32)
            # Token expires in 24 hours
            expiration_time = timezone.now() + timedelta(hours=24)
            
            # Save token and expiration to database
            user.password_reset_token = token
            user.password_reset_token_expire = expiration_time
            user.save()
            
            # In production, send email with reset link:
            # reset_link = f"http://yourdomain.com/reset-password/{token}/"
            # send_email(email, reset_link)
            
            return render(request, 'forgot_password.html', {
                'success_message': f'Password reset token generated. Use the reset link to set your new password.',
                'token': token,
                'show_reset_form': True
            })
        except regtable.DoesNotExist:
            return render(request, 'forgot_password.html', {
                'error_message': 'No account found with this email address.'
            })
    
    return render(request, 'forgot_password.html')


def reset_password(request, token):
    """Reset password with valid token"""
    try:
        user = regtable.objects.get(password_reset_token=token)
        
        # Check if token is expired
        if user.password_reset_token_expire < timezone.now():
            return render(request, 'reset_password.html', {
                'error_message': 'This password reset link has expired. Please request a new one.',
                'token_expired': True
            })
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # Validate passwords
            if not new_password or len(new_password) < 6:
                return render(request, 'reset_password.html', {
                    'error_message': 'Password must be at least 6 characters long.',
                    'token': token
                })
            
            if new_password != confirm_password:
                return render(request, 'reset_password.html', {
                    'error_message': 'Passwords do not match.',
                    'token': token
                })
            
            # Update password and clear token
            user.password = new_password
            user.password_reset_token = None
            user.password_reset_token_expire = None
            user.save()
            
            return render(request, 'reset_password.html', {
                'success_message': 'Your password has been successfully reset. You can now login with your new password.',
                'show_success': True
            })
        
        return render(request, 'reset_password.html', {
            'token': token,
            'show_form': True
        })
        
    except regtable.DoesNotExist:
        return render(request, 'reset_password.html', {
            'error_message': 'Invalid password reset link.'
        })


def doctor_forgot_password(request):
    """Doctor forgot password - Generate secure token"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            doctor = Doctor.objects.get(email=email)
            # Generate secure token
            token = secrets.token_urlsafe(32)
            # Token expires in 24 hours
            expiration_time = timezone.now() + timedelta(hours=24)
            
            # Save token and expiration to database
            doctor.password_reset_token = token
            doctor.password_reset_token_expire = expiration_time
            doctor.save()
            
            # In production, send email with reset link:
            # reset_link = f"http://yourdomain.com/reset-doctor-password/{token}/"
            # send_email(email, reset_link)
            
            return render(request, 'doctor_forgot_password.html', {
                'success_message': f'Password reset token generated. Use the reset link to set your new password.',
                'token': token,
                'show_reset_form': True
            })
        except Doctor.DoesNotExist:
            return render(request, 'doctor_forgot_password.html', {
                'error_message': 'No doctor account found with this email address.'
            })
    
    return render(request, 'doctor_forgot_password.html')


def reset_doctor_password(request, token):
    """Reset doctor password with valid token"""
    try:
        doctor = Doctor.objects.get(password_reset_token=token)
        
        # Check if token is expired
        if doctor.password_reset_token_expire < timezone.now():
            return render(request, 'reset_doctor_password.html', {
                'error_message': 'This password reset link has expired. Please request a new one.',
                'token_expired': True
            })
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # Validate passwords
            if not new_password or len(new_password) < 6:
                return render(request, 'reset_doctor_password.html', {
                    'error_message': 'Password must be at least 6 characters long.',
                    'token': token
                })
            
            if new_password != confirm_password:
                return render(request, 'reset_doctor_password.html', {
                    'error_message': 'Passwords do not match.',
                    'token': token
                })
            
            # Update password and clear token
            doctor.password = new_password
            doctor.password_reset_token = None
            doctor.password_reset_token_expire = None
            doctor.save()
            
            return render(request, 'reset_doctor_password.html', {
                'success_message': 'Your password has been successfully reset. You can now login with your new password.',
                'show_success': True
            })
        
        return render(request, 'reset_doctor_password.html', {
            'token': token,
            'show_form': True
        })
        
    except Doctor.DoesNotExist:
        return render(request, 'reset_doctor_password.html', {
            'error_message': 'Invalid password reset link.'
        })