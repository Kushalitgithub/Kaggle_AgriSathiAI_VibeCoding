import hashlib
from security.audit_logger import log_event

# Mock credentials mapping passcodes to roles
PASSCODE_MAP = {
    "1234": ("Farmer", "General farmer access to diagnostic tool and weather/market inquiries"),
    "5678": ("Advisor", "Agricultural consultant access with authority to generate advanced reports"),
    "9999": ("Admin", "System administrator access with access to audit logs and security settings")
}

def authenticate_user(passcode: str) -> tuple[bool, str, str]:
    """
    Verifies user passcode and returns (is_authenticated, role, description).
    """
    if not passcode:
        return False, "", "Please enter a passcode."
    
    if passcode in PASSCODE_MAP:
        role, desc = PASSCODE_MAP[passcode]
        log_event(user=f"user_{passcode}", role=role, action="USER_LOGIN", details=f"Successful login as {role}", status="SUCCESS")
        return True, role, desc
    
    log_event(user="unknown", role="guest", action="USER_LOGIN_FAILED", details=f"Failed login attempt with passcode {passcode}", status="FAILED")
    return False, "", "Invalid passcode. Access Denied."

def has_permission(user_role: str, required_role: str) -> bool:
    """
    Simple RBAC helper:
    Admin can do everything.
    Advisor can do Advisor and Farmer actions.
    Farmer can only do Farmer actions.
    """
    role_hierarchy = {
        "Farmer": 1,
        "Advisor": 2,
        "Admin": 3
    }
    
    user_level = role_hierarchy.get(user_role, 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    return user_level >= required_level
