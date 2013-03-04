#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: ~/code/bash/011_Map_PE_Reads_Verify_Assembly.sh <INDEX NAME> <ASSEMBLY FASTA> <READ 1> <READ 2> <MISMATCH ALLOWED>
## TODO, make the mapping range adjustable

set -o verbose

index_name=${1}
assembly_file=${2}
r1=${3}
r2=${4}
mismatch=${5}

## Build bowtie index
bowtie-build --ntoa $assembly_file $index_name

## Pass1
## Map in PE fashion, 2mismatch, 0-600bp range (output = SAM)
bowtie --sam --al "$index_name"_pass1_mapped.fq --un "$index_name"_pass1_unmapped.fq -t -I 0 -X 600 --fr -v $mismatch -p 20 "$index_name" -1 $r1 -2 $r2 "$index_name"_pass1_bowtie_out.sam  > "$index_name"_pass1_bowtie-stdout 2> "$index_name"_pass1_bowtie-stderr < /dev/null

## Pass2
## For unmapped reads in pass1, map in SE fashion, max hit = 2, identify uniq/multi/no-hit reads (output = BOWTIE)
bowtie --un "$index_name"_pass2_unmapped_1.fq -t -k 2 -v $mismatch -p 20 "$index_name" "$index_name"_pass1_unmapped_1.fq  "$index_name"_pass2_read1_bowtie_out > "$index_name"_pass2_read1_bowtie-stdout 2> "$index_name"_pass2_read1_bowtie-stderr < /dev/null
bowtie --un "$index_name"_pass2_unmapped_2.fq -t -k 2 -v $mismatch -p 20 "$index_name" "$index_name"_pass1_unmapped_2.fq  "$index_name"_pass2_read2_bowtie_out > "$index_name"_pass2_read2_bowtie-stdout 2> "$index_name"_pass2_read2_bowtie-stderr < /dev/null

## identify pairs whether they hit uniq thing or multi things
python ~/code/python/20130221_Read_1_2_Assign_Uniq_Multi_No_Hit.py "$index_name"_pass1_unmapped_1.fq "$index_name"_pass1_unmapped_2.fq "$index_name"_pass2_read1_bowtie_out "$index_name"_pass2_read2_bowtie_out / "$index_name"
## Read 1
cut -f 1 "$index_name"_pass2_read1_bowtie_out | sort | uniq -d > "$index_name"_pass2_read1_multi_hit.id
cut -f 1 "$index_name"_pass2_read1_bowtie_out | sort | uniq -u > "$index_name"_pass2_read1_unique_hit.id
## Read 2
cut -f 1 "$index_name"_pass2_read2_bowtie_out | sort | uniq -d > "$index_name"_pass2_read2_multi_hit.id
cut -f 1 "$index_name"_pass2_read2_bowtie_out | sort | uniq -u > "$index_name"_pass2_read2_unique_hit.id

## TODO fix the hardcoded ID
grep ^"@GRC076" "$index_name"_pass2_unmapped_1.fq | cut -c 2- > "$index_name"_pass2_read1_no_hit.id
grep ^"@GRC076" "$index_name"_pass2_unmapped_2.fq | cut -c 2- > "$index_name"_pass2_read2_no_hit.id

## Both/Union No-hit/uniq/multi ...
cat "$index_name"_pass2_read[1-2]_no_hit.id | cut -f 1 -d'/' | sort | uniq -d > "$index_name"_pass2_both_no_hit.id
cat "$index_name"_pass2_read[1-2]_no_hit.id | cut -f 1 -d'/' | sort | uniq > "$index_name"_pass2_union_no_hit.id

cat "$index_name"_pass2_read[1-2]_unique_hit.id | cut -f 1 -d'/' | sort | uniq -d > "$index_name"_pass2_both_unique_hit.id
cat "$index_name"_pass2_read[1-2]_unique_hit.id | cut -f 1 -d'/' | sort | uniq > "$index_name"_pass2_union_unique_hit.id

