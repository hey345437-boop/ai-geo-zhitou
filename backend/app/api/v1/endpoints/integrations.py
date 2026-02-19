"""
Workflow & Integration Hub API Endpoints

Provides endpoints for managing integrations, notifications, and automated workflows.
"""

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

from app.services.workflow_integration import (
    SlackIntegration,
    EmailNotification,
    WebhookIntegration,
    ReportAutomation,
    IntegrationType,
    IntegrationConfig
)

router = APIRouter()

# Initialize services
slack_integration = SlackIntegration()
email_notification = EmailNotification()
webhook_integration = WebhookIntegration()
report_automation = ReportAutomation()


# Request/Response Models
class SlackConfigRequest(BaseModel):
    """Request model for Slack configuration"""
    webhook_url: str = Field(..., description="Slack webhook URL")
    channel: str = Field(..., description="Default Slack channel")
    username: Optional[str] = Field("智投", description="Bot username")
    icon_emoji: Optional[str] = Field(":chart_with_upwards_trend:", description="Bot icon")


class EmailConfigRequest(BaseModel):
    """Request model for email configuration"""
    smtp_host: str
    smtp_port: int = Field(587, ge=1, le=65535)
    smtp_user: str
    smtp_password: str
    from_email: EmailStr
    from_name: Optional[str] = "智投"


class WebhookConfigRequest(BaseModel):
    """Request model for webhook configuration"""
    url: str = Field(..., description="Webhook URL")
    method: str = Field("POST", description="HTTP method")
    headers: Optional[Dict[str, str]] = Field(default_factory=dict)
    auth_type: Optional[str] = Field(None, description="Authentication type (bearer, basic)")
    auth_credentials: Optional[Dict[str, str]] = Field(default_factory=dict)


class NotificationRequest(BaseModel):
    """Request model for sending notifications"""
    channel: str = Field(..., description="Notification channel (slack, email, webhook)")
    title: str
    message: str
    priority: Optional[str] = Field("normal", description="Priority level (low, normal, high, urgent)")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    recipients: Optional[List[str]] = Field(None, description="Email recipients or Slack channels")


class ReportScheduleRequest(BaseModel):
    """Request model for scheduling reports"""
    report_type: str = Field(..., description="Type of report (visibility, roi, attribution)")
    schedule: str = Field(..., description="Cron expression for schedule")
    format: str = Field("pdf", description="Report format (pdf, excel, html)")
    recipients: List[str] = Field(..., description="Email addresses or Slack channels")
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict)


class WebhookEventRequest(BaseModel):
    """Request model for webhook event subscription"""
    webhook_id: str
    event_types: List[str] = Field(..., description="Event types to subscribe to")
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict)


class IntegrationResponse(BaseModel):
    """Response model for integration configuration"""
    integration_id: str
    integration_type: str
    status: str
    created_at: datetime
    last_used: Optional[datetime]
    config_summary: Dict[str, Any]


class NotificationResponse(BaseModel):
    """Response model for notification"""
    notification_id: str
    channel: str
    status: str
    sent_at: datetime
    error: Optional[str]


class ReportScheduleResponse(BaseModel):
    """Response model for report schedule"""
    schedule_id: str
    report_type: str
    schedule: str
    next_run: datetime
    status: str
    created_at: datetime


class WebhookLogResponse(BaseModel):
    """Response model for webhook log"""
    log_id: str
    webhook_id: str
    event_type: str
    status_code: int
    response_time_ms: float
    timestamp: datetime
    error: Optional[str]


