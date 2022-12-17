import logging

from classes.Company import Company
from classes.Elbit import Elbit
from classes.Iai import Iai
from classes.Refael import Refael


class JobProviderFactory:
    @classmethod
    def create_job_provider(cls, company: Company):
        if company is None:
            logging.warning('JobProviderFactory: received null \'company\' parameter')
            return

        if company == Company.ELBIT:
            return Elbit()
        elif company == Company.IAI:
            return Iai()
        elif company == Company.REFAEL:
            return Refael()
