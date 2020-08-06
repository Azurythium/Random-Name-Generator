import random
import re

class NameGenerator:
    """
    Represents an instance of a name generator object
    """
    
    def __init__(self, file):
        """
        Reads data from an input file separated by syllables and segments

        param file (TextIOWrapper): opened file containing list of words
                                    separated by syllables
        """
        
        # regex that matches a syllable based on segments (onset, nucleus, and coda)
        print(type(file))
        syllable_regex = re.compile(r"(y|[^aeiouy]*)([aeiouy]+|$)([^aeiouy]*)")

        # list containing dictionaries of segments read from data file.
        # key/value pairs are (segment):(dictionary of next possible segments).
        # the four dictionaries correspond to onsets, nuclei, codas, and endings
        self.segments = [{}, {}, {}]
        self.ONSET = 0
        self.NUCLEUS = 1
        self.CODA = 2

        # dictionary containing frequency of number of syllables.
        # key/value pairs are (number of syllables):(frequency).
        self.nums_syllables = {}

        for line in file:
            line = line.strip()
            if not line:
                continue
            
            # count number of syllables in the line
            num_syllables = line.count("-") + 1
            if num_syllables in self.nums_syllables:
                self.nums_syllables[num_syllables] += 1
            else:
                self.nums_syllables[num_syllables] = 1

            prev_segment = None
            for syllable in line.split("-"):
                syll_segments = syllable_regex.match(syllable).groups()

                for segment_type, segment in enumerate(syll_segments):
                    # add a previous segment to dictionary
                    if prev_segment not in self.segments[segment_type]:
                        self.segments[segment_type][prev_segment] = {}
                    frequencies = self.segments[segment_type][prev_segment]
                    # increment frequency of next segment
                    if segment in frequencies:
                        frequencies[segment] += 1
                    else:
                        frequencies[segment] = 1
                    if segment:
                        prev_segment = segment

    def get_key(self, dictionary):
        """
        Returns a random key from dictionary based on frequencies

        param dictionary (dict): dictionary to get key from
        return (str): random key weighted by frequency
        """
        frequencies = dictionary.values()
        index = random.randrange(sum(frequencies))
        
        for key, frequency in dictionary.items():
            if index < frequency:
                return key
            else:
                index -= frequency

    def generate_name(self, num_syllables):
        """
        Generate a random name using a Markov chain process

        param num_syllables (int): number of syllables in the word
        return (str): string containing a randomly generated name
        """
        prev_segment = None
        region_name = ""
        for i in range(num_syllables):
            for segment_type in [self.ONSET, self.NUCLEUS, self.CODA]:
                # if no next segment can be found, generate a new name
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

# main
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

# loop to generate random names
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
# pause at end of output
input("Press ENTER key to exit")
