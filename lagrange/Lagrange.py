import yaml


class Lagrange:
    """Static Lagrange parameters"""

    # Classical Constraints
    alpha = 1
    beta = 1
    gamma = 1

    # Optimization
    delta = 1
    epsilon = 1
    zeta = 1

    # Turtlebot Constraints
    eta = 1
    theta = 1
    iota = 1
    kappa = 1
    my = 1

    @staticmethod
    def load_params():
        with open("parameters.yaml", 'r') as stream:
            try:
                params = yaml.safe_load(stream)
                Lagrange.alpha = params["alpha"]
                Lagrange.beta = params["beta"]
                Lagrange.gamma = params["gamma"]

                Lagrange.delta = params["delta"]
                Lagrange.epsilon = params["epsilon"]
                Lagrange.zeta = params["zeta"]

                Lagrange.eta = params["eta"]
                Lagrange.theta = params["theta"]
                Lagrange.iota = params["iota"]
                Lagrange.kappa = params["kappa"]
                Lagrange.my = params["my"]
            except yaml.YAMLError as exc:
                print(exc)
