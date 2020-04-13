import yaml

from Flags.Flags import Flags


def load_params():
    with open("parameters.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def print_params(alpha, beta, gamma):
    Flags.verbose_print("---PARAMETERS---")
    Flags.verbose_print("Alpha: " + str(alpha))
    Flags.verbose_print("Beta: " + str(beta))
    Flags.verbose_print("Gamma: " + str(gamma))
    Flags.verbose_print("")


def print_response(response):
    Flags.verbose_print("--------------")
    Flags.verbose_print("   RESPONSE   ")
    Flags.verbose_print("--------------")
    Flags.verbose_print(response)
    Flags.verbose_print("")
