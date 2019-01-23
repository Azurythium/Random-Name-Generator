import random
import re

class NameGenerator:
    """
    Reads in data from a file by separating syllables and segments

    @param file: Opened file containing list of words separated by syllables
    """
    def __init__(self, file):
        # Regex that matches a syllable
        # Three segments of a syllable: onset, nucleus, and coda
        syllable_regex = re.compile(r"(y|[^aeiouy]*)([aeiouy]+|$)([^aeiouy]*)")

        # List containing dictionaries of segments read from data file.
        # Key/value pairs are (segment):(dictionary of next possible segments).
        # The four dictionaries correspond to onsets, nuclei, codas, and endings
        self.segments = [{}, {}, {}]
        self.ONSET = 0
        self.NUCLEUS = 1
        self.CODA = 2

        # Dictionary containing frequency of number of syllables.
        # Key/value pairs are (number of syllables):(frequency).
        self.nums_syllables = {}

        for line in file:
            line = line.strip()
            if not line:
                continue
            
            num_syllables = line.count("-") + 1
            if num_syllables in self.nums_syllables:
                self.nums_syllables[num_syllables] += 1
            else:
                self.nums_syllables[num_syllables] = 1

            prev_segment = None
            for syllable in line.split("-"):
                syll_segments = syllable_regex.match(syllable).groups()

                for segment_type, segment in enumerate(syll_segments):
                    # Add a previous segment to dictionary
                    if prev_segment not in self.segments[segment_type]:
                        self.segments[segment_type][prev_segment] = {}
                    frequencies = self.segments[segment_type][prev_segment]
                    # Increment frequency of next segment
                    if segment in frequencies:
                        frequencies[segment] += 1
                    else:
                        frequencies[segment] = 1
                    if segment:
                        prev_segment = segment

    """
    Returns a random key from dictionary based on frequencies

    @param dictionary: dictionary to get key from
    @return: random key weighted by frequency
    """
    def get_key(self, dictionary):
        frequencies = dictionary.values()
        index = random.randrange(sum(frequencies))
        
        for key, frequency in dictionary.items():
            if index < frequency:
                return key
            else:
                index -= frequency

    """
    Generate a random name using a Markov chain process

    @param num_syllables: number of syllables in the word
    @return: string containing a randomly generated name
    """
    def generate_name(self, num_syllables):
        prev_segment = None
        region_name = ""
        for i in range(num_syllables):
            for segment_type in [self.ONSET, self.NUCLEUS, self.CODA]:
                # If no next segment can be found, generate a new name
                try:
                    frequencies = self.segments[segment_type][prev_segment]
                except KeyError:
                    return None
                
                segment = self.get_key(frequencies)
                region_name += segment
                if segment:
                    prev_segment = segment
        if len(region_name) >= 11: # cull excessively long names
            return None
        return region_name.title()

# Main
while True:
    file_name = input("Enter file name to read data from: ")
    try:
        file = open(file_name)
    except FileNotFoundError:
        print("Error opening file, try again\n")
    else:
        break
    
generator = NameGenerator(file)
num_names = int(input("Enter number of names to generate: "))
num_generated = 0 # count number of successfully generated names
num_culled = 0 # count number of unsuccessfully generated names
while num_generated < num_names:
    num_syllables = generator.get_key(generator.nums_syllables)
    if num_syllables < 2:
        num_syllables = 2
    generated_name = generator.generate_name(num_syllables)
    if generated_name:
        print(generated_name)
        num_generated += 1
    else:
        num_culled += 1

print("Generated", num_generated, "names,", num_culled, "culled")   
# Pause at end of output
input("Press ENTER key to exit")
