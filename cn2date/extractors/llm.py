from ..core.proto import ExtractionResult
from ..core.base_extractor import BaseExtractor


class LlmExtractor(BaseExtractor):
    def extract(self, text: str) -> ExtractionResult: ...

    @property
    def name(self) -> str:
        return "llm_extractor"
