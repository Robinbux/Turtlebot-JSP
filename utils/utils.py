import yaml

from Flags.Flags import Flags
from lagrange.Lagrange import Lagrange


def load_params():
    with open("parameters.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def print_params():
    Flags.verbose_print("---PARAMETERS---")
    Flags.verbose_print("Alpha: " + str(Lagrange.alpha))
    Flags.verbose_print("Beta: " + str(Lagrange.beta))
    Flags.verbose_print("Gamma: " + str(Lagrange.gamma))
    Flags.verbose_print("")
    Flags.verbose_print("Eta: " + str(Lagrange.eta))
    Flags.verbose_print("Theta: " + str(Lagrange.theta))
    Flags.verbose_print("Iota: " + str(Lagrange.iota))
    Flags.verbose_print("Kappa: " + str(Lagrange.kappa))
    Flags.verbose_print("My: " + str(Lagrange.my))
    Flags.verbose_print("")


def print_response(response):
    Flags.verbose_print("--------------")
    Flags.verbose_print("   RESPONSE   ")
    Flags.verbose_print("--------------")
    Flags.verbose_print(response.to_pandas_dataframe().head(10))
    Flags.verbose_print("")
