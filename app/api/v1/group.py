from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import (get_current_user, require_admin, require_group_admin)
from app.models.user import User
from app.models.group import Group
from app.schemas.schemas import (GroupCreate, GroupRead, MembershipCreate, MembershipRead)
from app.services.group_service import (create_group, add_user_to_group, remove_user_from_group, update_group_role)

router = APIRouter(
    prefix = "/groups",
    tags = ["Groups"]
)

# Create a new group
@router.post("/", response_model = GroupRead)
def create_new_group(group: GroupCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    try:
        return create_group(db, group.name, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
# Get a specific group
@router.get("/{group_id}", response_model = GroupRead)
def get_group(group_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_group_admin(group_id, current_user, db)

    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code = 404, detail = "Group not found")
    
    return group

# Add user to group
@router.post("/{group_id}/members", response_model = MembershipRead)
def add_member(group_id: int, membership: MembershipCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_group_admin(group_id, current_user, db)
    try:
        return add_user_to_group(db, group_id, membership.user_id, membership.role)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
# Update user role in group
@router.patch("/{group_id}/members/{user_id}", response_model = MembershipRead)
def change_member_role(group_id: int, user_id: int, membership: MembershipCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_group_admin(group_id, current_user, db)
    try:
        return update_group_role(db, group_id, user_id, membership.role)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
# Remove user from group
@router.delete("/{group_id}/members/{user_id}")
def remove_member(group_id: int, user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_group_admin(group_id, current_user, db)
    try:
        remove_user_from_group(db, group_id, user_id)
        return {"message": "User removed from group"}
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))
    