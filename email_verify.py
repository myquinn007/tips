from models import User, Music, EmailGroup, SendEmail, VerificationEmail


def email_verified_check(email):
    verify = VerificationEmail.query.filter(VerificationEmail.email == email).first()
    if verify:
        if verify.verified == 1:
            return   'verified'         
           
        if not verify.verification_test:
            verify.verification_test = 0
        #
        #
        # Check the time for 10 minutes
        if verify.verification_test <= 1:
            # Resend email with db_email.verification_test 
            return   'waiting'
            
        else:
            return 'waiting-confirmation'
    else:
        return 'not_verified'
