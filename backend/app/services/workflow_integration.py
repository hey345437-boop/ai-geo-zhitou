"""
Workflow & Integration Hub
Slack, Email, Webhook integrations and report automation
"""
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class IntegrationType(Enum):
    """Integration types"""
    SLACK = "slack"
    EMAIL = "email"
    WEBHOOK = "webhook"
    TEAMS = "teams"


@dataclass
class IntegrationConfig:
    """Integration configuration"""
    id: str
    type: IntegrationType
    name: str
    enabled: bool
    config: Dict
    created_at: datetime


class SlackIntegration:
    """Slack webhook integration"""
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url
        self.connected = False
    
    def connect(self) -> bool:
        """Test Slack connection"""
        if not self.webhook_url:
            logger.error("Slack webhook URL not configured")
            return False
        
        logger.info("Slack integration connected")
        self.connected = True
        return True
    
    def send_notification(
        self,
        message: str,
        channel: Optional[str] = None,
        attachments: Optional[List[Dict]] = None
    ) -> bool:
        """
        Send notification to Slack
        
        Args:
            message: Message text
            channel: Slack channel (optional)
            attachments: Message attachments
        """
        if not self.connected:
            logger.warning("Slack not connected")
            return False
        
        # Build Slack message payload
        payload = {
            "text": message,
            "username": "智投",
            "icon_emoji": ":chart_with_upwards_trend:"
        }
        
        if channel:
            payload["channel"] = channel
        
        if attachments:
            payload["attachments"] = attachments
        
        # Mock send (replace with actual HTTP POST)
        logger.info(f"Sending Slack notification: {message[:50]}...")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        return True
    
    def send_alert(
        self,
        alert_type: str,
        title: str,
        description: str,
        severity: str = "info"
    ) -> bool:
        """Send formatted alert to Slack"""
        # Color coding
        colors = {
            "critical": "#FF0000",
            "warning": "#FFA500",
            "info": "#0000FF",
            "success": "#00FF00"
        }
        
        attachment = {
            "color": colors.get(severity, "#808080"),
            "title": title,
            "text": description,
            "fields": [
                {
                    "title": "Alert Type",
                    "value": alert_type,
                    "short": True
                },
                {
                    "title": "Severity",
                    "value": severity.upper(),
                    "short": True
                },
                {
                    "title": "Timestamp",
                    "value": datetime.now().isoformat(),
                    "short": False
                }
            ],
            "footer": "智投",
            "ts": int(datetime.now().timestamp())
        }
        
        return self.send_notification(
            message=f"🚨 {title}",
            attachments=[attachment]
        )
    
    def send_report(
        self,
        report_title: str,
        metrics: Dict,
        summary: str
    ) -> bool:
        """Send formatted report to Slack"""
        # Build metrics fields
        fields = []
        for metric_name, metric_value in metrics.items():
            fields.append({
                "title": metric_name.replace("_", " ").title(),
                "value": str(metric_value),
                "short": True
            })
        
        attachment = {
            "color": "#36a64f",
            "title": report_title,
            "text": summary,
            "fields": fields,
            "footer": "智投报告",
            "ts": int(datetime.now().timestamp())
        }
        
        return self.send_notification(
            message=f"📊 {report_title}",
            attachments=[attachment]
        )


class EmailNotification:
    """Email notification service"""
    
    def __init__(self, smtp_config: Dict = None):
        self.smtp_config = smtp_config or {}
        self.connected = False
    
    def connect(self) -> bool:
        """Connect to SMTP server"""
        logger.info("Email service connected")
        self.connected = True
        return True
    
    def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        html: bool = False,
        attachments: Optional[List[Dict]] = None
    ) -> bool:
        """
        Send email
        
        Args:
            to: Recipient email addresses
            subject: Email subject
            body: Email body (text or HTML)
            html: Whether body is HTML
            attachments: File attachments
        """
        if not self.connected:
            logger.warning("Email service not connected")
            return False
        
        # Mock send (replace with actual SMTP)
        logger.info(f"Sending email to {', '.join(to)}")
        logger.info(f"Subject: {subject}")
        logger.debug(f"Body: {body[:100]}...")
        
        return True
    
    def send_alert_email(
        self,
        to: List[str],
        alert_type: str,
        title: str,
        description: str,
        severity: str = "info"
    ) -> bool:
        """Send alert email"""
        subject = f"[{severity.upper()}] {title}"
        
        body = f"""
        <html>
        <body>
            <h2>{title}</h2>
            <p><strong>Alert Type:</strong> {alert_type}</p>
            <p><strong>Severity:</strong> {severity.upper()}</p>
            <p><strong>Description:</strong></p>
            <p>{description}</p>
            <hr>
            <p><small>由智投发送于 {datetime.now().isoformat()}</small></p>
        </body>
        </html>
        """
        
        return self.send_email(to, subject, body, html=True)
    
    def send_report_email(
        self,
        to: List[str],
        report_title: str,
        report_content: str,
        attachments: Optional[List[Dict]] = None
    ) -> bool:
        """Send report email"""
        subject = f"Report: {report_title}"
        
        body = f"""
        <html>
        <body>
            <h2>{report_title}</h2>
            {report_content}
            <hr>
            <p><small>由智投生成于 {datetime.now().isoformat()}</small></p>
        </body>
        </html>
        """
        
        return self.send_email(to, subject, body, html=True, attachments=attachments)


