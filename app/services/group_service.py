from sqlalchemy.orm import Session
from app.models.group import Group
from app.models.user import User
from app.models.membership import Membership

# Creates a new group and assigns the creator as a group admin
def create_group(db: Session,
                 name: str,
                 creator_id: int) -> Group:
    user = db.query(User).filter(User.id == creator_id).first()
    if not user:
        raise ValueError("User not found")
    
    # Create the group
    new_group = Group(
        name = name
    )

    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    # Create membership for the creator as a group admin
    membership = Membership(user_id = creator_id,
                            group_id = new_group.id,
                            role = "GROUP ADMIN"
    )

    db.add(membership)
    db.commit()
    db.refresh(new_group)
    return new_group

# Adds a user to a group
def add_user_to_group(db: Session,
                      group_id: int,
                      user_id: int,
                      role: str = "MEMBER"):
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    
    # Check if the group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise ValueError("Group not found")
    
    # Prevent duplicating a person in a group
    exist_membership = db.query(Membership).filter(Membership.user_id == user_id, Membership.group_id == group_id).first()
    if exist_membership:
        raise ValueError("User is already in this group")
    
    membership = Membership(user_id = user_id, group_id = group_id, role = role)
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership

# Removes a user from a group
def remove_user_from_group(db: Session,
                           group_id: int,
                           user_id: int):
    membership = db.query(Membership).filter(Membership.user_id == user_id, Membership.group_id == group_id).first()
    if not membership:
        raise ValueError("Membership not found")
    
    db.delete(membership)
    db.commit()

# Updates a user role in a group
def update_group_role(db: Session,
                      group_id: int,
                      user_id: int,
                      new_role: str):
    membership = db.query(Membership).filter(Membership.user_id == user_id, Membership.group_id == group_id).first()
    if not membership:
        raise ValueError("Membership not found")
    
    membership.role = new_role
    db.commit()
    db.refresh(membership)
    return membership
    