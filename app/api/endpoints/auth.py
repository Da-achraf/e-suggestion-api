from typing import Optional
from fastapi import APIRouter, status
from sqlalchemy.exc import SQLAlchemyError

from app.core.security import generate_tokens
from app.db.dependencies import SessionDep


from app.dependencies.user import UserToSaveDep
from app.db.repositories import UserRepositoryDep, RoleRepositoryDep
from app.core.config import SettingsDep
from app.core.dpendencies import AuthenticatedUserDep
from app.schemas import Response
from app.db.models import User, UserWithToken, Role, RoleEnum
from app.schemas.auth import Token
from app.utils.exceptions.db import transaction_failed

from app.utils.exceptions.auth import account_not_approved, incorrect_credentials


router = APIRouter()


# Register A User
@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=Response[UserWithToken])
async def register(
    user_to_save: UserToSaveDep,
    user_repository: UserRepositoryDep,
    role_repository: RoleRepositoryDep,
    db: SessionDep,
    settings: SettingsDep
):

    if not user_to_save:
        raise exceptions.credentials_already_taken
    try:
        saved_user = user_repository.insert_line(data=user_to_save, db=db)
        
        parsed_user = User.model_validate(saved_user)
        
        role: Optional[Role] = role_repository.find_by_id(db=db, model_id=user_to_save.role_id)
        
        # Activate the account
        if role and Role.model_validate(role).name == RoleEnum.SUBMITTER.value:
            saved_user.account_status = True
        
        if parsed_user and role and role.name not in [role['name'] for role in parsed_user.roles]:
            saved_user.roles.append(role)
        
        db.commit()
        
        # Generate tokens
        access_token, _ = generate_tokens(user=parsed_user, settings=settings.JWT)
        user_with_token = UserWithToken(**parsed_user.model_dump(), token=access_token)
        
    except SQLAlchemyError:
        db.rollback()
        raise transaction_failed
    else:
        db.commit()
        return Response[UserWithToken](
            data=user_with_token
        )


# Login
@router.post(path="/login", response_model=Response[UserWithToken])
async def login_for_tokens(
    settings: SettingsDep,
    authenticated_user: AuthenticatedUserDep,
):

    if not authenticated_user:
        raise incorrect_credentials
    if not authenticated_user.account_status:
        raise account_not_approved

    access_token, _ = generate_tokens(user=authenticated_user, settings=settings.JWT)
    
    user_with_token = UserWithToken(**authenticated_user.model_dump(), token=access_token)

    return Response[UserWithToken](
        data=user_with_token
    )


# @router.get(path="/refresh-token", status_code=status.HTTP_200_OK, response_model=Response)
# async def refresh_access_token(
#         token: str,
#         db: SessionDep,
#         settings: SettingsDep
# ):
#     sett = TokenVerificationSettings(
#         token=token,
#         key=settings.JWT.REFRESH_SECRET,
#         algorithm=settings.JWT.ALGORITHM
#     )
#     username = await verify_token(sett)
#     if not username:
#         raise invalid_token
#     user: User = user_repository.find_by_username_or_email(username=username, db=db)
#     if not user:
#         raise incorrect_credentials

#     access_token, refresh_token = generate_tokens(user=user, settings=settings.JWT)

#     return Response[Token](
#         data=Token(
#             access_token=access_token,
#             refresh_token=refresh_token,
#             token_type="bearer"
#         )
#     )


# @router.post(path="/forget-password", status_code=status.HTTP_200_OK, response_model=Response)
# async def forget_password(
#         fpr: ForgetPasswordRequest,
#         bg_tasks: BackgroundTasks,
#         settings: Settings = Depends(get_settings),
#         db: Session = Depends(get_db)
# ):
#     try:
#         user = user_repository.find_by_username_or_email(email=fpr.email, db=db)
#         if user is None:
#             raise exceptions.invalid_email

#         secret_token = create_reset_password_token(email=fpr.email, settings=settings.JWT)
#         forget_url_link = f"http://{settings.APP_HOST}/auth/reset-password?token={secret_token}"

#         email_body = format_template(
#             reset_pwd_html_template,
#             username=user.username,
#             link_expiry_min=int(settings.FORGET_PASSWORD_LINK_EXPIRE_MINUTES),
#             reset_link=forget_url_link
#         )

#         bg_tasks.add_task(
#             send_email,
#             user.email,
#             email_body,
#             settings.MAIL
#         )

#         return Response(
#             message="Email has been sent"
#         )

#     except Exception as e:
#         raise e


# @router.post(path="/verify-rp-token", status_code=status.HTTP_200_OK, response_model=Response)
# async def verify_reset_password_token(
#         rptvr: ResetPasswordTokenVerificationRequest,
#         settings: Settings = Depends(get_settings),
# ):
#     try:
#         token_verif_settings = TokenVerificationSettings(
#             token=rptvr.token,
#             key=settings.JWT.FORGET_PWD_SECRET,
#             algorithm=settings.JWT.ALGORITHM
#         )

#         email = await verify_token(token_verif_settings)

#         if not email:
#             raise exceptions.invalid_token

#         return Response[ForgetPasswordRequest](
#             data=ForgetPasswordRequest(email=email),
#             message="Token verified successfully"
#         )

#     except Exception as e:
#         raise e


# @router.post(path="/reset-password", status_code=status.HTTP_200_OK, response_model=Response)
# async def reset_password(
#         rpr: ResetPasswordRequest,
#         db: Session = Depends(get_db)
# ):
#     try:
#         if rpr.new_password != rpr.confirm_password:
#             raise exceptions.passwords_mismatch

#         new_hashed_password = get_password_hash(password=rpr.new_password)
#         user_repository.update_password(
#             email=rpr.email,
#             new_password=new_hashed_password,
#             db=db
#         )

#         return Response(
#             message="Password updated successfully",
#         )

#     except Exception as e:
#         raise e