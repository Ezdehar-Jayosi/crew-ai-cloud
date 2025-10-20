import os
import json
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from pydantic import BaseModel
from jambo import SchemaConverter

required_vars = ['AZURE_API_KEY', 'AZURE_API_BASE', 'AZURE_API_VERSION']
for var in required_vars:
    if var not in os.environ:
        print(f"Missing: {var}")
    else:
        print(f"{var}: Set")

azure_llm = LLM(
    model="azure/gpt-4",  # or your deployed model
    base_url=os.getenv("AZURE_API_BASE"),
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION")
)
@CrewBase
class mycrew:
    """UntitledProject crew"""

    @agent
    def information_collector(self) -> Agent:
        return Agent(
            config=self.agents_config["information_collector"],

            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            # llm=LLM(
            #     model="azure/gpt-4o",
            #     temperature=0.7,
            # ),
            llm=azure_llm,

        )

    @agent
    def information_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config["information_summarizer"],

            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            # llm=LLM(
            #     model="azure/gpt-4o",
            #     temperature=0.7,
            # ),
            llm=azure_llm,
        )

    @task
    def collect_personal_project_information(self) -> Task:
        return Task(
            config=self.tasks_config["collect_personal_project_information"],
            markdown=False,
            output_json=self._load_response_format("collect_personal_project_information"),
            human_input=True

        )

    @task
    def create_person_summary(self) -> Task:
        return Task(
            config=self.tasks_config["create_person_summary"],
            markdown=False,

        )

    @crew
    def crew(self) -> Crew:
        """Creates the UntitledProject crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