cat "$index_name"_pass2_read[1-2]_multi_hit.id | cut -f 1 -d'/' | sort | uniq -d > "$index_name"_pass2_both_multi_hit.id
cat "$index_name"_pass2_read[1-2]_multi_hit.id | cut -f 1 -d'/' | sort | uniq > "$index_name"_pass2_union_multi_hit.id

## What are these??
python ~/code/python/022_Compare_2_Sets.py "$index_name"_pass2_union_multi_hit.id "$index_name"_pass2_union_unique_hit.id "$index_name"_comp
python ~/code/python/022_Compare_2_Sets.py "$index_name"_pass2_union_multi_hit.id "$index_name"_pass2_union_no_hit.id "$index_name"_2comp
python ~/code/python/022_Compare_2_Sets.py "$index_name"_pass2_union_no_hit.id "$index_name"_pass2_union_unique_hit.id "$index_name"_3comp

## any unique hit

python ~/code/python/046_Fastq_PE_Filter_by_ID.py "$index_name"_comp*_B_* "$index_name"_for_pass3_1.fq "$index_name"_not_pass3_1.fq "$index_name"_pass1_unmapped_1.fq /
python ~/code/python/046_Fastq_PE_Filter_by_ID.py "$index_name"_comp*_B_* "$index_name"_for_pass3_2.fq "$index_name"_not_pass3_2.fq "$index_name"_pass1_unmapped_2.fq /

## Pass3
## map with unlimited range (output = bowtie)
bowtie --al "$index_name"_pass3_mapped.fq --un "$index_name"_pass3_unmapped.fq -t -I 0 -X 30000000 --fr -v $mismatch -p 20 "$index_name" -1 "$index_name"_for_pass3_1.fq -2 "$index_name"_for_pass3_2.fq "$index_name"_pass3_bowtie_out > "$index_name"_pass3_bowtie-stdout 2> "$index_name"_pass3_bowtie-stderr < /dev/null

## Pass4
## map to uniq uniq diff (in SE fashion) (output = bowtie)
bowtie --al "$index_name"_pass4_mapped_1.fq -t -v $mismatch -p 20 "$index_name" "$index_name"_pass3_unmapped_1.fq  "$index_name"_pass4_read1_bowtie_out > "$index_name"_pass4_read1_bowtie-stdout 2> "$index_name"_pass4_read1_bowtie-stderr < /dev/null
bowtie --al "$index_name"_pass4_mapped_2.fq -t -v $mismatch -p 20 "$index_name" "$index_name"_pass3_unmapped_2.fq  "$index_name"_pass4_read2_bowtie_out > "$index_name"_pass4_read2_bowtie-stdout 2> "$index_name"_pass4_read2_bowtie-stderr < /dev/null

## Pass5
## Same as pass3, map with unlimited range (output = SAM)
bowtie -t -I 0 -X 30000000 --fr -v $mismatch -p 20 --sam "$index_name" -1 "$index_name"_pass3_mapped_1.fq -2 "$index_name"_pass3_mapped_2.fq "$index_name"_pass5_bowtie_out.sam > "$index_name"_pass5_bowtie-stdout 2> "$index_name"_pass5_bowtie-stderr < /dev/null
## Same as pass5, map with unlimited range (output = BOWTIE)
bowtie -t -I 0 -X 30000000 --fr -v $mismatch -p 20 "$index_name" -1 "$index_name"_pass3_mapped_1.fq -2 "$index_name"_pass3_mapped_2.fq "$index_name"_pass5_bowtie_out > "$index_name"_pass5_bowtie-stdout_2 2> "$index_name"_pass5_bowtie-stderr_2 < /dev/null

