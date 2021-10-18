export nodes=$1
export rows=$2
export iterations=$3
export simCycles=$4

echo "Running traffic corelation data for and rows : " $nodes " " $rows

for i in $( eval echo {0..$(($nodes-1))})
do
    for j in $( eval echo {0..$(($nodes-1))})
    do
        if [ $i -eq $j ]; then
            continue
        fi
        for k in $( eval echo {0..$(($iterations-1))})
        do
            export out_filename="${nodes}_${i}_${j}_${k}.txt" 
            ../build/X86_DeepCorr/gem5.debug -d raw_data/"${nodes}_nodes_100"/${i}_${j} --debug-file=$out_filename --debug-flags=GarnetSyntheticTraffic2,Hello ../configs/example/garnet_synth_traffic.py --cor-p1=$i --cor-p2=$j --num-cpus=$nodes --num-dirs=$nodes --network=garnet2.0 --topology=Mesh_XY --mesh-rows=$rows --sim-cycles=$simCycles  --synthetic=uniform_random --injectionrate=0.01
        done
        rm -r raw_data/"${nodes}_nodes"/${i}_${j}/fs
    done
done



# for c-style 

# for (( i = 0; i < $nodes; i++))
# do
#     for (( j = 0; j < $nodes; j++))
#     do
#         if (($i == $j)); then
#             continue
#         fi
#         for (( k = 0; k < $iterations; k++))
#         do
#             # out_filename = "${nodes}_${i}_${j}_${k}.txt" 
#             # ../build/X86_DeepCorr/gem5.debug --debug-file=raw_dd/"${nodes}_nodes"/out_filename --debug-flags=GarnetSyntheticTraffic2,Hello ../configs/example/garnet_synth_traffic.py --cor-p1=$i --cor-p2=$j --num-cpus=4 --num-dirs=4 --network=garnet2.0 --topology=Mesh_XY --mesh-rows=2 --sim-cycles=1000  --synthetic=uniform_random --injectionrate=0.01
#             echo $i $j
#         done
#     done
# done