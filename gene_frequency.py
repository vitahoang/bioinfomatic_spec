def count_pattern(sequence, pattern):
    count = 0
    short_len = len(pattern)
    for i in range(len(sequence) - short_len + 1):
        if sequence[i:i + short_len] == pattern:
            count += 1
    return count


# Example usage:
sequence = "GACCATCAAAACTGATAAACTACTTAAAAATCAGT"
pattern = "AAA"
frequency = count_pattern(sequence, pattern)
print(f"The frequency of '{pattern}' in '{sequence}' is {frequency}.")


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


# Example usage:
sequence = "TAAACGTGAGAGAAACGTGCTGATTACACTTGTTCGTGTGGTAT"
k = 3
result = most_frequent_kmer(sequence, k)
print(f"The most frequent {k}-mers are: {result}")


def reverse_complement(sequence):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    reverse_sequence = sequence[::-1]
    reverse_complement_sequence = ''.join(
        complement[base] for base in reverse_sequence)
    return reverse_complement_sequence


# Example usage:
sequence = "CCAGATC"
reverse_complement_seq = reverse_complement(sequence)
print(f"The reverse complement of '{sequence}' is '{reverse_complement_seq}'.")


def find_pattern_positions(sequence, pattern):
    positions = []
    pattern_length = len(pattern)
    for i in range(len(sequence) - pattern_length + 1):
        if sequence[i:i + pattern_length] == pattern:
            positions.append(i)
    return positions


# Example usage:
sequence = "ATGACTTCGCTGTTACGCGC"
pattern = "CGC"
positions = find_pattern_positions(sequence, pattern)
print("Starting positions of pattern in text (0-based indexing):", positions)
