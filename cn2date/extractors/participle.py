from ..core.proto import ExtractionResult
from ..core.base_extractor import BaseExtractor


class ParticipleExtractor(BaseExtractor):
    def extract(self, text: str) -> ExtractionResult: ...

    @property
    def name(self) -> str:
        return "participle_extractor"
