export nodes=$1
export rows=$2
export iterations=$3
export simCycles=$4
export dest_folder=$5
export apply_cf=$6

echo "Running traffic corelation data for and rows : " $nodes " " $rows

export is_apply_cf=false
if [[ "$apply_cf" == "-cw" ]]; then
    is_apply_cf=true 
fi


if [ "$is_apply_cf" = true ]; then
            echo "ssss"
fi


for i in $( eval echo {0..$(($nodes-1))})
do
    for j in $( eval echo {0..$(($nodes-1))})
    do
        if [[ ("$is_apply_cf" = true ) && (($j -eq $(($i-1))) || ($j -eq $(($i+1))) || ($j -eq $(($i+$rows))) || ($j -eq $(($i-$rows))))]]; then
            echo $i $j
        fi
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