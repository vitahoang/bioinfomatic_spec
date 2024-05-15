from collections import defaultdict
import time
import ray


def count_pattern(sequence, pattern):
    count = 0
    short_len = len(pattern)
    for i in range(len(sequence) - short_len + 1):
        if sequence[i:i + short_len] == pattern:
            count += 1
    return count


def most_frequent_kmer(sequence, k):
    kmer_frequency = {}
    max_frequency = 0
    most_frequent_kmers = []

    # Count the frequency of each k-mer
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        kmer_frequency[kmer] = kmer_frequency.get(kmer, 0) + 1
        max_frequency = max(max_frequency, kmer_frequency[kmer])

    # Find all k-mers with maximum frequency
    for kmer, frequency in kmer_frequency.items():
        if frequency == max_frequency:
            most_frequent_kmers.append(kmer)

    return most_frequent_kmers


def reverse_complement(sequence):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    reverse_sequence = sequence[::-1]
    reverse_complement_sequence = ''.join(
        complement[base] for base in reverse_sequence)
    return reverse_complement_sequence


def find_pattern_positions(sequence, pattern):
    positions = []
    pattern_length = len(pattern)
    for i in range(len(sequence) - pattern_length + 1):
        if sequence[i:i + pattern_length] == pattern:
            positions.append(i)
    return positions


def hamming_distance(str1, str2):
    if len(str1) != len(str2):
        raise ValueError("Strings must be of equal length")

    distance = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            distance += 1

    return distance


def min_skew_position(dna_sequence):
    min_skew = float('inf')
    min_positions = []
    skew = 0

    for i, nucleotide in enumerate(dna_sequence):
        if nucleotide == 'G':
            skew += 1
        elif nucleotide == 'C':
            skew -= 1

        if skew < min_skew:
            min_skew = skew
            min_positions = [i + 1]
        elif skew == min_skew:
            min_positions.append(i + 1)

    return min_positions


@ray.remote
def most_frequent_kmers_range(sequence, k_range):
    counts = defaultdict(int)

    for k in range(k_range[0], k_range[1] + 1):
        for i in range(len(sequence) - k + 1):
            kmer = sequence[i:i + k]
            counts[kmer] += 1

    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_counts


@ray.remote(num_cpus=10)
def create_window(sequence, L):
    for i in range(len(sequence) - L + 1):
        yield sequence[i:i + L]


def find_clumps(sequence, k, L, t):
    start_time = time.time()
    db_object_ref = ray.put(sequence)
    clumps = set()
    for window in create_window.remote(db_object_ref, L):
        patterns = most_frequent_kmers_range.remote(window, (k, k))
        valid_patterns = [pattern for pattern in ray.get(
            patterns) if pattern[1] == t]
        if valid_patterns:
            for pattern in valid_patterns:
                clumps.add(pattern)

    print(f"Execution time: {time.time() - start_time:.2f} seconds")
    return [clump[0] for clump in clumps]


if __name__ == "__main__":
    sequence = "ACGTTGCATGTCGCATGATGCATGAGAGCT"
    pattern = "CCGAACGCC"
    positions = find_pattern_positions(sequence, pattern)
    print("Starting positions of pattern in text (0-based indexing):", positions)

    str1 = "CAGAAAGGAAGGTCCCCATACACCGACGCACCAGTTTA"
    str2 = "CACGCCGTATGCATAAACGAGCCGCACGAACCAGAGAG"
    distance = hamming_distance(str1, str2)
    print("Hamming distance:", distance)

    dna_sequence = "GATACACTTCCCGAGTAGGTACTG"
    min_positions = min_skew_position(dna_sequence)
    print("Positions with minimum skew:", min_positions)

    sequence = "ACGTTGCATGTCGCATGATGCATGAGAGCT"
    k_range = (3, 5)
    result = most_frequent_kmers_range.remote(sequence, k_range)
    print("Most frequent k-mers:", ray.get(result))

    sequence = \
        "AAACTACTGGCTATCAGTACGTGCTAGGAATGTTTAACTCGCAATTCTTGACCGTATATCCAAATGTGCGTTCTTTTACCCTCATGCAATTCCTTATACCTGGCTCAGCTAAGCTTATACCTGATCTTATACCTGATACCTGCATAACTCTACCTTATATATTAGCGGATTCTGCTAATTCTGCTAGATTCTGCTATAACAGCTCAGGATGGGGGGGCGGAGCATTAGGGGGGCGGAAGGGGGGGCGGAGGGGAATGAATGGGGGGCGGAACCGCTCGCTTTGGTACGGGGGGCGGACGATGCAACAGCAGGGCGGGCATACCGGCTCTCTGGCGGTTCGGGCGGGCATACCGTACCGACGTGGCGGGGCATACCGTACGGGCATACCGAAACGCACATAATAGGGCGGTGGCATTAGGCATCAGTACACTGGCTCCCGATGTGTCTCAATCGAGGATCATCTCATCTTGATTACGTCCTGAAGGATCATCTGATCATCTTTCTAGGTTAGGATCATCTTATGGGCCAGGATCATCTGAGGATCATCTCTATGTAGTGCAGTGAGCATTTAGTTCCGGATGATCTTCTGCAGAGCTTCGCAACGAACGGCCGGTTTCTCCTGCCTGGCGTAATGATATTGTGGTCCGAGCAGGCCCTCAATGAAATTAGACGACGGTCCCGGGCGCGAACAATTGCTCAACAGAAGTCGGGACGTCTATGTCTATCCGAGTCCGGGACGGGGTGCCGCTCACATATGACAATCGTAGAGAGTCGGGTGAGTATCACAGTGTACCACTATAGATGTTACTAGAGTGTCGAACTTAGATTTTGACTTATGAACACTTCGCAGACACAACCCTAAAATTGCGCCATACAACCCTAATTGACAACCCTACAACCCTAAACAACCCTAAACCCTAACTGACATCTCAGTGTGTTTCCAATCACTATGTTCAGAAGCGCGAGGCTACTAATGCATGAATCAGACATG"
    k = 10
    L = 100
    t = 4
    result = find_clumps(sequence, k, L, t)
    print("Patterns in clumps:", result)
    ray.shutdown()
