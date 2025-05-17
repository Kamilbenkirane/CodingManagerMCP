from enum import Enum


class StatusEnum(str, Enum):
    # For ValidateCodeResponse, UpdateManagerContextResponse,
    # StreamProactiveSuggestionsSubscriptionResponse
    VALID = "valid"
    VALID_WITH_SUGGESTIONS = "valid_with_suggestions"
    NEEDS_REVISION = "needs_revision"
    ERROR = "error"
    CONTEXT_UPDATED = "context_updated"
    UPDATE_QUEUED = "update_queued"
    SUBSCRIBED = "subscribed"
    UNSUBSCRIBED = "unsubscribed"
    UPDATED = "updated"  # For subscription status


class SeverityEnum(str, Enum):
    # For ValidationFeedbackItem
    INFO = "info"
    SUGGESTION = "suggestion"
    WARNING = "warning"
    ERROR = "error"  # Also a StatusEnum, contextually different here


class ReferenceTypeEnum(str, Enum):
    # For ReferenceItem in GetProjectAdviceResponse
    DOCUMENTATION = "documentation"
    FILE = "file"
    CODE_EXAMPLE = "code_example"


class UpdateTypeEnum(str, Enum):
    # For UpdateManagerContextRequest
    NEW_DEPENDENCY = "new_dependency"
    ARCHITECTURAL_DECISION = "architectural_decision"
    STYLE_GUIDE_CHANGE = "style_guide_change"
    FEATURE_SPECIFICATION = "feature_specification"
    FILE_ANNOTATION = "file_annotation"


class SuggestionTypeEnum(str, Enum):
    # For ProactiveSuggestionItem
    REFACTORING_OPPORTUNITY = "refactoring_opportunity"
    POTENTIAL_BUG = "potential_bug"
    STYLE_INCONSISTENCY = "style_inconsistency"
    RELEVANT_MODULE_REMINDER = "relevant_module_reminder"
    BEST_PRACTICE_TIP = "best_practice_tip"
    EFFICIENCY_IMPROVEMENT = "efficiency_improvement"
    NEW_API_USAGE = "new_api_usage"
    DOCUMENTATION_REMINDER = "documentation_reminder"


class PriorityEnum(str, Enum):
    # For ProactiveSuggestionItem
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SubscriptionActionEnum(str, Enum):
    # For StreamProactiveSuggestionsSubscriptionRequest
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    UPDATE_FILTERS = "update_filters"
