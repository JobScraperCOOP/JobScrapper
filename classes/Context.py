from classes.JobProviderFactory import JobProviderFactory


def init_job_providers(companies):
    job_providers = []
    for company in companies:
        job_providers.append(JobProviderFactory.create_job_provider(company))
    return job_providers


class Context:
    def __init__(self, companies):
        self.job_providers = init_job_providers(companies)
        self.job_entries = []

