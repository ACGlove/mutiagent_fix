from pydantic import BaseModel,Field


class Plan_structure(BaseModel):
    id:str=Field(description='此步骤的唯一标识，如step_1')
    step_depends_on:list[str]=Field(description='此步骤依赖的步骤的step_id',default=[])
    objective:str=Field(description='此步骤的目标')
    expected_output:str=Field(description='预期结果')


class Plan(BaseModel):
    plan:list[Plan_structure]






















































