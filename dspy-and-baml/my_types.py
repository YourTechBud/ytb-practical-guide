from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar

from baml_py import Collector

Input = TypeVar("Input")
Output = TypeVar("Output")


class Example(Generic[Input, Output]):
    def __init__(self, input: Input, output: Output, **extras: Any):
        self.input = input
        self.output = output
        self.extras = extras or {}

    def get_extra(self, key: str, default: Any = None) -> Any:
        return self.extras.get(key, default)


class Prediction(Generic[Output]):
    _baml_collector: Collector

    def __init__(self, output: Output):
        self.output = output


class EvaluationResult:
    def __init__(self, score: float, feedback: dict[str, str]):
        self.score = score
        self.feedback = feedback


class TraceData:
    output: Any
    input: Any
    component_name: str

    def __init__(self, output: Any, input: Any, component_name: str):
        self.output = output
        self.input = input
        self.component_name = component_name


class Trajectory(Generic[Input, Output]):
    def __init__(
        self,
        example: Example[Input, Output],
        prediction: Prediction[Output],
        traces: list[TraceData],
        feedback: dict[str, str],
        additional_context: Optional[dict[str, str]] = None,
    ):
        self.example = example
        self.prediction = prediction
        self.traces = traces
        self.feedback = feedback
        self.additional_context = additional_context


class Context:
    def __init__(
        self,
        baml_collector: Collector,
        candidates: dict[str, str],
        additional_context: Optional[dict[str, str]] = None,
    ):
        self.baml_collector = baml_collector
        self.candidates = candidates
        self.additional_context = additional_context


class Module(Generic[Input, Output], ABC):
    @abstractmethod
    def call(self, context: "Context", input: Input) -> Prediction[Output]: ...
