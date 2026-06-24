from security.auth import has_permission
from security.audit_logger import log_event

def verify_tool_execution(tool_name: str, user: str, role: str, required_role: str, user_consent_given: bool = True) -> tuple[bool, str]:
    """
    Validates if a tool can be run based on:
    1. User's role permissions (RBAC)
    2. Explicit user consent/approval for write actions
    
    Returns (allowed, message).
    """
    # 1. RBAC check
    if not has_permission(role, required_role):
        log_event(
            user=user,
            role=role,
            action="UNAUTHORIZED_TOOL_BLOCKED",
            details=f"Blocked attempt to execute tool '{tool_name}' (requires {required_role} role)",
            status="BLOCKED"
        )
        return False, f"Unauthorized: Executing '{tool_name}' requires '{required_role}' privilege."
        
    # 2. Consent check for write operations
    is_write_action = tool_name.startswith("write_") or tool_name.startswith("update_") or "schedule" in tool_name or "plan" in tool_name
    if is_write_action and not user_consent_given:
        log_event(
            user=user,
            role=role,
            action="TOOL_EXECUTION_BLOCKED_NO_CONSENT",
            details=f"Blocked write tool '{tool_name}' because user consent was not granted.",
            status="BLOCKED"
        )
        return False, f"Blocked: Tool '{tool_name}' requires explicit user consent to execute."
        
    log_event(
        user=user,
        role=role,
        action="TOOL_EXECUTION_ALLOWED",
        details=f"User {user} ({role}) executed tool '{tool_name}' successfully.",
        status="SUCCESS"
    )
    return True, "Authorized."
