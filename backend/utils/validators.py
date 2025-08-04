from typing import Any, Dict
from datetime import datetime
import re


class ValidationError(Exception):
    """Custom validation error"""
    pass


def validate_username(username: str) -> bool:
    """Validate username format following business rules"""
    if not username or len(username) < 3 or len(username) > 50:
        return False
    
    # Username can only contain alphanumeric characters and underscores
    pattern = r'^[a-zA-Z0-9_]+$'
    return bool(re.match(pattern, username))


def validate_password(password: str) -> bool:
    """Validate password strength"""
    if not password or len(password) < 6:
        return False
    
    # Password should contain at least one letter and one number
    has_letter = bool(re.search(r'[a-zA-Z]', password))
    has_number = bool(re.search(r'\d', password))
    
    return has_letter and has_number


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_group(group: str) -> bool:
    """Validate group name"""
    valid_groups = ["Group_A", "Group_B"]
    return group in valid_groups


def sanitize_input(data: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not isinstance(data, str):
        return str(data)
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`']
    sanitized = data
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()


def format_user_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format and sanitize user data"""
    formatted_data = {}
    
    for key, value in user_data.items():
        if isinstance(value, str):
            formatted_data[key] = sanitize_input(value)
        elif isinstance(value, datetime):
            formatted_data[key] = value.isoformat()
        else:
            formatted_data[key] = value
    
    return formatted_data


def validate_user_registration_data(data: Dict[str, Any]) -> Dict[str, str]:
    """Validate user registration data and return errors if any"""
    errors = {}
    
    # Validate username
    if not validate_username(data.get('username', '')):
        errors['username'] = 'Username must be 3-50 characters long and contain only alphanumeric characters and underscores'
    
    # Validate password
    if not validate_password(data.get('password', '')):
        errors['password'] = 'Password must be at least 6 characters long and contain at least one letter and one number'
    
    # Validate email
    if not validate_email(data.get('email', '')):
        errors['email'] = 'Invalid email format'
    
    # Validate group
    if not validate_group(data.get('group', '')):
        errors['group'] = 'Invalid group. Must be either Group_A or Group_B'
    
    # Validate names
    if not data.get('first_name', '').strip():
        errors['first_name'] = 'First name is required'
    
    if not data.get('last_name', '').strip():
        errors['last_name'] = 'Last name is required'
    
    return errors