## Pass6 (remap?)
## these are unique mappable reads which cannot be mapped to the same contig
bowtie -t -v $mismatch -p 20 "$index_name" "$index_name"_pass4_mapped_1.fq "$index_name"_pass6_read1_bowtie_out_remap > "$index_name"_pass6_read1_bowtie-stdout_remap 2> "$index_name"_pass6_read1_bowtie-stderr_remap < /dev/null
bowtie -t -v $mismatch -p 20 "$index_name" "$index_name"_pass4_mapped_2.fq "$index_name"_pass6_read2_bowtie_out_remap > "$index_name"_pass6_read2_bowtie-stdout_remap 2> "$index_name"_pass6_read2_bowtie-stderr_remap < /dev/null
## Identify Uniq-Uniq and Uniq-No-hit
cut -f 1 "$index_name"*tie_out_remap | cut -f 1 -d '/' | sort | uniq -d > "$index_name"_uniq_uniq_diff_contig.id
cut -f 1 "$index_name"*tie_out_remap | cut -f 1 -d '/' | sort | uniq -u > "$index_name"_uniq_no-hit.id

## Obtain the Uniq-Uniq-Diff-Contig Reads
python ~/code/python/046_Fastq_PE_Filter_by_ID.py "$index_name"_uniq_uniq_diff_contig.id "$index_name"_uniq_uniq_diff_contig_1.fq - "$index_name"_pass4_mapped_1.fq /
python ~/code/python/046_Fastq_PE_Filter_by_ID.py "$index_name"_uniq_uniq_diff_contig.id "$index_name"_uniq_uniq_diff_contig_2.fq - "$index_name"_pass4_mapped_2.fq /
cat "$index_name"_uniq_uniq_diff_contig_1.fq "$index_name"_uniq_uniq_diff_contig_2.fq > "$index_name"_uniq_uniq_diff_contig_c1+2.fq

## Obtain the Uniq-No-Hit reads
python ~/code/python/046_Fastq_PE_Filter_by_ID.py "$index_name"_uniq_no-hit.id "$index_name"_uniq_no-hit_1.fq - "$index_name"_pass4_mapped_1.fq /
python ~/code/python/046_Fastq_PE_Filter_by_ID.py "$index_name"_uniq_no-hit.id "$index_name"_uniq_no-hit_2.fq - "$index_name"_pass4_mapped_2.fq /
cat "$index_name"_uniq_no-hit_1.fq "$index_name"_uniq_no-hit_2.fq > "$index_name"_uniq_no-hit_c1+2.fq

## Pass7
## Map the uniq-uniq-diff-contig reads (Output = SAM)
bowtie -t -v $mismatch -p 20 --sam "$index_name" "$index_name"_uniq_uniq_diff_contig_c1+2.fq "$index_name"_uniq_uniq_diff_contig_c1+2.sam > "$index_name"_uniq_uniq_diff_contig_c1+2_bowtie-stdout 2> "$index_name"_uniq_uniq_diff_contig_c1+2_bowtie-stderr < /dev/null

## Pass8
## Map the uniq-no-hit reads (Output = SAM)
bowtie -t -v $mismatch -p 20 --sam "$index_name" "$index_name"_uniq_no-hit_c1+2.fq "$index_name"_uniq_no-hit_c1+2.sam > "$index_name"_uniq_no-hit_c1+2_bowtie-stdout 2> "$index_name"_uniq_no-hit_c1+2_bowtie-stderr < /dev/null

# this is quite different in KY v.s. NICK, why?
cut -f 1-2 "$index_name"_pass1_bowtie_out | cut -f 2 -d'/' | sort | uniq -c > "$index_name"_pass1.direction

python ~/code/python/20130221_Read_1_2_Assign_Uniq_Multi_No_Hit.py "$index_name"_pass1_unmapped_1.fq "$index_name"_pass1_unmapped_2.fq "$index_name"_pass2_read1_bowtie_out "$index_name"_pass2_read2_bowtie_out / "$index_name" 

## 50 is the read length
python /home/klui/code/python/20130221_PE_Bowtie_Out_To_Insert_Size_Distribution.py "$index_name"_pass3_bowtie_out "$index_name"_pass3.insert_size 50
sort -k 2 -t $'\t' -n -r "$index_name"_pass3.insert_size > "$index_name"_pass3.insert_size.sorted

