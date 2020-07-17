from JSPConstraint.JSPConstraint import JSPConstraint


def main(args=None):
    jsp_constraint = JSPConstraint()

    operation_results = {
        0: 0,
        1: 3,
        2: 9,
        3: 3,
        4: 7,
        5: 11,
        6: 0,
        7: 5,
        8: 10,
        9: 0,
        10: 4,
        11: 10,
        14: 1,
        15: 5,
        19: 5,
        23: 9,
        24: 2,
        28: 7,
        31: 1,
        35: 6
    }

    jsp_constraint.plot_operations__TEMP(operation_results)






if __name__ == "__main__":
    main()