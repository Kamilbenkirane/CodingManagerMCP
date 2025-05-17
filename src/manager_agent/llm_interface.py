from typing import AsyncGenerator, List, Optional

from .context_manager import ProjectContext
from .enums import (
    PriorityEnum,
    ReferenceTypeEnum,
    SeverityEnum,
    StatusEnum,
    SuggestionTypeEnum,
)
from .models import (
    DataModelToUse,
    GetProjectAdviceResponse,
    GetTaskStartingContextResponse,
    ProactiveSuggestionItem,
    ReferenceItem,
    RelevantModuleOrInterface,
    ValidateCodeResponse,
    ValidationFeedbackItem,
)


class LLMInterface:
    """
    Interface for communication with a Large Language Model (LLM).
    This class defines methods for various LLM-driven analyses and content
    generation tasks required by the Manager Agent's capabilities.
    Initially, these methods will return mock responses.
    """

    async def analyze_code_for_validation(
        self,
        code_content: str,
        file_path: str,
        project_context: ProjectContext,
        developer_intent: Optional[str] = None,
        # additional_context_paths: Optional[List[str]] = None # From blueprints
    ) -> ValidateCodeResponse:
        """
        Analyzes code for validation against project context, standards, & goals.
        (Mock implementation)
        """
        mock_feedback = []
        if "error" in code_content.lower():
            mock_feedback.append(
                ValidationFeedbackItem(
                    item_id="mock-err-001",
                    severity=SeverityEnum.error,
                    message="Mock Error: Found 'error' keyword. This code "
                    "might have issues.",
                    file_path=file_path,
                    line_range=None,  # Add if possible to determine from mock
                    suggested_code_fix="# Consider removing or handling the "
                    "'error' keyword.",
                )
            )
        else:
            mock_feedback.append(
                ValidationFeedbackItem(
                    item_id="mock-sug-001",
                    severity=SeverityEnum.suggestion,
                    message="Mock Suggestion: Code looks okay. Consider more "
                    "comments.",
                    file_path=file_path,
                    line_range=None,
                )
            )

        return ValidateCodeResponse(
            validation_id="mock-validation-123",
            status=(
                StatusEnum.valid_with_suggestions
                if mock_feedback
                and mock_feedback[0].severity == SeverityEnum.suggestion
                else StatusEnum.needs_revision
            ),
            feedback_items=mock_feedback,
        )

    async def generate_advice(
        self,
        query: str,
        project_context: ProjectContext,
        current_file_path: Optional[str] = None,
        related_code_snippet: Optional[str] = None,
    ) -> GetProjectAdviceResponse:
        """
        Generates contextual advice or answers questions related to the project.
        (Mock implementation)
        """
        mock_response_text = (
            f"Mock advice for '{query}': Always consult the "
            f"{project_context.project_name} docs. For example, use the "
            f"standard logging module."
        )
        mock_references = [
            ReferenceItem(
                reference_type=ReferenceTypeEnum.documentation,
                path_or_url="docs/README.md",  # Assuming a generic doc
                description="Project README for general guidelines",
            )
        ]
        if project_context.key_modules:
            first_module = project_context.key_modules[0]
            mock_references.append(
                ReferenceItem(
                    reference_type=ReferenceTypeEnum.code_example,
                    path_or_url=(
                        first_module.path
                        if first_module.path
                        else f"module/{first_module.name.lower()}.py"
                    ),
                    description=f"Example usage in {first_module.name}",
                )
            )

        return GetProjectAdviceResponse(
            advice_id="mock-advice-456",
            response_text=mock_response_text,
            references=mock_references,
            suggested_sub_tasks=[
                "Review relevant code examples",
                "Update configuration if needed",
            ],
        )

    async def generate_task_starting_context(
        self,
        task_description: str,
        target_file_path: str,
        project_context: ProjectContext,
        related_file_paths: Optional[List[str]] = None,
        user_query_for_llm: Optional[str] = None,
    ) -> GetTaskStartingContextResponse:
        """
        Provides relevant project context, guidelines, & pointers for a new task.
        (Mock implementation)
        """
        # Extract conditional expressions to variables for clarity
        module_name = (
            project_context.key_modules[0].name
            if project_context.key_modules
            else "main module"
        )
        coding_standard = (
            project_context.coding_standards[0].description
            if project_context.coding_standards
            else "PEP 8"
        )

        # Construct context summary with extracted variables
        context_summary = (
            f"Mock Context: For task '{task_description}', "
            f"use modules like {module_name} "
            f"and follow coding standards like '{coding_standard}'"
        )

        relevant_modules = []
        if project_context.key_modules:
            for mod in project_context.key_modules[:2]:  # Max 2 for mock
                usage_snippet_l1 = f"# from {mod.path} import {mod.name}\n"
                usage_snippet_l2 = f"# {mod.name.lower()} = {mod.name}()"
                usage_example_snippet = usage_snippet_l1 + usage_snippet_l2
                relevant_modules.append(
                    RelevantModuleOrInterface(
                        name=mod.name,
                        description=mod.description,
                        usage_example_snippet=usage_example_snippet,
                    ),
                )

        data_models = []
        if (
            project_context.requirements
        ):  # Using requirements as a proxy for data model needs for mock
            definition_l1 = "class ExampleSchema(BaseModel): "
            definition_l2 = "id: int; name: str"
            definition_path_or_snippet = definition_l1 + definition_l2
            data_models.append(
                DataModelToUse(
                    name="ExampleSchema",
                    definition_path_or_snippet=definition_path_or_snippet,
                )  # Ensure parameters are on separate lines
            )

        return GetTaskStartingContextResponse(
            context_id="mock-context-789",
            context_summary=context_summary,
            relevant_modules_or_interfaces=relevant_modules,
            key_design_patterns_to_follow=[
                "Repository Pattern (Mock)",
                "Observer Pattern (Mock)",
            ],
            code_style_reminders=[
                cs.description for cs in project_context.coding_standards[:2]
            ],
            data_models_to_use=data_models,
            warnings_or_common_pitfalls=[
                "Mock Warning: Avoid direct DB calls from controllers.",
                "Remember to handle None values carefully.",
            ],
            suggested_sub_tasks=[
                "Define data models",
                "Implement business logic",
                "Write unit tests",
            ],
        )

    async def stream_proactive_suggestions(
        self,
        project_context: ProjectContext,
        # Potentially add more parameters like active_file, recent_changes etc.
    ) -> AsyncGenerator[ProactiveSuggestionItem, None]:
        """
        Streams proactive suggestions based on ongoing analysis.
        (Mock implementation - yields a few predefined suggestions)
        """
        yield ProactiveSuggestionItem(
            suggestion_id="mock-proactive-sug-001",
            type=SuggestionTypeEnum.best_practice_tip,
            message="Mock Tip: Consider refactoring long functions for better "
            "readability.",
            file_path="src/manager_agent/agent.py",  # Example path
            priority=PriorityEnum.low,
        )
        yield ProactiveSuggestionItem(
            suggestion_id="mock-proactive-sug-002",
            type=SuggestionTypeEnum.potential_bug,
            message="Mock Warning: A new dependency was added, ensure it's "
            "in pyproject.toml.",
            priority=PriorityEnum.medium,
        )
        # This is a generator, so it would yield suggestions as they are found.
        # For a mock, we just yield a couple and finish.
        if False:  # Keep Pyright happy about an empty generator
            yield

    async def close(self):
        """
        Clean up any resources (e.g., close HTTP client sessions).
        (Mock implementation)
        """


