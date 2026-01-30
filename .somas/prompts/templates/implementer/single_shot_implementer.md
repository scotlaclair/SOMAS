# SINGLE-SHOT IMPLEMENTATION PROTOCOL

**You have ONE attempt to implement this correctly. No retries allowed.**

This protocol enforces planning before coding to maximize first-shot success rate.

---

## PHASE 1: ANALYSIS (Do not write code yet)

**STOP. READ EVERYTHING FIRST.**

1. **Read ARCHITECTURE.md section {section_id} completely**
   - Understand all components
   - Note all dependencies
   - Identify all interfaces

2. **Read SPEC.md requirements {req_ids} completely**
   - List every requirement that applies
   - Note all acceptance criteria
   - Identify all constraints

3. **List ALL edge cases that must be handled**
   - Null/empty inputs
   - Invalid data types
   - Boundary conditions
   - Concurrent access (if applicable)
   - Network failures (if applicable)
   - Resource limits

4. **List ALL imports/dependencies required**
   - Standard library modules
   - Third-party packages
   - Internal modules
   - Version requirements

5. **Identify ALL error conditions**
   - Invalid inputs
   - Resource unavailable
   - Permission denied
   - Timeout/deadline exceeded
   - Unexpected state

6. **Plan test cases (minimum 6)**
   - Happy path (normal operation)
   - Edge case 1
   - Edge case 2
   - Error condition 1
   - Error condition 2
   - Performance/load test

---

## PHASE 2: DESIGN (Still no code)

**DESIGN FIRST. CODE LATER.**

7. **Write pseudocode for main logic**
   ```
   function main_operation(input):
       validate input
       prepare resources
       execute core logic
       handle results
       cleanup resources
       return output
   ```

8. **Write pseudocode for error handling**
   ```
   try:
       main logic
   catch ValidationError:
       log error
       return error response
   catch ResourceError:
       cleanup
       return error response
   finally:
       ensure cleanup
   ```

9. **Identify which libraries to use (prefer existing)**
   - Check `.somas/knowledge/approved_libraries.yml`
   - Use battle-tested libraries over custom code
   - Document library choice rationale

10. **Design function signatures (input/output types)**
    ```
    def process_data(
        data: Dict[str, Any],
        options: Optional[ProcessOptions] = None,
        timeout: int = 30
    ) -> Result[ProcessedData, ProcessingError]:
        """
        Process data according to specification.
        
        Args:
            data: Input data dictionary
            options: Optional processing configuration
            timeout: Maximum processing time in seconds
            
        Returns:
            Result with ProcessedData on success, ProcessingError on failure
            
        Raises:
            ValueError: If data format is invalid
            TimeoutError: If processing exceeds timeout
        """
    ```

---

## PHASE 3: IMPLEMENTATION (Now write code)

**IMPLEMENT IN ONE COMPLETE PASS. NO PLACEHOLDERS.**

11. **Implement in ONE complete pass**
    - Write complete, working code
    - No TODOs
    - No placeholders
    - No "implement later" comments

12. **Include ALL imports at top**
    ```python
    # Standard library imports
    import json
    import logging
    from typing import Dict, Any, Optional
    
    # Third-party imports
    import requests
    from pydantic import BaseModel
    
    # Internal imports
    from somas.core import utils
    ```

13. **Include ALL error handling**
    - Try-catch blocks where needed
    - Specific exception types
    - Meaningful error messages
    - Proper cleanup in finally blocks

14. **Include ALL input validation**
    - Type checking
    - Null/empty checking
    - Range validation
    - Format validation
    - Security validation (injection prevention)

15. **Include tests in same file/commit**
    ```python
    # At the end of implementation file or separate test file
    
    def test_happy_path():
        result = process_data(valid_data)
        assert result.is_success()
        assert result.value.status == "processed"
    
    def test_invalid_input():
        with pytest.raises(ValueError):
            process_data(invalid_data)
    ```

