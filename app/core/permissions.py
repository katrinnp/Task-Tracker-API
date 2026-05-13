from sqlalchemy.orm import Session
from app.models.user import User
from app.models.membership import Membership

# Check if user is admin
def is_admin(user: User) -> bool:
    return user.role == "admin"

# Check if user is a group admin
def is_group_admin(db: Session, user: User, group_id: int) -> bool:
    membership = (db.query(Membership).filter(Membership.user_id == user.id, Membership.group_id == group_id, Membership.role == "group_admin").first())
    return membership is not None

# Check if current_user can manage target_user
def can_manage_user(db: Session, current_user: User, target_user: User) -> bool:
    if is_admin(current_user): # Global admin has full access
        return True
    # Find all groups where current_user is a group admin
    current_admin_groups = (db.query(Membership.group_id).filter(
        Membership.user_id == current_user.id, 
        Membership.role == "group_admin").all()) # Returns a list of matching rows
    admin_group_ids = [group[0] for group in current_admin_groups] # For each group in current_admin_groups, take first element
    if not admin_group_ids: # Can not manage anyone
        return False
    # Check if user belongs to any admin groups
    shared_membership = (db.query(Membership).filter(
        Membership.user_id == target_user.id, 
        Membership.group_id.in_(admin_group_ids)).first())
    # If a shared group exists, current_user can manage target_user
    return shared_membership is not None

# Check if current_user can view a task
def can_view_task(db: Session, current_user: User, task) -> bool:
    if task.user_id == current_user.id:
        return True
    if is_admin(current_user):
        return True
    # Check if current_user can manage the owner of this task
    return can_manage_user(db, current_user, task.owner)