# Example usage (for testing purposes, remove later)
# if __name__ == "__main__":
#     import asyncio
#     from .context_manager import ProjectContext, KeyModule, CodingStandard
#
#     async def main():
#         llm_interface = LLMInterface()
#         sample_context = ProjectContext(
#             project_name="TestProject",
#             project_goals=["Goal 1"],
#             key_modules=[KeyModule(name="TestModule", description="A test "
#                                    "module", path="modules/test.py")],
#             coding_standards=[CodingStandard(id="CS-1", description="Follow "
#                                              "PEP8")]
#         )
#
#         # Test validate_code
#         validation_resp = await llm_interface.analyze_code_for_validation(
#             code_content="def hello():\n  print('hello') # error here "
#             "potentially",
#             file_path="test.py",
#             project_context=sample_context,
#             developer_intent="Testing validation"
#         )
#         print("\nValidation Response:", validation_resp.model_dump_json(indent=2))
#
#         # Test get_project_advice
#         advice_resp = await llm_interface.generate_advice(
#             query="How to log?", project_context=sample_context
#         )
#         print("\nAdvice Response:", advice_resp.model_dump_json(indent=2))
#
#         # Test get_task_starting_context
#         task_context_resp = await llm_interface.generate_task_starting_context(
#             task_description="Implement new feature",
#             target_file_path="feature.py",
#             project_context=sample_context
#         )
#         print("\nTask Context Response:", task_context_resp.model_dump_json(indent=2))
#
#         # Test stream_proactive_suggestions
#         print("\nProactive Suggestions:")
#         async for suggestion in llm_interface.stream_proactive_suggestions(
#             project_context=sample_context
#         ):
#             print(suggestion.model_dump_json(indent=2))
#
#         await llm_interface.close()
#
#     asyncio.run(main())
