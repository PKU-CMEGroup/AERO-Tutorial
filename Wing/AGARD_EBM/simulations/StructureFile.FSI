CONTROL
Structure
1
StructureNodes
StructureElementsS
********************************************************************
AERO
*C0 0.5 0.375
A6 0.5 0.125
MATCHER "../../data/fluidmodel.match.fem"
********************************************************************
MASS
********************************************************************
TRBM
1.0E-09
********************************************************************
NONLINEAR
********************************************************************
STATIC
* sparse
MUMPS PIVOT
MUMPS_ICNTL 14 200
******************************************************************
* specify the type of node renumbering for skyline and sparse solvers
* RENUM
* rcm
********************************************************************
DYNAMICS
NEWMARK
MECH          0.25  0.50
TIME          0.0   0.5e-4  0.1
**************************************************************************
OUTPUT
GDISPLAC "postpro.FSI/structure.GDISPLAC.xpost" 100
**********************************************************************
OUTPUT6
GDISPLAC "postpro.FSI/structure.GDISPLAC.111" 1 111
GDISPLAC "postpro.FSI/structure.GDISPLAC.116" 1 116
GDISPLAC "postpro.FSI/structure.GDISPLAC.121" 1 121
********************************************************************
INCLUDE "StructureFile.include"
INCLUDE "StructureFile.composite"
********************************************************************
END
********************************************************************
