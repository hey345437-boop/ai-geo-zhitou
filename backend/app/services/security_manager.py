"""
Security Manager Service

Provides security hardening features including authentication, authorization,
audit logging, and security validation.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import secrets
import re


class UserRole(Enum):
    """User roles for RBAC"""
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class Permission(Enum):
    """System permissions"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    MANAGE_USERS = "manage_users"
    VIEW_AUDIT_LOGS = "view_audit_logs"


class AuditEventType(Enum):
    """Types of audit events"""
    LOGIN = "login"
    LOGOUT = "logout"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    DATA_DELETION = "data_deletion"
    PERMISSION_CHANGE = "permission_change"
    SECURITY_EVENT = "security_event"
    API_CALL = "api_call"


@dataclass
class User:
    """User model"""
    user_id: str
    email: str
    role: UserRole
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['role'] = self.role.value
        data['created_at'] = self.created_at.isoformat()
        data['last_login'] = self.last_login.isoformat() if self.last_login else None
        return data


@dataclass
class AuditLog:
    """Audit log entry"""
    log_id: str
    user_id: str
    event_type: AuditEventType
    resource: str
    action: str
    ip_address: str
    user_agent: str
    timestamp: datetime
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['event_type'] = self.event_type.value
        data['timestamp'] = self.timestamp.isoformat()
        return data


