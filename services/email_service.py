"""
Email service using SendGrid API
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for handling email operations"""

    def __init__(self, config):
        # Validate required config
        api_key = config.get('SENDGRID_API_KEY')
        from_email = config.get('FROM_EMAIL')

        if not api_key:
            raise ValueError("SENDGRID_API_KEY not found in config. Please add it to .env file")

        if not from_email:
            raise ValueError("FROM_EMAIL not found in config. Please add it to .env file")

        self.sg = SendGridAPIClient(api_key)
        self.from_email = from_email
        self.config = config
        logger.info(f"Email service initialized with SendGrid. Sender: {from_email}")

    def send_verification_email(self, email, verification_token, unique_number):
        """Send verification email with login link and unique number"""
        verification_link = f"{self.config.get('BASE_URL', 'http://localhost:5000')}/auth/verify?token={verification_token}"

        # Create email HTML content
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px 10px 0 0;">
                    <h2 style="color: white; margin: 0;">Welcome to RoomSense!</h2>
                </div>
                <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                    <p style="font-size: 16px; color: #333;">Your unique ID is:</p>
                    <p style="background: white; padding: 15px; border-radius: 5px; text-align: center;">
                        <strong style="font-size: 24px; color: #667eea; letter-spacing: 2px;">{unique_number}</strong>
                    </p>
                    
                    <p style="font-size: 16px; color: #333; margin-top: 30px;">Click the button below to verify your email and complete your login:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{verification_link}" 
                           style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                  color: white; 
                                  padding: 15px 40px; 
                                  text-decoration: none; 
                                  border-radius: 25px; 
                                  display: inline-block;
                                  font-weight: bold;
                                  font-size: 16px;
                                  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);">
                            Verify Email Address
                        </a>
                    </div>
                    
                    <p style="color: #666; font-size: 14px; margin-top: 30px;">Or copy and paste this link into your browser:</p>
                    <p style="background: white; padding: 12px; border-radius: 5px; word-break: break-all; font-size: 12px; color: #667eea;">
                        {verification_link}
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                    
                    <p style="color: #999; font-size: 12px; text-align: center;">
                        ⏱️ This link will expire in 15 minutes<br>
                        If you didn't request this, please ignore this email.
                    </p>
                </div>
            </body>
        </html>
        """

        try:
            # Create the message using the correct format
            message = Mail(
                from_email=(self.from_email, 'RoomSense'),  # Tuple format: (email, name)
                to_emails=email,
                subject='RoomSense - Verify Your Email',
                html_content=html_content
            )

            response = self.sg.send(message)
            logger.info(f"✅ Verification email sent to: {email}, Status: {response.status_code}")
            return True

        except Exception as e:
            logger.error(f"❌ SendGrid error for {email}: {str(e)}")
            raise