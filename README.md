# Supplementray material for the paper "Strategyproofness and Proportionality in Party-Approval Multi-Winner Voting"

This repository contains the code for generating a logical formula that encodes a party-approval multi-winner voting rule that satisfies anonymity, strategyproofness and weak representation. The formula will be written in an output file in the dimacs format. Thus, the satisfiability can be checked by handing the output file to a SATsolver (such as glucose or minisat) and minimal unsatisfiable sets can be computed by handing the file to MUS extractors (such as muser2 or haifa_muc). In summary, the code allows to verify Proposition 1 of Delemazure et al. [1] by checking the code and reproducing the impossibilty.

## Usage

The repository contains a commandline tool, which writes a logical formula into the output file in dimacs format. The logical formula encodes a party-approval voting rule satisfying anonymity, weak representation, and strategyproofness. Note that our code allows for flexibility beyond just verifying Proposition 1 of Delemazure et al. [1] by allowing variuos parameters. Our code requires python 3.9 or later and the packages numpy and pycosat.

For installing the dependencies, run the following command. 

<pre>
pip install -r requirements.txt
</pre>

<pre> 
Usage: EncodePAPPElections.py [-h] [-k K] [-m M] [-n N] [--cleverWR] [--SymmetryBreaking] [--PO] [--allprofiles] [--SATsolve] OutputFile

positional arguments:
  OutputFile          Specifies the file in which the logical formula will be written

optional arguments:
  -h, --help          show this help message and exit
  -k K                size of the committee k (k=3 by default)
  -m M                number of parties m (m=4 by default)
  -n N                number of voters n (n=6 by default)
  --cleverWR          If specified, the program will additionally encode the constraints specified in Lemma 2 in the appendix of [1] (by default off)
  --SymmetryBreaking  If specified, the program will encode the symmtery-breaking as specified by Lemma 3 in the appendix of [1]; if m or n are modified this should be off (by default off)
  --PO                If specified, the program will additionally encode that the P-APP voting rule satisfies Pareto-optimality (by default off)
  --allprofiles       If specified, the program will consider the domain of all profiles; otherwise, we will focus on the domain A_{SAT} specified in [1]
  --SATsolve          If specified, the program will evaluate whether the constructed formula is true; this requires the pycosat package (by default off)
</pre>

## Example

The simplest use of our program is without any optional parameter. This will compute the formula required for proving Proposition 1 in [1].

<pre>
python3 EncodePAPPElections.py formula.cnf
</pre>

Moreover, the program also supports different numbers of voters, parties, and seats of the committee. For instance, the following example encodes a formula specifying a P-APP voting rule that satisfies anonymity, strategyproofness, and weak representation for m=3, n=3, k=3. Also, we activated the SATsolve option, which means that the program will automatically apply a SAT solver to check whether formula is satisfiable and print the result. For the given parameters, the corresponding formula is shown to be satisfiable. 

<pre>
python3 EncodePAPPElections.py -k 3 -m 3 -n 3 --SATsolve formula.cnf
</pre>

As last example, we note that our code also supports the optimizations discussed in the appendix of [1]. In particular, the following command was used to compute the formula from which the proof of Proposition 2 in the appendix of [1] was extracted.

<pre>
python3 EncodePAPPElections.py --P0 --cleverWR --SymmetryBreaking formula.cnf
</pre>

## Architecture

Our code is split up in 5 classes. Subsequently we roughly describe the functionality of each class.

<pre>
EncodePAPPElections.py            This is the interface of our architecture. The class itself only offers a main function, which 
                                  handles the console input and then calls the FormulaConstructor class. 
FormulaConstructor.py             This class is responsible for the main functionality of our software: it computes the logical 
                                  formula for which we want to check whether it is satisfiable or not. For this it relies on 
                                  three auxiliary classes: AxiomHelper.py, DataManager.py, and PAPPElectionBuilder.py.
PAPPElectionBuilder.py            This class contains the functionality to compute the set of all approval ballots, committees, 
                                  and approval profiles for the given input parameters m, n, and k. 
AxiomHelper.py                    This class contains several helper methods for encoding weak representation and Pareto-optimality.
                                  In particular, we compute here for each preference profile which committees are feasible given 
                                  weak representation, Pareto-optimality, etc.
DataManager.py                    This class contains functionality for handling our data. In particular, this method offers functions
                                  to compute the variable for a given approval profile and committee and to decide when a voter prefers
                                  a committee to another one. 
</pre>

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