@router.post("/integrations/slack", response_model=IntegrationResponse, status_code=201)
async def configure_slack(request: SlackConfigRequest):
    """
    Configure Slack integration
    
    Sets up Slack webhook for sending notifications and alerts.
    """
    try:
        config = workflow_manager.configure_slack(
            webhook_url=request.webhook_url,
            channel=request.channel,
            username=request.username,
            icon_emoji=request.icon_emoji
        )
        
        return IntegrationResponse(
            integration_id=config["integration_id"],
            integration_type="slack",
            status="active",
            created_at=datetime.utcnow(),
            last_used=None,
            config_summary={
                "channel": request.channel,
                "username": request.username
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to configure Slack: {str(e)}")


@router.post("/integrations/email", response_model=IntegrationResponse, status_code=201)
async def configure_email(request: EmailConfigRequest):
    """
    Configure email integration
    
    Sets up SMTP server for sending email notifications and reports.
    """
    try:
        config = workflow_manager.configure_email(
            smtp_host=request.smtp_host,
            smtp_port=request.smtp_port,
            smtp_user=request.smtp_user,
            smtp_password=request.smtp_password,
            from_email=request.from_email,
            from_name=request.from_name
        )
        
        return IntegrationResponse(
            integration_id=config["integration_id"],
            integration_type="email",
            status="active",
            created_at=datetime.utcnow(),
            last_used=None,
            config_summary={
                "smtp_host": request.smtp_host,
                "from_email": request.from_email
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to configure email: {str(e)}")


@router.post("/integrations/webhook", response_model=IntegrationResponse, status_code=201)
async def configure_webhook(request: WebhookConfigRequest):
    """
    Configure webhook integration
    
    Sets up webhook endpoint for sending event notifications.
    """
    try:
        config = workflow_manager.configure_webhook(
            url=request.url,
            method=request.method,
            headers=request.headers,
            auth_type=request.auth_type,
            auth_credentials=request.auth_credentials
        )
        
        return IntegrationResponse(
            integration_id=config["webhook_id"],
            integration_type="webhook",
            status="active",
            created_at=datetime.utcnow(),
            last_used=None,
            config_summary={
                "url": request.url,
                "method": request.method
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to configure webhook: {str(e)}")


@router.get("/integrations", response_model=List[IntegrationResponse])
async def list_integrations():
    """
    List all configured integrations
    
    Returns all active integrations and their status.
    """
    # In production, fetch from database
    return [
        IntegrationResponse(
            integration_id="slack_001",
            integration_type="slack",
            status="active",
            created_at=datetime.utcnow(),
            last_used=datetime.utcnow(),
            config_summary={"channel": "#geo-alerts"}
        ),
        IntegrationResponse(
            integration_id="email_001",
            integration_type="email",
            status="active",
            created_at=datetime.utcnow(),
            last_used=datetime.utcnow(),
            config_summary={"smtp_host": "smtp.gmail.com"}
        )
    ]


@router.delete("/integrations/{integration_id}", status_code=204)
async def delete_integration(integration_id: str):
    """
    Delete an integration
    
    Removes an integration configuration from the system.
    """
    # In production, delete from database
    return None


@router.post("/notifications/send", response_model=NotificationResponse)
async def send_notification(request: NotificationRequest, background_tasks: BackgroundTasks):
    """
    Send a notification
    
    Sends a notification through the specified channel (Slack, email, or webhook).
    """
    try:
        channel = NotificationChannel(request.channel)
        
        # Send notification in background
        notification_id = f"notif_{datetime.utcnow().timestamp()}"
        
        result = workflow_manager.send_notification(
            channel=channel,
            title=request.title,
            message=request.message,
            priority=request.priority,
            metadata=request.metadata,
            recipients=request.recipients
        )
        
        return NotificationResponse(
            notification_id=notification_id,
            channel=request.channel,
            status="sent" if result["success"] else "failed",
            sent_at=datetime.utcnow(),
            error=result.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")


@router.get("/notifications/history", response_model=List[NotificationResponse])
async def get_notification_history(
    limit: int = Query(50, ge=1, le=100),
    channel: Optional[str] = Query(None, description="Filter by channel")
):
    """
    Get notification history
    
    Returns recent notifications sent through the system.
    """
    # In production, fetch from database
    return [
        NotificationResponse(
            notification_id=f"notif_{i}",
            channel=channel or "slack",
            status="sent",
            sent_at=datetime.utcnow(),
            error=None
        )
        for i in range(min(limit, 10))
    ]


@router.post("/reports/schedule", response_model=ReportScheduleResponse, status_code=201)
async def schedule_report(request: ReportScheduleRequest):
    """
    Schedule automated report
    
    Creates a scheduled job to generate and send reports automatically.
    """
    try:
        report_format = ReportFormat(request.format)
        
        schedule = workflow_manager.schedule_report(
            report_type=request.report_type,
            schedule=request.schedule,
            format=report_format,
            recipients=request.recipients,
            filters=request.filters
        )
        
        return ReportScheduleResponse(
            schedule_id=schedule["schedule_id"],
            report_type=request.report_type,
            schedule=request.schedule,
            next_run=schedule["next_run"],
            status="active",
            created_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to schedule report: {str(e)}")


@router.get("/reports/schedules", response_model=List[ReportScheduleResponse])
async def list_report_schedules():
    """
    List all report schedules
    
    Returns all configured automated report schedules.
    """
    # In production, fetch from database
    return [
        ReportScheduleResponse(
            schedule_id="sched_001",
            report_type="visibility",
            schedule="0 9 * * 1",  # Every Monday at 9 AM
            next_run=datetime.utcnow(),
            status="active",
            created_at=datetime.utcnow()
        )
    ]


@router.delete("/reports/schedules/{schedule_id}", status_code=204)
async def delete_report_schedule(schedule_id: str):
    """
    Delete a report schedule
    
    Removes an automated report schedule.
    """
    # In production, delete from database
    return None


@router.post("/reports/generate")
async def generate_report(
    report_type: str = Query(..., description="Type of report"),
    format: str = Query("pdf", description="Report format"),
    background_tasks: BackgroundTasks = None
):
    """
    Generate report on-demand
    
    Generates a report immediately and returns download URL.
    """
    try:
        report_format = ReportFormat(format)
        
        # Generate report in background
        report = workflow_manager.generate_report(
            report_type=report_type,
            format=report_format,
            filters={}
        )
        
        return {
            "report_id": report["report_id"],
            "report_type": report_type,
            "format": format,
            "status": "generating",
            "download_url": f"/api/v1/reports/download/{report['report_id']}",
            "estimated_completion": datetime.utcnow()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@router.post("/webhooks/{webhook_id}/subscribe", response_model=Dict[str, Any])
async def subscribe_webhook_events(webhook_id: str, request: WebhookEventRequest):
    """
    Subscribe webhook to events
    
    Configures which events should trigger the webhook.
    """
    try:
        event_types = [EventType(et) for et in request.event_types]
        
        subscription = workflow_manager.subscribe_webhook(
            webhook_id=webhook_id,
            event_types=event_types,
            filters=request.filters
        )
        
        return {
            "webhook_id": webhook_id,
            "subscribed_events": request.event_types,
            "status": "active",
            "created_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to subscribe webhook: {str(e)}")


@router.get("/webhooks/{webhook_id}/logs", response_model=List[WebhookLogResponse])
async def get_webhook_logs(
    webhook_id: str,
    limit: int = Query(50, ge=1, le=100)
):
    """
    Get webhook execution logs
    
    Returns recent webhook call logs for debugging and monitoring.
    """
    # In production, fetch from database
    return [
        WebhookLogResponse(
            log_id=f"log_{i}",
            webhook_id=webhook_id,
            event_type="visibility_change",
            status_code=200,
            response_time_ms=125.5,
            timestamp=datetime.utcnow(),
            error=None
        )
        for i in range(min(limit, 10))
    ]


@router.post("/webhooks/{webhook_id}/test")
async def test_webhook(webhook_id: str):
    """
    Test webhook configuration
    
    Sends a test payload to verify webhook is working correctly.
    """
    try:
        result = workflow_manager.test_webhook(webhook_id)
        
        return {
            "webhook_id": webhook_id,
            "status": "success" if result["success"] else "failed",
            "status_code": result.get("status_code"),
            "response_time_ms": result.get("response_time_ms"),
            "error": result.get("error"),
            "tested_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to test webhook: {str(e)}")
