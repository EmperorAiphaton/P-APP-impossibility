from FormulaConstructor import FormulaConstructor
import argparse

if __name__ == '__main__':
    """This function parses the command line input and builds the logical formula accordingly."""
    description = "This program computes a logical formula specifying a P-APP voting rule that satisfies anonymity, strategy-proofness, and weak representation. " \
                 "This code is the basis for the paper \"Strategy-proofness and Proportionality in Party-Approval Multi-winner Elections\" Theo Delemazure, " \
                 "Tom Demeulemeester,  Manuel Eberl, Jonas Israel, and Patrick Lederer [1]"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("OutputFile", type=str, help="Specifies the file in which the logical formula will be written")
    parser.add_argument("-k", type=int, help="size of the committee k (k=3 by default)", default=3)
    parser.add_argument("-m", type=int, help="number of parties m (m=4 by default)", default=4)
    parser.add_argument("-n", type=int, help="number of voters n (n=6 by default)", default=6)

    parser.add_argument("--SymmetryBreaking", type=bool,
                        help="If on, the program will encode the symmtery-breaking as specified by Lemma 2 in [1]; if m or n are modified this should be off"
                             "(by default on if m or n is not speified; otherwise off)")

    parser.add_argument("--PO", help="If specified, the program will additionally encode that the P-APP voting rule satisfies Pareto-optimality (by default off)",
                        action="store_true", default=False)
    parser.add_argument("--naive", help ="If specified, the program will use a naive implementation of weak representation instead of the variant specified in "
                                         + "Lemma 1 (by default off)", action="store_true", default=False)
    parser.add_argument("--allprofiles", help="If specified, the program will consider the domain of all profiles; otherwise, we will focus on the "
                                               + "domain A_{SAT} specified in [1]", action="store_true", default=False)
    parser.add_argument("--SATsolve", help="If specified, the program will evaluate whether the constructed formula is true; "
                                            + "this requires the pycosat package (by default off)", action="store_true", default=False)

    args = parser.parse_args()

    if args.SymmetryBreaking is None and (args.k!=3 or args.m!=4 or args.n!=6):
        args.SymmetryBreaking=False
    else:
        args.SymmetryBreaking=True
    formula_constructor = FormulaConstructor(args.k, args.m, args.n, args.PO, args.naive, args.allprofiles)
    formula_constructor.write_formula(args.OutputFile, args.SATsolve, args.SymmetryBreaking)
