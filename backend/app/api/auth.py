import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User, Profile
from backend.app.models.passport import SkillPassport
from backend.app.schemas.auth import UserRegister, UserLogin, Token
from backend.app.utils.security import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

DEMO_PERSONAS = {
    "arif": "arif@skillpath.dev",
    "priya": "priya@skillpath.dev",
    "rohan": "rohan@skillpath.dev",
    "ananya": "ananya@skillpath.dev",
    "admin": "admin@skillpath.dev"
}

@router.post("/guest", response_model=Token)
def guest_login(db: Session = Depends(get_db)):
    """
    Creates an instant anonymous learner profile and returns a valid JWT,
    enabling frictionless 'Start my career journey' zero-barrier entry.
    """
    guest_uid = uuid.uuid4().hex[:8]
    guest_email = f"guest_{guest_uid}@guest.skillpath.dev"

    user = User(
        email=guest_email,
        hashed_password=get_password_hash(uuid.uuid4().hex),
        role="learner",
        is_active=True
    )
    db.add(user)
    db.flush()

    profile = Profile(
        user_id=user.id,
        full_name="Guest Explorer",
        education="College / University",
        branch="Undecided",
        year=1,
        goal_status="unknown",
        weekly_hours=8.0,
        learner_pace_factor=1.0
    )
    db.add(profile)

    passport = SkillPassport(
        user_id=user.id,
        slug=f"guest-{user.id:04d}",
        is_public=True
    )
    db.add(passport)
    db.commit()

    token_data = {"sub": user.email, "user_id": user.id, "role": user.role, "is_guest": True}
    access_token = create_access_token(token_data)

    return Token(
        access_token=access_token,
        role=user.role,
        user_id=user.id,
        full_name=profile.full_name,
        email=user.email,
        goal_status=profile.goal_status,
        is_guest=True
    )

@router.post("/demo/{name}", response_model=Token)
def demo_login(name: str, db: Session = Depends(get_db)):
    """
    Passwordless instant login for seeded evaluation personas
    (arif, priya, rohan, ananya, admin).
    """
    normalized_name = name.strip().lower()
    demo_email = DEMO_PERSONAS.get(normalized_name)
    if not demo_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown demo persona '{name}'. Available personas: {', '.join(DEMO_PERSONAS.keys())}"
        )

    user = db.query(User).filter(User.email == demo_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Demo user '{demo_email}' is not seeded in database. Run 'make seed'."
        )

    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    full_name = profile.full_name if profile else normalized_name.title()
    career_goal = profile.career_goal if profile else None
    goal_status = profile.goal_status if profile else None

    token_data = {"sub": user.email, "user_id": user.id, "role": user.role}
    access_token = create_access_token(token_data)

    return Token(
        access_token=access_token,
        role=user.role,
        user_id=user.id,
        full_name=full_name,
        email=user.email,
        career_goal=career_goal,
        goal_status=goal_status,
        is_guest=False
    )

@router.post("/register", response_model=Token)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists"
        )

    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_active=True
    )
    db.add(user)
    db.flush()

    profile = Profile(
        user_id=user.id,
        full_name=user_in.full_name,
        goal_status="unknown",
        weekly_hours=8.0,
        learner_pace_factor=1.0
    )
    db.add(profile)

    slug = user_in.full_name.lower().replace(" ", "-") + f"-{user.id:04d}"
    passport = SkillPassport(
        user_id=user.id,
        slug=slug,
        is_public=True
    )
    db.add(passport)
    db.commit()

    token_data = {"sub": user.email, "user_id": user.id, "role": user.role}
    access_token = create_access_token(token_data)

    return Token(
        access_token=access_token,
        role=user.role,
        user_id=user.id,
        full_name=profile.full_name,
        email=user.email,
        goal_status=profile.goal_status,
        is_guest=False
    )

@router.post("/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    full_name = profile.full_name if profile else "Student"
    career_goal = profile.career_goal if profile else None
    goal_status = profile.goal_status if profile else None

    token_data = {"sub": user.email, "user_id": user.id, "role": user.role}
    access_token = create_access_token(token_data)

    return Token(
        access_token=access_token,
        role=user.role,
        user_id=user.id,
        full_name=full_name,
        email=user.email,
        career_goal=career_goal,
        goal_status=goal_status,
        is_guest=False
    )

