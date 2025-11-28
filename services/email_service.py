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

    def send_verification_email(self, email, sessionId):
        """Send verification email with login link"""
        verification_link = f"{self.config.get('BASE_URL', 'http://localhost:5000')}/auth/verify?sessionId={sessionId}"

        # Create professional email HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title>Verify Your Email - RoomSense</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif; background-color: #f3f4f6;">
            <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f3f4f6;">
                <tr>
                    <td align="center" style="padding: 40px 20px;">
                        <table role="presentation" style="max-width: 600px; width: 100%; border-collapse: collapse; background: white; border-radius: 16px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                            
                            <!-- Header with gradient -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 48px 40px; border-radius: 16px 16px 0 0; text-align: center;">
                                    <div style="width: 64px; height: 64px; background: rgba(255, 255, 255, 0.2); border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 16px;">
                                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                                            <polyline points="22,6 12,13 2,6"/>
                                        </svg>
                                    </div>
                                    <h1 style="margin: 0; color: white; font-size: 28px; font-weight: 700; letter-spacing: -0.5px;">
                                        Verify Your Email
                                    </h1>
                                    <p style="margin: 12px 0 0 0; color: rgba(255, 255, 255, 0.9); font-size: 16px;">
                                        Welcome to RoomSense
                                    </p>
                                </td>
                            </tr>
                            
                            <!-- Content -->
                            <tr>
                                <td style="padding: 40px;">
                                    <p style="margin: 0 0 24px 0; color: #374151; font-size: 16px; line-height: 1.6;">
                                        Hello,
                                    </p>
                                    
                                    <p style="margin: 0 0 32px 0; color: #374151; font-size: 16px; line-height: 1.6;">
                                        Thank you for signing up! To complete your registration and access your RoomSense account, please verify your email address by clicking the button below.
                                    </p>
                                    
                                    <!-- CTA Button -->
                                    <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                        <tr>
                                            <td align="center" style="padding: 8px 0;">
                                                <a href="{verification_link}" 
                                                   style="display: inline-block; 
                                                          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                                          color: white; 
                                                          text-decoration: none; 
                                                          padding: 16px 48px; 
                                                          border-radius: 12px; 
                                                          font-weight: 600; 
                                                          font-size: 16px;
                                                          box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
                                                          text-align: center;">
                                                    Verify Email Address
                                                </a>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <!-- Info Box -->
                                    <div style="margin: 32px 0; padding: 20px; background: linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%); border: 1px solid #c7d2fe; border-radius: 12px;">
                                        <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                            <tr>
                                                <td style="padding-right: 16px; vertical-align: top; width: 24px;">
                                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                        <circle cx="12" cy="12" r="10"/>
                                                        <line x1="12" y1="16" x2="12" y2="12"/>
                                                        <line x1="12" y1="8" x2="12.01" y2="8"/>
                                                    </svg>
                                                </td>
                                                <td>
                                                    <p style="margin: 0; color: #4338ca; font-size: 14px; line-height: 1.6; font-weight: 500;">
                                                        <strong>Security Note:</strong> This verification link will expire in 15 minutes for your security.
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </div>
                                    
                                    <!-- Divider -->
                                    <div style="margin: 32px 0; border-top: 1px solid #e5e7eb;"></div>
                                    
                                    <!-- Alternative link -->
                                    <p style="margin: 0 0 12px 0; color: #6b7280; font-size: 14px;">
                                        If the button doesn't work, copy and paste this link into your browser:
                                    </p>
                                    <p style="margin: 0; padding: 12px; background: #f9fafb; border-radius: 8px; word-break: break-all; font-size: 13px; color: #667eea; font-family: 'Courier New', monospace;">
                                        {verification_link}
                                    </p>
                                    
                                    <div style="margin: 32px 0; border-top: 1px solid #e5e7eb;"></div>
                                    
                                    <!-- Footer note -->
                                    <p style="margin: 0; color: #9ca3af; font-size: 13px; line-height: 1.6;">
                                        If you didn't create an account with RoomSense, you can safely ignore this email.
                                    </p>
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td style="padding: 32px 40px; background: #f9fafb; border-radius: 0 0 16px 16px; text-align: center;">
                                    <p style="margin: 0 0 8px 0; color: #111827; font-weight: 600; font-size: 16px;">
                                        RoomSense
                                    </p>
                                    <p style="margin: 0; color: #6b7280; font-size: 13px; line-height: 1.6;">
                                        Smart Classroom Management Platform
                                    </p>
                                    <div style="margin: 16px 0 0 0; padding-top: 16px; border-top: 1px solid #e5e7eb;">
                                        <p style="margin: 0; color: #9ca3af; font-size: 12px;">
                                            © 2024 RoomSense. All rights reserved.
                                        </p>
                                    </div>
                                </td>
                            </tr>
                            
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        try:
            # Create the message using the correct format
            message = Mail(
                from_email=(self.from_email, 'RoomSense'),  # Tuple format: (email, name)
                to_emails=email,
                subject='Verify Your Email - RoomSense',
                html_content=html_content
            )

            response = self.sg.send(message)
            logger.info(f"✅ Verification email sent to: {email}, Status: {response.status_code}")
            return True

        except Exception as e:
            logger.error(f"❌ SendGrid error for {email}: {str(e)}")
            raise