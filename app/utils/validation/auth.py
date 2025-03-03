from app.db.models import Role, RoleEnum

def is_submitter(role):
    return Role.model_validate(role).name == RoleEnum.SUBMITTER.value