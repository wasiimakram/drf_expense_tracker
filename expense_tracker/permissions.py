from rest_framework import permissions

class IsManagerAdminOrOwner(permissions.BasePermission):
    """
    Custom Permission Logic:
    1. Managers (Group): Read-Only access to EVERYTHING.
    2. Admins (Staff): Full access (Read/Write/Delete) to EVERYTHING.
    3. Owners: Read/Write access to THEIR OWN records. NO DELETE allowed.
    """

    def has_permission(self, request, view):
        # Layer 1: Authentication Check
        # User must be logged in to even try accessing this endpoint
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        method = request.method # GET, POST, PUT, DELETE
        
        # --- ROLE 1: MANAGER ---
        # Managers can VIEW all data, but cannot change anything.
        is_manager = user.groups.filter(name='Manager').exists()
        if is_manager:
            if method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
                return True # Allow Read
            return False # Deny Write/Delete for Managers

        # --- ROLE 2: ADMIN ---
        # Admins have 'God Mode'. They can do anything to any object.
        if user.is_staff:
            return True # Allow Everything

        # --- ROLE 3: REGULAR OWNER ---
        # If you are not a Manager or Admin, you must own the object.
        is_owner = (obj.owner == user)
        
        if not is_owner:
            return False # You cannot touch other people's data!
            
        # If you are the owner, you have rights, BUT with one restriction:
        if method == 'DELETE':
            return False # Policy: Owners cannot delete records (Audit requirement)
            
        return True # Allow Read/Edit for Owner
