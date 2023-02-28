from classes.Context import Context
from classes.EngineActions.EngineActionInterface import EngineActionInterface


class ScrapeJobEntries(EngineActionInterface):
    @staticmethod
    def perform(context: Context):
        for job_provider in context.job_providers:
            try:
                print(job_provider)
                context.job_entries.append(job_provider.get_job_entries())
            except:
                print("Error trying to run get job enteries. ")
