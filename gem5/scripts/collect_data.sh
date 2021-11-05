export nodes=$1
export rows=$2
export iterations=$3
export simCycles=$4
export dest_folder=$5
export traffic_prob=$6
export apply_cf=$7
export apply_delay=$8

echo "Running traffic corelation data for and rows : " $nodes " " $rows

export is_apply_cf=false
export cw=""
export cw_flag=""
if [[ "$apply_cf" == "-cw" ]]; then
    is_apply_cf=true 
    cw="c"
    cw_flag="--enable-add-chaff"
fi

export delay=""
export delay_flag=""
if [[ "$apply_delay" == "-delay" ]]; then
    delay="d"
    delay_flag="--enable-add-delay"
fi


for i in $( eval echo {0..$(($nodes-1))})
do
    for j in $( eval echo {0..$(($nodes-1))})
    do
        if [[ ("$is_apply_cf" = true ) && (($j -eq $(($i-1))) || ($j -eq $(($i+1))) || ($j -eq $(($i+$rows))) || ($j -eq $(($i-$rows))))]]; then
            continue
        fi
        if [ $i -eq $j ]; then
            continue
        fi
        for k in $( eval echo {0..$(($iterations-1))})
        do
            export out_filename="${nodes}_${i}_${j}_${k}.txt" 
            ../build/X86_DeepCorr/gem5.debug -d $dest_folder/"${nodes}_nodes_${traffic_prob}_${cw}${delay}"/${i}_${j} --debug-file=$out_filename --debug-flags=GarnetSyntheticTraffic2,Hello ../configs/example/garnet_synth_traffic.py --cor-p1=$i --cor-p2=$j --cor-prec=$traffic_prob --num-cpus=$nodes --num-dirs=$nodes --network=garnet2.0 --topology=Mesh_XY --mesh-rows=$rows --sim-cycles=$simCycles  --synthetic=uniform_random --injectionrate=0.01  $cw_flag  $delay_flag
        done
        rm -r $dest_folder/"${nodes}_nodes_${traffic_prob}_${cw}${delay}"/${i}_${j}/fs
        rm -r $dest_folder/"${nodes}_nodes_${traffic_prob}_${cw}${delay}"/${i}_${j}/*.dot
        rm -r $dest_folder/"${nodes}_nodes_${traffic_prob}_${cw}${delay}"/${i}_${j}/*.pdf
        rm -r $dest_folder/"${nodes}_nodes_${traffic_prob}_${cw}${delay}"/${i}_${j}/*.svg
        rm -r $dest_folder/"${nodes}_nodes_${traffic_prob}_${cw}${delay}"/${i}_${j}/*.ini
        rm -r $dest_folder/"${nodes}_nodes_${traffic_prob}_${cw}${delay}"/${i}_${j}/*.json
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