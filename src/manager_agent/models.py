from typing import List, Optional

from pydantic import BaseModel

from .enums import (
    PriorityEnum,
    ReferenceTypeEnum,
    SeverityEnum,
    StatusEnum,
    SubscriptionActionEnum,
    SuggestionTypeEnum,
    UpdateTypeEnum,
)


# Common inline models
class SelectionRange(BaseModel):
    start_line: int
    end_line: int


class LineRange(BaseModel):
    start_line: int
    end_line: int


# 4.1 Capability: validate_code
class ValidateCodeRequest(BaseModel):
    code_content: str
    file_path: str
    selection_range: Optional[SelectionRange] = None
    developer_intent: Optional[str] = None
    additional_context_paths: Optional[List[str]] = None


class ValidationFeedbackItem(BaseModel):
    item_id: str
    severity: SeverityEnum
    message: str
    file_path: str  # File the feedback pertains to
    line_range: Optional[LineRange] = None
    suggested_code_fix: Optional[str] = None


class ValidateCodeResponse(BaseModel):
    validation_id: str
    status: StatusEnum
    feedback_items: List[ValidationFeedbackItem]


# 4.2 Capability: get_project_advice
class GetProjectAdviceRequest(BaseModel):
    query: str
    current_file_path: Optional[str] = None
    related_code_snippet: Optional[str] = None


class ReferenceItem(BaseModel):
    reference_type: ReferenceTypeEnum
    path_or_url: str
    description: str


class GetProjectAdviceResponse(BaseModel):
    advice_id: str
    response_text: str
    references: Optional[List[ReferenceItem]] = None
    suggested_sub_tasks: Optional[List[str]] = None


# 4.3 Capability: update_manager_context
class UpdateManagerContextRequest(BaseModel):
    update_type: UpdateTypeEnum
    summary: str
    details_uri_or_text: str
    relevant_file_paths: Optional[List[str]] = None


class UpdateManagerContextResponse(BaseModel):
    update_id: str
    status: StatusEnum
    message: Optional[str] = None


# 4.4 Capability: get_task_starting_context
class GetTaskStartingContextRequest(BaseModel):
    task_id: Optional[str] = None
    task_description: str
    target_file_path: str  # The primary file path where the work will be done
    related_file_paths: Optional[List[str]] = None
    user_query_for_llm: Optional[str] = None


class RelevantModuleOrInterface(BaseModel):
    name: str
    description: str
    usage_example_snippet: Optional[str] = None


class DataModelToUse(BaseModel):
    name: str
    definition_path_or_snippet: str


class GetTaskStartingContextResponse(BaseModel):
    context_id: str
    context_summary: str
    relevant_modules_or_interfaces: Optional[List[RelevantModuleOrInterface]] = None
    key_design_patterns_to_follow: Optional[List[str]] = None
    code_style_reminders: Optional[List[str]] = None
    data_models_to_use: Optional[List[DataModelToUse]] = None
    warnings_or_common_pitfalls: Optional[List[str]] = None
    suggested_sub_tasks: Optional[List[str]] = None


# 4.5 Capability: stream_proactive_suggestions
class ProactiveSuggestionItem(BaseModel):  # This is the data pushed in the stream
    suggestion_id: str
    type: SuggestionTypeEnum
    message: str
    file_path: Optional[str] = None
    line_range: Optional[LineRange] = None
    priority: PriorityEnum
    supporting_context_snippets: Optional[List[str]] = None
    related_documentation_links: Optional[List[str]] = None


class FilterPreferences(BaseModel):
    min_priority: Optional[PriorityEnum] = None
    types_to_include: Optional[List[SuggestionTypeEnum]] = None
    # Using Dict[str, Any] for future flexibility if more complex filters
    # are needed.
    # For now, it aligns with the example:
    # {min_priority: 'medium', types_to_include: ['potential_bug']}
    # This could be more strictly typed if the filter structure is fixed.
    # For the example `filter_preferences: object` in blueprints, this is a
    # flexible way.
    # If it were `filter_preferences: {min_priority: string,
    # types_to_include: list[string]}`, then `min_priority:
    # Optional[PriorityEnum]` and `types_to_include:
    # Optional[List[SuggestionTypeEnum]]` would be directly in
    # StreamProactiveSuggestionsSubscriptionRequest.
    # The blueprint's `object` suggests a flexible dictionary.
    # We'll stick to specific fields for now as per the example, and can
    # expand if needed.


class StreamProactiveSuggestionsSubscriptionRequest(BaseModel):  # Request from Cursor
    action: SubscriptionActionEnum
    project_id: str
    # The blueprint specifies `filter_preferences: object`.
    # An example {min_priority: 'medium',
    # types_to_include: ['potential_bug', 'refactoring_opportunity']} is given.
    # This implies filter_preferences is a dictionary. For Pydantic, we can
    # define a nested model or use Dict.
    # Let's use a specific model for clarity based on the example.
    filter_preferences: Optional[FilterPreferences] = None


class StreamProactiveSuggestionsSubscriptionResponse(
    BaseModel
):  # Response to subscription management
    subscription_id: Optional[str] = None  # Present if subscribed/updated successfully
    status: StatusEnum
    message: Optional[str] = None
