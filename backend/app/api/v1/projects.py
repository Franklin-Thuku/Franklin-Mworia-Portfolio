from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.api.deps import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    category: Optional[str] = Query(None, description="Filter by category slug (e.g. backend, ai, security)"),
    featured_only: Optional[bool] = Query(False, description="Return only featured case studies"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Fetch all portfolio projects with optional category filtering and pagination.
    """
    query = select(Project).order_by(Project.created_at.asc())
    
    if featured_only:
        query = query.where(Project.is_featured == True)
        
    if category and category.lower() != "all":
        query = query.where(
            or_(
                Project.category_slug.ilike(f"%{category}%"),
                Project.category.ilike(f"%{category}%")
            )
        )
        
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{slug_or_id}", response_model=ProjectResponse)
async def get_project(
    slug_or_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve full details and architecture for a single project by slug or ID.
    """
    query = select(Project).where(
        or_(Project.slug == slug_or_id, Project.id == slug_or_id)
    )
    result = await db.execute(query)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with identifier '{slug_or_id}' not found."
        )
    return project


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new portfolio project entry.
    """
    # Check if slug already exists
    existing = await db.execute(select(Project).where(Project.slug == project_in.slug))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A project with slug '{project_in.slug}' already exists."
        )
    
    project_data = project_in.model_dump()
    project = Project(**project_data)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_in: ProjectUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing project entry.
    """
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{project_id}' not found."
        )
        
    update_data = project_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
        
    await db.commit()
    await db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Remove a project from the catalog.
    """
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{project_id}' not found."
        )
        
    await db.delete(project)
    await db.commit()
    return None
