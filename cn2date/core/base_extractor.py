import abc
from pydantic import BaseModel
from .proto import ExtractionResult


class BaseExtractor(BaseModel, abc.ABC):
    """所有提取器都必须继承的抽象基类"""

    @abc.abstractmethod
    def extract(self, text: str) -> ExtractionResult:
        """
        核心提取方法。
        参数:
            text: 输入的自然语言文本
        返回:
            ExtractionResult: 包含所有提取元素的结构化结果
        """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """返回提取器的名称"""
