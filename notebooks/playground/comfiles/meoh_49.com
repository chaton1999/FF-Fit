%nproc=4
%mem=5760MB
%chk=meoh_49.chk
#P PBE1PBE/aug-cc-pVDZ scf(maxcycle=200) 

Gaussian input

0 1
O 1.4313 -0.0105 -0.0008
C 0.0087 0.0016 -0.0000
H 1.7211 0.9257 0.0010
H -0.3673 -1.0215 0.0002
H -0.3582 0.5146 0.8889
H -0.3587 0.5140 -0.8891

