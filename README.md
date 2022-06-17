# Supplementray material for the paper "Strategy-Proofness and Proportionality in Party-Approval Multi-Winner Voting" by Theo Delemazure, Tom Demeulemeester, Manuel Eberl, Jonas Israel, and Patrick Lederer 

This repository contains the code for generating a logical formula that encodes a party-approval multi-winner voting rule that satisfies anonymity, strategy-proofness and weak representation. The formula will be written in an output file in the dimacs format. Thus, the satisfiability can be checked by handing the output file to a SATsolver (such as glucose or minisat) and minimal unsatisfiable sets can be computed by handing the file to MUS extractors (such as muser2 or haifa_muc). In summary, the code allows to verify Proposition 1 of Delemazure et al. [1] by checking the code and reproducing the impossibilty.

## Usage

The repository contains a commandline tool, which writes a logical formula into the output file in dimacs format. The logical formula encodes a party-approval voting rule satisfying anonymity, weak representation, and strategy-proofness. Note that our code allows for flexibility beyond just verifying Proposition 1 of Delemazure et al. [1] by allowing variuos parameters. Our code requires python 3.9 or later and the packages numpy and pycosat.

For installing the dependencies, run the following command. 

<pre>
pip install -r requirements.txt
</pre>

<pre> 
Usage: EncodePAPPElections.py [-h] [-k K] [-m M] [-n N] [--SymmetryBreaking SYMMETRYBREAKING] [--PO] [--naive] [--allprofiles] [--SATsolve] OutputFile

Positional arguments:
  OutputFile                 Specifies the file in which the logical formula will be written` 


optional arguments:
  -h, --help                 show this help message and exit
  -k K                       size of the committee k (k=3 by default)
  -m M                       number of parties m (m=4 by default)
  -n N                       number of voters n (n=6 by default)
  --SymmetryBreaking SB      If on, the program will encode the symmtery-breaking as specified by Lemma 2 in [1]; 
                             if m or n are modified this should be off(by default on if m or n is not speified; otherwise off)
  --PO                       If specified, the program will additionally encode that the P-APP voting rule satisfies 
                             Pareto-optimality (by default off)
  --naive                    If specified, the program will use a naive implementation of weak representation instead of the 
                             variant specified in Lemma 1 (by default off)
  --allprofiles              If specified, the program will consider the domain of all profiles; otherwise, we will focus on the 
                             domain A_{SAT} specified in [1]
  --SATsolve                 If specified, the program will evaluate whether the constructed formula is true; 
                             this requires the pycosat package (by default off)
</pre>

## Example

The simplest use of our program is without any optional parameter. This will compute the formula required for proving Proposition 1 in [1].

<pre>
python3 EncodePAPPElections.py formula.cnf
</pre>

Moreover, the program also supports different numbers of voters, parties, and seats of the committee. For instance, the following example encodes a P-APP voting rule satisfying anonymity, strategy-proofness, and weak representation for m=3, n=3, k=3. Also, we activated the SATsolve option, which means that the program will automatically apply a SAT solver to check whether formula is satisfiable and print the result. For the given parameters, the corresponding formula is shown to be satisfiable. 

<pre>
python3 EncodePAPPElections.py -k 3 -m 3 -n 3 --SATsolve formula.cnf
</pre>

As last example, we note that we can also modify the axioms and how axioms are encoded. For instance, the following example uses additionally Pareto-optimality, but does not use Lemma 1 for a more advanced encoding of weak representation. Also, we modified the domain in this example by not using the tie-breaking as described in Lemma 2 of [1]

<pre>
python3 EncodePAPPElections.py --P0 --naive --SymmetryBreaking False formula.cnf
</pre>
