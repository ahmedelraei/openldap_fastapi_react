import ldap
import ldap.modlist as modlist
from typing import List
from fastapi import HTTPException

from core.config import settings
from core.security import security_service
from services.interfaces import LDAPServiceAbstractClass
from models.schemas import UserRegistration


class LDAPService(LDAPServiceAbstractClass):
    """LDAP Service"""
    
    def __init__(self):
        self.host = settings.LDAP_HOST
        self.port = settings.LDAP_PORT
        self.base_dn = settings.LDAP_BASE_DN
        self.admin_dn = settings.LDAP_ADMIN_DN
        self.admin_password = settings.LDAP_ADMIN_PASSWORD
        self.users_ou = settings.LDAP_USERS_OU
        self.groups_ou = settings.LDAP_GROUPS_OU

    def _get_connection(self):
        """Get LDAP connection"""
        try:
            conn = ldap.initialize(f"ldap://{self.host}:{self.port}")
            conn.protocol_version = ldap.VERSION3
            conn.simple_bind_s(self.admin_dn, self.admin_password)
            return conn
        except ldap.LDAPError as e:
            raise HTTPException(status_code=500, detail=f"LDAP connection error: {str(e)}")

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user against LDAP"""
        try:
            conn = ldap.initialize(f"ldap://{self.host}:{self.port}")
            conn.protocol_version = ldap.VERSION3
            print(f"Authenticating user {username} against LDAP")
            user_dn = f"uid={username},{self.users_ou},{self.base_dn}"
            conn.simple_bind_s(user_dn, password)
            conn.unbind()
            return True
        except ldap.INVALID_CREDENTIALS:
            return False
        except ldap.LDAPError:
            return False

    def get_user_groups(self, username: str) -> List[str]:
        """Get user's group memberships"""
        try:
            conn = self._get_connection()
            search_filter = f"(&(objectClass=groupOfNames)(member=uid={username},{self.users_ou},{self.base_dn}))"
            result = conn.search_s(f"{self.groups_ou},{self.base_dn}", ldap.SCOPE_SUBTREE, search_filter, ['cn'])
            
            groups = []
            for dn, attrs in result:
                if 'cn' in attrs:
                    groups.extend([group.decode('utf-8') for group in attrs['cn']])
            
            conn.unbind()
            return groups
        except ldap.LDAPError as e:
            raise HTTPException(status_code=500, detail=f"Error getting user groups: {str(e)}")

    def user_exists(self, username: str) -> bool:
        """Check if user exists in LDAP"""
        try:
            conn = self._get_connection()
            result = conn.search_s(
                f"uid={username},{self.users_ou},{self.base_dn}", 
                ldap.SCOPE_BASE
            )
            conn.unbind()
            return len(result) > 0
        except ldap.NO_SUCH_OBJECT:
            return False
        except ldap.LDAPError:
            return False

    def create_user(self, user_data: UserRegistration) -> bool:
        """Create new user in LDAP"""
        try:
            conn = self._get_connection()
            
            # Check if user already exists
            if self.user_exists(user_data.username):
                raise HTTPException(status_code=400, detail="User already exists")
            
            # Get next UID number
            uid_number = self._get_next_uid_number(conn)
            
            password = user_data.password  # Store plaintext for LDAP authentication
            
            # Create user entry
            user_dn = f"uid={user_data.username},{self.users_ou},{self.base_dn}"
            attrs = {
                'objectClass': [b'inetOrgPerson', b'posixAccount', b'shadowAccount'],
                'cn': [user_data.username.encode('utf-8')],
                'sn': [user_data.last_name.encode('utf-8')],
                'givenName': [user_data.first_name.encode('utf-8')],
                'displayName': [f"{user_data.first_name} {user_data.last_name}".encode('utf-8')],
                'uid': [user_data.username.encode('utf-8')],
                'uidNumber': [str(uid_number).encode('utf-8')],
                'gidNumber': [str(uid_number).encode('utf-8')],
                'homeDirectory': [f"/home/{user_data.username}".encode('utf-8')],
                'loginShell': [b'/bin/bash'],
                'mail': [user_data.email.encode('utf-8')],
                'userPassword': [password.encode('utf-8')]
            }
            
            ldif = modlist.addModlist(attrs)
            conn.add_s(user_dn, ldif)
            
            # Add user to specified group
            self._add_user_to_group(conn, user_data.username, user_data.group)
            
            conn.unbind()
            return True
            
        except ldap.LDAPError as e:
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

    def _get_next_uid_number(self, conn) -> int:
        """Get next available UID number"""
        try:
            result = conn.search_s(
                f"{self.users_ou},{self.base_dn}", 
                ldap.SCOPE_SUBTREE, 
                "(objectClass=posixAccount)", 
                ['uidNumber']
            )
            
            uid_numbers = []
            for dn, attrs in result:
                if 'uidNumber' in attrs:
                    uid_numbers.append(int(attrs['uidNumber'][0].decode('utf-8')))
            
            return max(uid_numbers) + 1 if uid_numbers else 1001
            
        except ldap.LDAPError:
            return 1001

    def _add_user_to_group(self, conn, username: str, group_name: str):
        """Add user to a group - private method"""
        try:
            group_dn = f"cn={group_name},{self.groups_ou},{self.base_dn}"
            user_dn = f"uid={username},{self.users_ou},{self.base_dn}"
            
            # Check if group exists, create if not
            try:
                conn.search_s(group_dn, ldap.SCOPE_BASE)
            except ldap.NO_SUCH_OBJECT:
                # Create group
                attrs = {
                    'objectClass': [b'groupOfNames'],
                    'cn': [group_name.encode('utf-8')],
                    'description': [f"{group_name} group".encode('utf-8')],
                    'member': [user_dn.encode('utf-8')]
                }
                ldif = modlist.addModlist(attrs)
                conn.add_s(group_dn, ldif)
                return
            
            # Add user to existing group
            mod_attrs = [(ldap.MOD_ADD, 'member', [user_dn.encode('utf-8')])]
            conn.modify_s(group_dn, mod_attrs)
            
        except ldap.LDAPError as e:
            # If user is already in group, ignore the error
            if "Attribute or value exists" not in str(e):
                raise HTTPException(status_code=500, detail=f"Error adding user to group: {str(e)}")


def get_ldap_service() -> LDAPServiceAbstractClass:
    """Factory function for LDAP service"""
    return LDAPService()
