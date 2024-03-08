SOWER=/home/pavery/bin/sower

# postprocess solution with sower
$SOWER -struct -merge -con ../../data_1/OUTPUT.con -mesh ../../data_1/OUTPUT.msh -result results/DGB.gdisplac.all -frequency 1 -width 20 -precision 15
$SOWER -struct -merge -con ../../data_1/OUTPUT.con -mesh ../../data_1/OUTPUT.msh -result results/DGB.stressvm.all -frequency 1 -width 20 -precision 15
