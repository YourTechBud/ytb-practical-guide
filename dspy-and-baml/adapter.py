from typing import Any, Callable, Union

from baml_py import Collector
from gepa.core.adapter import EvaluationBatch, GEPAAdapter

from my_types import (
    Context,
    EvaluationResult,
    Example,
    Module,
    Prediction,
    TraceData,
    Trajectory,
)


class Adapter(GEPAAdapter[Example, Trajectory, Prediction]):
    def __init__(
        self,
        program: Union[Module, Callable[[Example], Module]],
        metric: Callable[[Example, Prediction], EvaluationResult],
    ):
        self.program = program
        self.metric = metric

    def evaluate(
        self,
        batch: list[Example],
        candidate: dict[str, str],
        capture_traces: bool = False,
    ) -> EvaluationBatch[Trajectory, Prediction]:
        outputs: list[Prediction] = []
        scores: list[float] = []
        trajectories: list[Trajectory] | None = [] if capture_traces else None

        for data in batch:
            # First prepare the context object
            baml_collector = Collector(name="evaluation_collector")
            context = Context(baml_collector=baml_collector, candidates=candidate)

            # First get the module instance
            if isinstance(self.program, Module):
                program_instance = self.program
            else:
                program_instance = self.program(data)

            output = program_instance.call(context, data.input)
            output._baml_collector = baml_collector

            outputs.append(output)

        for data, output in zip(batch, outputs, strict=False):
            evaluation_result = self.metric(data, output)
            scores.append(evaluation_result.score)

            if capture_traces and trajectories is not None:
                # Get all traces from the collector
                traces: list[TraceData] = []
                for log in output._baml_collector.logs:
                    trace = TraceData(
                        component_name=log.function_name,
                        input=log.calls[-1].http_request.body.text(),  # type: ignore
                        output=log.calls[-1].http_response.body.text(),  # type: ignore
                    )
                    traces.append(trace)

                trajectories.append(
                    Trajectory(
                        example=data,
                        prediction=output,
                        feedback=evaluation_result.feedback,
                        traces=traces,
                    )
                )

        print("========= Evaluation Summary =========")
        print("Evaluation scores:", scores)
        print("Length of outputs:", len(outputs), len(scores))
        print(
            "trajectories:",
            len(trajectories) if trajectories else "No trajectories captured",
        )
        print("======================================")
        return EvaluationBatch(
            outputs=outputs, scores=scores, trajectories=trajectories
        )

    def make_reflective_dataset(
        self,
        candidate: dict[str, str],
        eval_batch: EvaluationBatch[Trajectory, Prediction],
        components_to_update: list[str],
    ) -> dict[str, list[dict[str, Any]]]:
        ret_d: dict[str, list[dict[str, Any]]] = {}

        print("Components to update:", components_to_update)

        for component_name in components_to_update:
            items: list[dict[str, Any]] = []
            if eval_batch.trajectories is None:
                continue
            for traj in eval_batch.trajectories:
                for trace in traj.traces:
                    if trace.component_name != component_name:
                        continue
                    item = {
                        "Inputs": trace.input,
                        "Generated Outputs": trace.output,
                        "Feedback": traj.feedback[component_name]
                        if component_name in traj.feedback
                        else "No feedback provided",
                    }
                    items.append(item)
            ret_d[component_name] = items

        return ret_d
