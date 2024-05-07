from dataclasses import dataclass, field
from pydantic import BaseModel
from ai_products.models import PromptInput
from typing import Dict, Any, List, Optional


@dataclass
class AiInputTypeLogicResult:
    message: Optional[str] = None
    function: Optional[Dict[str, Any]] = None
    output_base_model: Optional[BaseModel] = None
    prompt_inputs: List[PromptInput] = field(default_factory=list)
