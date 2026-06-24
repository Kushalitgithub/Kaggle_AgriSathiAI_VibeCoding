import re
from security.audit_logger import log_event

# Common prompt injection pattern signatures
PROMPT_INJECTION_PATTERNS = [
    r"(?i)ignore\s+(all\s+)?(previous\s+)?instructions",
    r"(?i)system\s+override",
    r"(?i)you\s+are\s+now\s+a\s+developer",
    r"(?i)jailbreak",
    r"(?i)forget\s+(what\s+you\s+were\s+told|your\s+system\s+prompt)",
    r"(?i)into\s+developer\s+mode",
    r"(?i)disregard\s+the\s+instructions",
    r"(?i)prompt\s+leak",
    r"(?i)reveal\s+(your\s+)?instructions",
    r"(?i)dan\s+mode"
]

def check_prompt_injection(user_input: str, user: str, role: str) -> tuple[bool, str]:
    """
    Checks user text input for injection signatures.
    Returns (is_safe, message_or_sanitized_text).
    """
    if not user_input:
        return True, ""
    
    # Check patterns
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, user_input):
            log_event(
                user=user,
                role=role,
                action="PROMPT_INJECTION_DETECTED",
                details=f"Prompt injection pattern match on string: '{user_input[:100]}'",
                status="BLOCKED"
            )
            return False, "Warning: Input blocked due to detected prompt injection attempt."
            
    # Basic HTML tag stripping to prevent markdown rendering issues or script injection
    cleaned_input = re.sub(r"<[^>]*>", "", user_input)
    
    return True, cleaned_input

def validate_image_upload(file_name: str, file_size_bytes: int, user: str, role: str) -> tuple[bool, str]:
    """
    Validates uploaded image type and file size (limit to 5MB).
    """
    MAX_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    
    # Check extension
    dot_idx = file_name.rfind(".")
    if dot_idx == -1:
        log_event(user=user, role=role, action="FILE_UPLOAD_FAILED", details=f"Rejected file {file_name} (no extension)", status="FAILED")
        return False, "File has no valid extension."
        
    ext = file_name[dot_idx:].lower()
    if ext not in ALLOWED_EXTENSIONS:
        log_event(user=user, role=role, action="FILE_UPLOAD_FAILED", details=f"Rejected file {file_name} (unsupported extension {ext})", status="FAILED")
        return False, f"Unsupported file type. Allowed formats: PNG, JPG, JPEG, WEBP."
        
    # Check size
    if file_size_bytes > MAX_SIZE:
        log_event(user=user, role=role, action="FILE_UPLOAD_FAILED", details=f"Rejected file {file_name} (size {file_size_bytes} bytes exceeds 5MB)", status="FAILED")
        return False, "File size exceeds the 5MB limit."
        
    log_event(user=user, role=role, action="FILE_UPLOAD_SUCCESS", details=f"Successfully validated and uploaded {file_name}", status="SUCCESS")
    return True, "File is valid."