python /home/klui/code/python/20130221_PE_Bowtie_Out_To_Insert_Size_Distribution.py "$index_name"_pass1_bowtie_out "$index_name"_pass1.insert_size 50
sort -k 2 -t $'\t' -n -r "$index_name"_pass1.insert_size > "$index_name"_pass1.insert_size.sorted

ls "$index_name"_pass1_bowtie_out.sam "$index_name"_pass5_bowtie_out.sam "$index_name"_uniq_uniq_diff_contig_c1+2.sam "$index_name"_uniq_no-hit_c1+2.sam | while read file_name
do
   base_name=`basename $file_name .sam`
   samtools view -bS $file_name > "$base_name".bam
   samtools sort "$base_name".bam "$base_name".sorted
   samtools index "$base_name".sorted.bam
done

## Create symbolic links
ln -s "$index_name"_pass1_bowtie_out.sorted.bam "$index_name"_properly_mapped.bam
ln -s "$index_name"_pass1_bowtie_out.sorted.bam.bai "$index_name"_properly_mapped.bam.bai
ln -s "$index_name"_pass5_bowtie_out.sorted.bam "$index_name"_out_of_range.bam
ln -s "$index_name"_pass5_bowtie_out.sorted.bam.bai "$index_name"_out_of_range.bam.bai

## mpileup
samtools mpileup "$index_name"_properly_mapped.bam > "$index_name"_properly_mapped.mpileup
samtools mpileup "$index_name"_out_of_range.bam > "$index_name"_out_of_range.mpileup
samtools mpileup "$index_name"_uniq_uniq_diff_contig_c1+2.sorted.bam > "$index_name"_uniq_uniq_diff_contig.mpileup
samtools mpileup "$index_name"_uniq_no-hit_c1+2.sorted.bam > "$index_name"_uniq_no-hit.mpileup

## Create cut sites
python ~/code/python/047-2A_Mpileup_Highlight_To_GFF_UniqUniqSame.py "$index_name"_out_of_range.mpileup "$index_name"_uniq_uniq_same_contig CutSite1 3.0 300
python ~/code/python/047-2B_Mpileup_Highlight_To_GFF_UniqUniqDiff.py "$index_name"_uniq_uniq_diff_contig.mpileup "$assembly_file".python007.len "$index_name"_uniq_uniq_diff_contig CutSite2 3.0 300


python ~/code/python/047-2B_Mpileup_Highlight_To_GFF_UniqUniqDiff.py "$index_name"_uniq_no-hit.mpileup "$assembly_file".python007.len "$index_name"_uniq_no-hit CutSite3 3.0 300

python ~/code/python/047-3_Merge_GFF.py "$index_name"_Merged "$assembly_file".python007.len "$index_name"*cut*3

## Create Useful cut product
python ~/code/python/047-4_GFF_To_044_Input.py "$index_name"_NewMerged ../../../00FirstAssessment/best922.python007.len "$index_name"_Merged.py047-3.gff3

## Identify Repeat
python ~/code/python/050_Mpileup_Highlight_Region_By_Coverage.py "$index_name"_properly_mapped.mpileup "$index_name"_properly_mapped REPEAT 200 100
cut -f 1,4,5 "$index_name"_properly_mapped.py050.cut_site.gff3 > "$index_name"_repeat
python ~/code/python/044_Fasta_Select_Bases_In_Range.py "$index_name"_repeat "$index_name"_repeat.fa $assembly_file

## Some output...
grep "#" "$index_name"*_pass3_bowtie-stderr

echo "To different contig"
cat "$index_name"*pass4*_out | cut -f 1 -d'/' | sort | uniq -d | wc -l

echo "One read does not map"
cat "$index_name"*pass4*_out | cut -f 1 -d'/' | sort | uniq -u | wc -l