class WebhookIntegration:
    """Generic webhook integration"""
    
    def __init__(self):
        self.webhooks: Dict[str, Dict] = {}
    
    def register_webhook(
        self,
        webhook_id: str,
        url: str,
        events: List[str],
        headers: Optional[Dict] = None,
        retry_count: int = 3
    ):
        """Register a webhook"""
        self.webhooks[webhook_id] = {
            "url": url,
            "events": events,
            "headers": headers or {},
            "retry_count": retry_count,
            "enabled": True,
            "created_at": datetime.now()
        }
        
        logger.info(f"Registered webhook: {webhook_id} for events: {events}")
    
    def trigger_webhook(
        self,
        event_type: str,
        payload: Dict
    ) -> Dict[str, bool]:
        """
        Trigger webhooks for an event
        
        Args:
            event_type: Event type (e.g., "visibility_alert", "experiment_completed")
            payload: Event payload
        
        Returns:
            Dict of webhook_id -> success status
        """
        results = {}
        
        for webhook_id, config in self.webhooks.items():
            if not config["enabled"]:
                continue
            
            if event_type not in config["events"]:
                continue
            
            # Trigger webhook
            success = self._send_webhook(
                config["url"],
                payload,
                config["headers"],
                config["retry_count"]
            )
            
            results[webhook_id] = success
        
        return results
    
    def _send_webhook(
        self,
        url: str,
        payload: Dict,
        headers: Dict,
        retry_count: int
    ) -> bool:
        """Send webhook with retry logic"""
        # Mock send (replace with actual HTTP POST)
        logger.info(f"Sending webhook to {url}")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Simulate success
        return True


class ReportAutomation:
    """Automated report generation and distribution"""
    
    def __init__(self):
        self.scheduled_reports: Dict[str, Dict] = {}
    
    def schedule_report(
        self,
        report_id: str,
        report_type: str,
        frequency: str,  # daily, weekly, monthly
        recipients: List[str],
        delivery_method: str = "email",  # email, slack
        config: Optional[Dict] = None
    ):
        """Schedule automated report"""
        self.scheduled_reports[report_id] = {
            "report_type": report_type,
            "frequency": frequency,
            "recipients": recipients,
            "delivery_method": delivery_method,
            "config": config or {},
            "enabled": True,
            "created_at": datetime.now(),
            "last_run": None
        }
        
        logger.info(f"Scheduled {frequency} {report_type} report: {report_id}")
    
    def generate_report(
        self,
        report_type: str,
        data: Dict,
        format: str = "html"
    ) -> str:
        """
        Generate report content
        
        Args:
            report_type: Type of report (visibility, roi, experiment)
            data: Report data
            format: Output format (html, pdf, excel)
        """
        if report_type == "visibility":
            return self._generate_visibility_report(data, format)
        elif report_type == "roi":
            return self._generate_roi_report(data, format)
        elif report_type == "experiment":
            return self._generate_experiment_report(data, format)
        else:
            return f"<h2>Report: {report_type}</h2><pre>{json.dumps(data, indent=2)}</pre>"
    
    def _generate_visibility_report(self, data: Dict, format: str) -> str:
        """Generate visibility report"""
        html = f"""
        <h2>Visibility Report</h2>
        <p><strong>Period:</strong> {data.get('period', 'N/A')}</p>
        <h3>Overall Metrics</h3>
        <ul>
            <li>Overall Score: {data.get('overall_score', 0):.2f}</li>
            <li>Mention Rate: {data.get('mention_rate', 0):.2f}%</li>
            <li>Position Score: {data.get('position_score', 0):.2f}</li>
            <li>Trend: {data.get('trend', 0):.2f}%</li>
        </ul>
        <h3>Top Performing Engines</h3>
        <ul>
        """
        
        for engine in data.get('top_engines', []):
            html += f"<li>{engine['name']}: {engine['score']:.2f}</li>"
        
        html += "</ul>"
        
        return html
    
    def _generate_roi_report(self, data: Dict, format: str) -> str:
        """Generate ROI report"""
        html = f"""
        <h2>ROI Report</h2>
        <p><strong>Period:</strong> {data.get('period', 'N/A')}</p>
        <h3>Financial Metrics</h3>
        <ul>
            <li>Total Investment: ${data.get('investment', 0):,.2f}</li>
            <li>Total Benefit: ${data.get('benefit', 0):,.2f}</li>
            <li>Net Profit: ${data.get('net_profit', 0):,.2f}</li>
            <li>ROI: {data.get('roi_percentage', 0):.2f}%</li>
        </ul>
        <h3>Business Impact</h3>
        <ul>
            <li>Revenue Increase: ${data.get('revenue_increase', 0):,.2f}</li>
            <li>Leads Increase: {data.get('leads_increase', 0)}</li>
            <li>Traffic Increase: {data.get('traffic_increase', 0)}</li>
        </ul>
        """
        
        return html
    
    def _generate_experiment_report(self, data: Dict, format: str) -> str:
        """Generate experiment report"""
        html = f"""
        <h2>Experiment Report: {data.get('name', 'N/A')}</h2>
        <p><strong>Status:</strong> {data.get('status', 'N/A')}</p>
        <h3>Results</h3>
        <ul>
            <li>Treatment Effect (ATE): {data.get('ate', 0):.4f}</li>
            <li>P-value: {data.get('p_value', 0):.4f}</li>
            <li>Significant: {'Yes' if data.get('is_significant', False) else 'No'}</li>
            <li>Effect Size: {data.get('effect_size', 'N/A')}</li>
        </ul>
        """
        
        return html


# Global instances
slack_integration = SlackIntegration()
email_notification = EmailNotification()
webhook_integration = WebhookIntegration()
report_automation = ReportAutomation()
