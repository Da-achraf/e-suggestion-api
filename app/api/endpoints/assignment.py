from typing import Dict

from app.db.models import AssignmentModel, Assignment, AssignmentCreate
from app.api.base_router import BaseRouter
from app.db.repositories import AssignmentRepository, UserRepositoryDep, AssignmentRepositoryDep
from app.db.dependencies import SessionDep
from app.schemas.response import Response
from app.utils.exceptions.db import transaction_failed

class AssignmentRouter(BaseRouter[AssignmentModel, Assignment]):
    def __init__(self):
        super().__init__(
            repository=AssignmentRepository(),
            request_type=AssignmentCreate,
            response_type=Assignment
        )
        
    async def update_item_by_id(
        self,
        resource_id: int,
        resource_to_update: Dict,
        db: SessionDep,
        user_repository: UserRepositoryDep,
        assignment_repository: AssignmentRepositoryDep,
    ):
        try:
            response = await super().update_item_by_id(
                resource_id=resource_id,
                resource_to_update=resource_to_update,
                db=db
            )
        except:
            raise transaction_failed
        
        # Add assignees
        try:
            if 'assignees' in resource_to_update.keys():
                assignees = resource_to_update['assignees']
            
                # Validate that assignees is an array of numbers
                if not isinstance(assignees, list) or not all(isinstance(assignee, int) for assignee in assignees):
                    raise ValueError("Assignees must be an array of integers (user IDs).")
                
                # Fetch the assignment
                assignment = assignment_repository.find_by_id(db=db, model_id=resource_id)
                if not assignment:
                    return response
                
                # Clear existing assignees
                assignment.assignees.clear()
                
                # Fetch all users in a single query for efficiency
                users = user_repository.find_by_ids(db=db, ids=assignees)
                
                # Add new assignees
                for user in users:
                    assignment.assignees.append(user)

                db.commit()
                
                return Response[self.response_type](data=assignment)
            
            return response
        except Exception as e:
            print('--EXception: ', str(e))
            raise transaction_failed
        

router = AssignmentRouter().router