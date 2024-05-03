from gene_frequency import most_frequent_kmers_range, find_pattern_positions, \
    find_clumps
from util import read_text_file

file_name = "Vibrio_cholerae.txt"
sequence = read_text_file(file_name)

top_frequency = most_frequent_kmers_range(sequence=sequence, k_range=(15, 20))
print(top_frequency)

positions = find_pattern_positions(sequence=sequence, pattern="CTTGATCAT")
print(positions)

sequence = read_text_file("E_coli.txt")
clump = find_clumps(sequence, 9, 500, 3)
print("final: {clump}")
