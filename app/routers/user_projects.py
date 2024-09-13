@router.get("/users/{user_id}/projects", response_model=List[Project_Pydantic])
async def get_user_projects(user_id: int):
    user = await Users.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_projects = await UserProjects.filter(user_id=user_id).prefetch_related('project')
    projects = [user_project.project for user_project in user_projects]
    return await Project_Pydantic.from_queryset(projects)