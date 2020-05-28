from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from AccessControl.views import (SignUp, LogIn, UploadAchivements, UploadKYC,
								VerifyEmail, ResetPassword, UploadProfilePic,
								VerificationLink, OTPVerification, GenerateOTP)

urlpatterns = [
	url(r'^v1/createuser/$', csrf_exempt(SignUp.as_view()), name="AccessControl_createuser"),
	url(r'^v1/login/$', csrf_exempt(LogIn.as_view()), name="AccessControl_login"),
	url(r'^v1/upload_achievements/$', csrf_exempt(UploadAchivements.as_view()), name="AccessControl_achievement"),
	url(r'^v1/upload_kyc/$', csrf_exempt(UploadKYC.as_view()), name="AccessControl_kyc"),
	url(r'^v1/verify_email/$', csrf_exempt(VerifyEmail.as_view()), name="AccessControl_verifyemail"),
	url(r'^v1/verify_otp/$', csrf_exempt(OTPVerification.as_view()), name="AccessControl_verifyotp"),
	url(r'^v1/generate_otp/$', csrf_exempt(GenerateOTP.as_view()), name="AccessControl_generateotp"),
	url(r'^v1/send_verification_link/$', csrf_exempt(VerificationLink.as_view()), name="verification_link"),
	url(r'^v1/reset_password/$', csrf_exempt(ResetPassword.as_view()), name="AccessControl_resetpassword"),
	url(r'^v1/upload_profile_pic/$', csrf_exempt(UploadProfilePic.as_view()), name="AccessControl_profilepic"),

]