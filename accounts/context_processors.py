def email_verification_status(request):
    if request.user.is_authenticated:
        return {'email_verified': request.user.verified_email}
    return {'email_verified': False}