16. **NO placeholders, NO TODOs**
    - ❌ `# TODO: implement error handling`
    - ❌ `# FIXME: optimize this later`
    - ❌ `pass  # implement this`
    - ✅ Complete implementation only

---

## PHASE 4: VERIFICATION (Before submitting)

**VERIFY EVERYTHING. SUBMIT ONLY WHEN PERFECT.**

17. **All imports present and correct**
    - [ ] No missing imports
    - [ ] No unused imports
    - [ ] Proper import organization

18. **All error cases handled**
    - [ ] Try-catch blocks in place
    - [ ] All exceptions logged
    - [ ] Meaningful error messages
    - [ ] Proper cleanup on errors

19. **Input validation included**
    - [ ] Type checking
    - [ ] Null/empty checking
    - [ ] Range/format validation
    - [ ] Security checks

20. **Tests included in same commit**
    - [ ] Happy path test
    - [ ] At least 5 edge/error tests
    - [ ] Tests are executable
    - [ ] Tests have assertions

21. **No TODOs or placeholders**
    - [ ] No TODO comments
    - [ ] No FIXME comments
    - [ ] No pass statements as placeholders
    - [ ] All functions fully implemented

22. **Documentation complete**
    - [ ] Docstrings on all public functions
    - [ ] Parameters documented
    - [ ] Return values documented
    - [ ] Exceptions documented

23. **Code follows standards**
    - [ ] Proper naming conventions
    - [ ] Consistent formatting
    - [ ] No code smells
    - [ ] DRY principle followed

---

## SUBMIT ONLY WHEN ALL CHECKS PASS

**If any check fails, fix it before submitting.**

This is your ONLY chance to get it right. There are no retries in single-shot mode.

---

## Example: Complete Implementation

