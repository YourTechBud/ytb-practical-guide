import gepa
from baml_py import Collector
from dotenv import load_dotenv

import adapter
from baml_client import b
from my_types import Context, EvaluationResult, Example, Module, Prediction

load_dotenv()

valset = [
    Example(
        input={"query": "What tasks are pending for today?"},
        output={"action": "GetTasks"},
    ),
    Example(
        input={"query": "I finished my homework"}, output={"action": "MarkTaskAsDone"}
    ),
    Example(
        input={"query": "Please remove the completed task about cleaning"},
        output={"action": "DeleteTask"},
    ),
    Example(input={"query": "Show me my to-do list"}, output={"action": "GetTasks"}),
    Example(
        input={"query": "I need to buy a new water bottle"},
        output={"action": "AddTask"},
    ),
    Example(
        input={"query": "I'm done with my groceries"},
        output={"action": "MarkTaskAsDone"},
    ),
    Example(
        input={"query": "I don't need to buy groceries anymore"},
        output={"action": "DeleteTask"},
    ),
]

trainset = [
    Example(input={"query": "Whats the plan for today"}, output={"action": "GetTasks"}),
    Example(
        input={"query": "I cleaned up my house"}, output={"action": "MarkTaskAsDone"}
    ),
    Example(
        input={"query": "I have done my dishes for today"},
        output={"action": "MarkTaskAsDone"},
    ),
    Example(
        input={"query": "I don't need to buy a new water bottle"},
        output={"action": "DeleteTask"},
    ),
    Example(
        input={"query": "He already did the dishes for me"},
        output={"action": "DeleteTask"},
    ),
    Example(
        input={"query": "Delete the task about doing the dishes"},
        output={"action": "DeleteTask"},
    ),
]


class MyModule(Module[dict[str, str], dict[str, str]]):
    def __init__(self):
        pass

    def call(
        self, context: Context, input: dict[str, str]
    ) -> Prediction[dict[str, str]]:
        retries = 0
        while retries < 5:
            try:
                result = b.ClassifyIntent(
                    query=input["query"],
                    instructions=context.candidates["ClassifyIntent"],
                    baml_options={"collector": context.baml_collector},
                )
                break
            except Exception:
                retries += 1
                if retries == 5:
                    raise
        return Prediction(output={"action": result.action})


def metric_fn(example: Example, prediction: Prediction) -> EvaluationResult:
    example_output: dict[str, str] = example.output  # type: ignore
    prediction_output: dict[str, str] = prediction.output  # type: ignore
    score = 1.0 if example_output["action"] == prediction_output["action"] else 0.0
    feedback = {}

    if score == 0.0:
        feedback["ClassifyIntent"] = (
            f"You have incorrectly identified the user's intended action. Expected action: {example_output['action']}, but got: {prediction_output['action']}. Think about how you could have reasoned to get the correct action."
        )
    else:
        feedback["ClassifyIntent"] = (
            f"The identified action is perfect. You have correctly identified the user's intended action: {prediction.output['action']}."
        )
    return EvaluationResult(score=score, feedback=feedback)


def evaluate():
    for example in valset:
        context = Context(
            baml_collector=Collector(name="evaluation_collector"),
            candidates={
                "ClassifyIntent": "Identify the intended action from the user's query."
            },
        )
        prediction = MyModule().call(context, example.input)
        evaluation_result = metric_fn(example, prediction)
        print(f"Input: {example.input['query']}")
        print(
            f"Expected Action: {example.output['action']}, Predicted Action: {prediction.output['action']}"  # type: ignore
        )
        print(f"Score: {evaluation_result.score}")
        print(f"Feedback: {evaluation_result.feedback['ClassifyIntent']}")
        print("-" * 50)


def main():
    seed_prompt = {
        "ClassifyIntent": "Identify the intended action from the user's query.",
    }

    a = adapter.Adapter(
        program=MyModule(),
        metric=metric_fn,
    )

    # Let's run GEPA optimization process.
    gepa_result = gepa.optimize(
        seed_candidate=seed_prompt,
        display_progress_bar=True,
        adapter=a,
        trainset=trainset,
        valset=valset,
        max_metric_calls=10,  # <-- Set a budget
        reflection_lm="gemini/gemini-2.5-flash",  # <-- Use a strong model to reflect on mistakes and propose better prompts
    )

    print("Gepa Optimization Result:", gepa_result.best_candidate["ClassifyIntent"])


if __name__ == "__main__":
    main()