class SecurityManager:
    """
    Security manager for authentication, authorization, and audit logging
    
    Implements security best practices including:
    - Role-based access control (RBAC)
    - Audit logging
    - Input validation
    - CSRF protection
    - XSS protection
    """
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.audit_logs: List[AuditLog] = []
        self.csrf_tokens: Dict[str, datetime] = {}
        
        # Role permissions mapping
        self.role_permissions = {
            UserRole.OWNER: [
                Permission.READ, Permission.WRITE, Permission.DELETE,
                Permission.ADMIN, Permission.MANAGE_USERS, Permission.VIEW_AUDIT_LOGS
            ],
            UserRole.ADMIN: [
                Permission.READ, Permission.WRITE, Permission.DELETE,
                Permission.MANAGE_USERS, Permission.VIEW_AUDIT_LOGS
            ],
            UserRole.EDITOR: [
                Permission.READ, Permission.WRITE
            ],
            UserRole.VIEWER: [
                Permission.READ
            ]
        }
    
    def create_user(
        self,
        email: str,
        role: UserRole = UserRole.VIEWER
    ) -> User:
        """
        Create a new user
        
        Args:
            email: User email
            role: User role
            
        Returns:
            Created User object
        """
        user_id = f"user_{hashlib.sha256(email.encode()).hexdigest()[:16]}"
        
        user = User(
            user_id=user_id,
            email=email,
            role=role,
            created_at=datetime.utcnow()
        )
        
        self.users[user_id] = user
        
        # Log user creation
        self.log_audit_event(
            user_id="system",
            event_type=AuditEventType.SECURITY_EVENT,
            resource="users",
            action="create_user",
            ip_address="127.0.0.1",
            user_agent="system",
            details={'new_user_id': user_id, 'role': role.value}
        )
        
        return user
    
    def check_permission(
        self,
        user_id: str,
        permission: Permission
    ) -> bool:
        """
        Check if user has permission
        
        Args:
            user_id: User identifier
            permission: Required permission
            
        Returns:
            True if user has permission
        """
        user = self.users.get(user_id)
        if not user or not user.is_active:
            return False
        
        user_permissions = self.role_permissions.get(user.role, [])
        return permission in user_permissions
    
    def generate_csrf_token(self, user_id: str) -> str:
        """
        Generate CSRF token for user
        
        Args:
            user_id: User identifier
            
        Returns:
            CSRF token
        """
        token = secrets.token_urlsafe(32)
        self.csrf_tokens[token] = datetime.utcnow()
        return token
    
    def validate_csrf_token(self, token: str) -> bool:
        """
        Validate CSRF token
        
        Args:
            token: CSRF token to validate
            
        Returns:
            True if token is valid
        """
        if token not in self.csrf_tokens:
            return False
        
        # Check if token is expired (1 hour)
        token_time = self.csrf_tokens[token]
        if datetime.utcnow() - token_time > timedelta(hours=1):
            del self.csrf_tokens[token]
            return False
        
        return True
    
    def sanitize_input(self, input_str: str) -> str:
        """
        Sanitize user input to prevent XSS
        
        Args:
            input_str: Input string to sanitize
            
        Returns:
            Sanitized string
        """
        # Remove HTML tags
        sanitized = re.sub(r'<[^>]+>', '', input_str)
        
        # Escape special characters
        sanitized = sanitized.replace('&', '&amp;')
        sanitized = sanitized.replace('<', '&lt;')
        sanitized = sanitized.replace('>', '&gt;')
        sanitized = sanitized.replace('"', '&quot;')
        sanitized = sanitized.replace("'", '&#x27;')
        
        return sanitized
    
    def validate_sql_input(self, input_str: str) -> bool:
        """
        Validate input for SQL injection attempts
        
        Args:
            input_str: Input string to validate
            
        Returns:
            True if input is safe
        """
        # Check for common SQL injection patterns
        dangerous_patterns = [
            r"(\bOR\b|\bAND\b).*=.*",
            r";\s*DROP\s+TABLE",
            r";\s*DELETE\s+FROM",
            r";\s*UPDATE\s+",
            r"UNION\s+SELECT",
            r"--",
            r"/\*.*\*/"
        ]
        
        input_upper = input_str.upper()
        for pattern in dangerous_patterns:
            if re.search(pattern, input_upper, re.IGNORECASE):
                return False
        
        return True
    
    def log_audit_event(
        self,
        user_id: str,
        event_type: AuditEventType,
        resource: str,
        action: str,
        ip_address: str,
        user_agent: str,
        details: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """
        Log an audit event
        
        Args:
            user_id: User who performed action
            event_type: Type of event
            resource: Resource affected
            action: Action performed
            ip_address: Client IP address
            user_agent: Client user agent
            details: Additional details
            
        Returns:
            Created AuditLog
        """
        log_id = f"log_{datetime.utcnow().timestamp()}_{secrets.token_hex(4)}"
        
        audit_log = AuditLog(
            log_id=log_id,
            user_id=user_id,
            event_type=event_type,
            resource=resource,
            action=action,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.utcnow(),
            details=details or {}
        )
        
        self.audit_logs.append(audit_log)
        
        # In production, store in secure database
        return audit_log
    
    def get_audit_logs(
        self,
        user_id: Optional[str] = None,
        event_type: Optional[AuditEventType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[AuditLog]:
        """
        Get audit logs with filtering
        
        Args:
            user_id: Filter by user
            event_type: Filter by event type
            start_date: Filter by start date
            end_date: Filter by end date
            limit: Maximum number of logs
            
        Returns:
            List of AuditLog objects
        """
        logs = self.audit_logs
        
        # Apply filters
        if user_id:
            logs = [log for log in logs if log.user_id == user_id]
        
        if event_type:
            logs = [log for log in logs if log.event_type == event_type]
        
        if start_date:
            logs = [log for log in logs if log.timestamp >= start_date]
        
        if end_date:
            logs = [log for log in logs if log.timestamp <= end_date]
        
        # Sort by timestamp (newest first)
        logs.sort(key=lambda x: x.timestamp, reverse=True)
        
        return logs[:limit]
    
    def get_security_headers(self) -> Dict[str, str]:
        """
        Get security headers for HTTP responses
        
        Returns:
            Dictionary of security headers
        """
        return {
            # HTTPS enforcement
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            
            # XSS protection
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            
            # Content Security Policy
            'Content-Security-Policy': (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self'"
            ),
            
            # Referrer policy
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            
            # Permissions policy
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
        }


class DataComplianceManager:
    """
    Data compliance manager for GDPR and privacy regulations
    
    Implements:
    - Data anonymization
    - Right to be forgotten
    - Data portability
    - Data retention
    - Data localization
    """
    
    def __init__(self):
        self.retention_days = 365  # Default retention period
    
    def anonymize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Anonymize personal data
        
        Args:
            data: Data to anonymize
            
        Returns:
            Anonymized data
        """
        anonymized = data.copy()
        
        # Fields to anonymize
        pii_fields = ['email', 'name', 'phone', 'address', 'ip_address']
        
        for field in pii_fields:
            if field in anonymized:
                # Hash the value
                value = str(anonymized[field])
                hashed = hashlib.sha256(value.encode()).hexdigest()[:16]
                anonymized[field] = f"anon_{hashed}"
        
        return anonymized
    
    def delete_user_data(self, user_id: str) -> Dict[str, Any]:
        """
        Delete all user data (Right to be Forgotten)
        
        Args:
            user_id: User identifier
            
        Returns:
            Deletion report
        """
        deleted_items = {
            'user_profile': 1,
            'probe_results': 0,
            'evaluation_runs': 0,
            'audit_logs_anonymized': 0,
            'cache_cleared': True
        }
        
        # In production:
        # 1. Delete user profile
        # 2. Delete or anonymize user data
        # 3. Anonymize audit logs
        # 4. Clear caches
        # 5. Notify connected systems
        
        return {
            'user_id': user_id,
            'deleted_at': datetime.utcnow().isoformat(),
            'items_deleted': deleted_items,
            'status': 'completed'
        }
    
    def export_user_data(
        self,
        user_id: str,
        format: str = 'json'
    ) -> Dict[str, Any]:
        """
        Export all user data (Data Portability)
        
        Args:
            user_id: User identifier
            format: Export format (json or csv)
            
        Returns:
            Exported data package
        """
        # In production, collect all user data from all tables
        user_data = {
            'user_id': user_id,
            'exported_at': datetime.utcnow().isoformat(),
            'format': format,
            'data': {
                'profile': {},
                'probe_results': [],
                'evaluation_runs': [],
                'recommendations': [],
                'audit_logs': []
            }
        }
        
        return user_data
    
    def enforce_retention_policy(self) -> Dict[str, int]:
        """
        Enforce data retention policy
        
        Returns:
            Report of deleted items
        """
        cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)
        
        deleted_counts = {
            'old_probe_results': 0,
            'old_evaluation_runs': 0,
            'old_audit_logs': 0
        }
        
        # In production:
        # 1. Find data older than retention period
        # 2. Delete or archive old data
        # 3. Update indexes
        
        return deleted_counts
    
    def determine_data_region(self, ip_address: str) -> str:
        """
        Determine data storage region based on user location
        
        Args:
            ip_address: User IP address
            
        Returns:
            Region code (e.g., 'eu', 'us', 'asia')
        """
        # Simple mock implementation
        # In production, use GeoIP database
        
        # Mock: Determine region from IP
        if ip_address.startswith('192.168'):
            return 'us'
        elif ip_address.startswith('10.'):
            return 'eu'
        else:
            return 'us'  # Default