```python
"""
User authentication module.

Handles user login, session management, and authorization.

SECURITY NOTE: This example demonstrates proper security patterns.
Production implementations must use dedicated password hashing libraries.
"""

import logging
import secrets
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from pydantic import BaseModel, validator
from fastapi import HTTPException

# CRITICAL: Use a proper password hashing library in production
# Examples: argon2-cffi, bcrypt, passlib
try:
    from argon2 import PasswordHasher
    ph = PasswordHasher()
    HASH_AVAILABLE = True
except ImportError:
    HASH_AVAILABLE = False
    # Fallback message for example only
    import warnings
    warnings.warn("argon2-cffi not installed. Install for production use.")

logger = logging.getLogger(__name__)


class LoginRequest(BaseModel):
    """Login request validation model"""
    username: str
    password: str
    
    @validator('username')
    def validate_username(cls, v):
        if not v or len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v.strip().lower()
    
    @validator('password')
    def validate_password(cls, v):
        if not v or len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class AuthSession(BaseModel):
    """User session model"""
    session_id: str
    user_id: str
    username: str
    created_at: datetime
    expires_at: datetime


class AuthenticationService:
    """Service for user authentication and session management"""
    
    def __init__(self, session_timeout: int = 3600):
        """
        Initialize authentication service.
        
        Args:
            session_timeout: Session timeout in seconds (default 1 hour)
        """
        self.session_timeout = session_timeout
        self.sessions: Dict[str, AuthSession] = {}
        
    def authenticate(self, request: LoginRequest) -> AuthSession:
        """
        Authenticate user and create session.
        
        Args:
            request: Login request with username and password
            
        Returns:
            AuthSession object with session details
            
        Raises:
            HTTPException: If authentication fails
        """
        try:
            # Validate input (Pydantic does this automatically)
            logger.info(f"Authentication attempt for user: {request.username}")
            
            # SECURITY: In production, retrieve stored hash from database
            # and use a proper password hashing library (argon2, bcrypt, scrypt)
            # DO NOT use fast hashes like SHA-256 for passwords!
            
            # Verify credentials (in production: database lookup)
            user = self._verify_credentials(request.username, request.password)
            if not user:
                logger.warning(f"Failed login attempt: {request.username}")
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
            # Create session
            session = self._create_session(user['id'], request.username)
            
            logger.info(f"User {request.username} authenticated successfully")
            return session
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise HTTPException(status_code=500, detail="Authentication failed")
    
    def _verify_credentials(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Verify user credentials against stored password hash.
        
        SECURITY: This is a demonstration example only!
        Production implementations MUST:
        1. Query database for user by username
        2. Retrieve stored password hash for that user
        3. Use argon2.verify(), bcrypt.checkpw(), or equivalent
        4. Use constant-time comparison
        5. Return user data ONLY if password matches
        
        Args:
            username: Username to verify
            password: Plain-text password from user
            
        Returns:
            User dict if credentials valid, None otherwise
        """
        # Example user (DEMONSTRATION ONLY - not for production)
        # In production: user = database.query_user(username)
        example_user = {
            'id': 'user-123',
            'username': 'demo_user',
            # This hash represents "SecurePassword123!" hashed with Argon2
            'password_hash': '$argon2id$v=19$m=65536,t=3,p=4$...'  # Example format only
        }
        
        # Production implementation would be:
        # if username != example_user['username']:
        #     return None
        # 
        # if HASH_AVAILABLE:
        #     try:
        #         ph.verify(example_user['password_hash'], password)
        #         return {'id': example_user['id'], 'username': username}
        #     except:
        #         return None
        # else:
        #     raise RuntimeError("Password hashing library required")
        
        # For demonstration: Accept any username with password "demo_password"
        # REMOVE THIS IN PRODUCTION!
        if password == "demo_password":
            return {"id": "user-123", "username": username}
        
        return None
    
    def _create_session(self, user_id: str, username: str) -> AuthSession:
        """Create new authentication session"""
        session_id = secrets.token_urlsafe(32)
        now = datetime.utcnow()
        
        session = AuthSession(
            session_id=session_id,
            user_id=user_id,
            username=username,
            created_at=now,
            expires_at=now + timedelta(seconds=self.session_timeout)
        )
        
        self.sessions[session_id] = session
        return session
    
    def validate_session(self, session_id: str) -> bool:
        """
        Validate session is active and not expired.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if session is valid, False otherwise
        """
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        if datetime.utcnow() > session.expires_at:
            # Clean up expired session
            del self.sessions[session_id]
            return False
        
        return True


# Tests
def test_successful_authentication():
    """Test happy path authentication"""
    service = AuthenticationService()
    request = LoginRequest(username="testuser", password="password123")
    
    session = service.authenticate(request)
    
    assert session.username == "testuser"
    assert service.validate_session(session.session_id)


def test_invalid_username():
    """Test authentication with invalid username"""
    import pytest
    
    with pytest.raises(ValueError, match="Username must be at least 3 characters"):
        LoginRequest(username="ab", password="password123")


def test_invalid_password():
    """Test authentication with invalid password"""
    import pytest
    
    with pytest.raises(ValueError, match="Password must be at least 8 characters"):
        LoginRequest(username="testuser", password="short")


def test_session_expiration():
    """Test session expires correctly"""
    service = AuthenticationService(session_timeout=1)
    request = LoginRequest(username="testuser", password="password123")
    
    session = service.authenticate(request)
    
    # Session valid immediately
    assert service.validate_session(session.session_id)
    
    # Wait for expiration (in production, use time mocking)
    import time
    time.sleep(2)
    
    # Session should be expired
    assert not service.validate_session(session.session_id)


def test_invalid_session_id():
    """Test validation with non-existent session"""
    service = AuthenticationService()
    
    assert not service.validate_session("nonexistent-session-id")
```

---

## Remember

- **Think first, code once**
- **Complete implementation only**
- **No retries or iterations**
- **Tests are mandatory**
- **Quality over speed**

**Success Rate Target: 89%+ (up from 31%)**
