import config
from utils.logger import logger

def should_skip_email(sender: str, subject: str) -> tuple[bool, str]:
    """
    Checks if an email should be skipped based on config rules.
    Returns (True, "reason") if it should be skipped, else (False, "").
    """
    if not sender and not subject:
        return False, ""
        
    sender_lower = sender.lower()
    subject_lower = subject.lower()
    
    for skip_sender in config.SKIP_SENDERS:
        if skip_sender.lower() in sender_lower:
            logger.info(f"Skipping email due to sender filter: '{skip_sender}' matched in '{sender}'", to_ui=False)
            return True, f"Sender matched filter: {skip_sender}"
            
    for skip_subject in config.SKIP_SUBJECTS:
        if skip_subject.lower() in subject_lower:
            logger.info(f"Skipping email due to subject filter: '{skip_subject}' matched in '{subject}'", to_ui=False)
            return True, f"Subject matched filter: {skip_subject}"
            
    return False, ""
