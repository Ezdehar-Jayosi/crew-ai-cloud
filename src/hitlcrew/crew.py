import os
import json
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from pydantic import BaseModel
from jambo import SchemaConverter


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
            llm=LLM(
                model="azure/gpt-4o",
                temperature=0.7,
            ),

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
            llm=LLM(
                model="azure/gpt-4o",
                temperature=0.7,
            ),

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
