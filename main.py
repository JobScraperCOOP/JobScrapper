from classes.Company import Company
from classes.Context import Context
from classes.EngineActions.ScrapeJobEntries import ScrapeJobEntries


def run_engine():
    companies = [company for company in Company]
    engine_actions = [ScrapeJobEntries]

    context = Context(companies)
    for action in engine_actions:
        action.perform(context)


if __name__ == "__main__":
    run_engine()






