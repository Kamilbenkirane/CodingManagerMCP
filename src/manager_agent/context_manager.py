from typing import List, Optional

from pydantic import BaseModel, Field


class KeyModule(BaseModel):
    """Represents a key module or component in the project."""

    name: str = Field(..., description="The name of the module.")
    description: str = Field(
        ...,
        description="A brief description of the module's purpose and " "functionality.",
    )
    path: Optional[str] = Field(
        None,
        description="Optional file path to the module's primary source "
        "file or directory.",
    )


class CodingStandard(BaseModel):
    """Represents a specific coding standard or convention."""

    id: str = Field(
        ...,
        description="A unique identifier for the standard (e.g., 'CS-001').",
    )
    description: str = Field(..., description="The description of the coding standard.")
    category: Optional[str] = Field(
        None,
        description="Category of the standard (e.g., 'Formatting', 'Naming', "
        "'Security').",
    )


class ProjectRequirement(BaseModel):
    """Represents a specific project requirement."""

    id: str = Field(
        ...,
        description="A unique identifier for the requirement (e.g., 'REQ-001').",
    )
    description: str = Field(
        ..., description="The detailed description of the requirement."
    )
    priority: Optional[str] = Field(
        "medium",
        description="Priority of the requirement (e.g., 'high'," " 'medium', 'low').",
    )


class ProjectContext(BaseModel):
    """
    Represents the comprehensive context of a software project.
    This model stores architecture details, key modules, coding standards,
    requirements, and overall project goals.
    """

    project_name: str = Field(..., description="The official name of the project.")
    project_goals: List[str] = Field(
        default_factory=list,
        description="A list of high-level goals for the project.",
    )
    architecture_overview: Optional[str] = Field(
        None, description="A textual overview of the project's architecture."
    )
    key_modules: List[KeyModule] = Field(
        default_factory=list,
        description="A list of key modules or components in the project.",
    )
    coding_standards: List[CodingStandard] = Field(
        default_factory=list,
        description="A list of coding standards and conventions to be " "followed.",
    )
    requirements: List[ProjectRequirement] = Field(
        default_factory=list,
        description="A list of functional and non-functional requirements for "
        "the project.",
    )
    # Future fields could include:
    # - technology_stack: List[str]
    # - external_dependencies: List[Dependency]
    # - data_models_overview: str
    # - deployment_environment: str
