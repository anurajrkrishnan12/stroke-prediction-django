from django.db import models



class regtable(models.Model):
    name=models.CharField(max_length=150)
    phone_number=models.CharField(max_length=120)
    email=models.CharField(max_length=120)
    password=models.CharField(max_length=120)
    password_reset_token=models.CharField(max_length=255, blank=True, null=True)
    password_reset_token_expire=models.DateTimeField(blank=True, null=True)


class Prediction(models.Model):
    user = models.ForeignKey(regtable, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    hypertension = models.IntegerField()
    heart_disease = models.IntegerField()
    ever_married = models.CharField(max_length=10)
    work_type = models.CharField(max_length=30)
    residence_type = models.CharField(max_length=10)
    avg_glucose_level = models.FloatField()
    bmi = models.FloatField()
    smoking_status = models.CharField(max_length=20)
    prediction_result = models.CharField(max_length=5)
    probability_no_stroke = models.FloatField()
    probability_stroke = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.user.name} - {self.prediction_result}"


class ConsultationRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(regtable, on_delete=models.CASCADE)
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField(help_text="Message or symptoms description")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, blank=True, null=True, related_name='consultations')
    doctor_name = models.CharField(max_length=150, blank=True, null=True)
    consultation_message = models.TextField(blank=True, null=True, help_text="Doctor's response")
    meeting_link = models.URLField(blank=True, null=True, help_text="Video consultation link")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consultation Request from {self.patient_name} - {self.status}"

    class Meta:
        ordering = ['-created_at']


class Doctor(models.Model):
    QUALIFICATION_CHOICES = [
        ('MD', 'Medicine (MD)'),
        ('DO', 'Osteopathic Medicine (DO)'),
        ('MBBS', 'MBBS'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    qualification = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES)
    specialization = models.CharField(max_length=150, help_text="e.g., Cardiology, Neurology, General Practice")
    years_of_experience = models.IntegerField()
    proof_document = models.FileField(upload_to='doctor_proofs/', help_text="Medical license, certificate, or degree")
    is_approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    password_reset_token_expire = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization}) - {'Approved' if self.is_approved else 'Pending'}"

    class Meta:
        ordering = ['-created_at']
