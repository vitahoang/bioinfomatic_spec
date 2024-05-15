
from gene_frequency import reverse_complement


def count_mismatch(str1, str2):
    count = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            count += 1
    return count


def approximate_pattern_positions(sequence, pattern, d):
    positions = []
    for i in range(len(sequence) - len(pattern) + 1):
        subsequence = sequence[i:i + len(pattern)]
        if count_mismatch(subsequence, pattern) <= d:
            positions.append(i)
    result = " ".join(map(str, positions))

    return result, len(positions)


def most_frequent_kmers_mismatches(sequence, k, d):
    kmer_counts = {}
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i+k]
        mismatches = []
        generate_mismatches(kmer, d, mismatches)
        for mismatch in mismatches:
            if mismatch in kmer_counts:
                kmer_counts[mismatch] += 1
            else:
                kmer_counts[mismatch] = 1
    max_count = max(kmer_counts.values())
    most_frequent_kmers = [kmer for kmer,
                           count in kmer_counts.items() if count == max_count]
    result = " ".join(most_frequent_kmers)
    return result


def generate_mismatches(kmer, d, mismatches, current="", index=0):
    if index == len(kmer):
        mismatches.append(current)
        mismatches.append(reverse_complement(current))
        return
    generate_mismatches(kmer, d, mismatches, current + kmer[index], index + 1)
    if d > 0:
        for nucleotide in "ACGT":
            if nucleotide != kmer[index]:
                generate_mismatches(kmer, d - 1, mismatches,
                                    current + nucleotide, index + 1)


if __name__ == "__main__":
    sequence = "AACAAGCTGATAAACATTTAAAGAG"
    pattern = "AAAAA"
    d = 2
    positions = approximate_pattern_positions(
        sequence, pattern, d)
    print("Approximate pattern positions:", positions[1])
    with open('dataset_30278_6.txt', 'r') as file:
        lines = file.read().split('\n')
    positions = approximate_pattern_positions(
        lines[1], lines[0], int(lines[2]))
    print("Approximate pattern positions:", positions[1])
