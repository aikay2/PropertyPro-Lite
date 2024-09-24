from rest_framework import permissions

class IsAgentOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow:
    - Authenticated agents to have full access (create, update, delete).
    - Only agents who own the property can modify it.
    - Authenticated non-agents to have read-only access.
    - Unauthenticated users cannot access anything.
    """

    def has_permission(self, request, view):
        # Allow read-only access for authenticated users (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Allow full access (POST, PUT, DELETE) only for authenticated agents
        return request.user.is_authenticated and request.user.user_type == 'agent'
    
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for authenticated users (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow modification only if the agent owns the property
        return request.user.is_authenticated and request.user.user_type == 'agent' and obj.owner == request.user.agent_profile
    
    
class IsAgent(permissions.BasePermission):
    """
    Custom permission to allow:
    - Only authenticated agents to have full access (POST, PUT, DELETE).
    - Agents can only modify the properties or models they own (where they are the owner/user).
    """
    
    def has_permission(self, request, view):
        # Allow full access (POST, PUT, DELETE) only for authenticated agents
        return request.user.is_authenticated and request.user.user_type == 'agent'

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission to allow agents to modify properties
        or models where they are the owner.
        """
        # Allow safe methods (GET, HEAD, OPTIONS) for all agents
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user.agent_profile


class IsAuthenticatedAndOwner(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users to create flags,
    and only allow users to edit flags they created.
    """

    def has_permission(self, request, view):
        # Allow creation of flags only for authenticated users
        if request.method == 'POST':
            return request.user.is_authenticated
        
        # For other methods (like PUT, PATCH), check if the user is the owner
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only allow the owner of the flag to edit it
        return obj.created_by == request.user
