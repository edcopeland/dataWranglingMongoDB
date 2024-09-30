# It is, a matter of fact, a collection of a lot of concatenated XML documents.
# So, one solution would be to split the file into separate documents,
# so that you can process the resulting files as valid XML documents.

import xml.etree.ElementTree as ET
PATENTS = 'patent.data'
patent_start_line = '<?xml version="1.0" encoding="UTF-8"?>'

def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def split_file(filename):
    """
    Split the input file into separate files, each containing a single patent.
    As a hint - each patent declaration starts with the same line that was
    causing the error found in the previous exercises.
    <?xml version="1.0" encoding="UTF-8"?>
    The new files should be saved with filename in the following format:
    "{}-{}".format(filename, n) where n is a counter, starting from 0.
    """
    with open(filename, 'r') as file:
        content = file.read()
        
        patent_lst = content.split(patent_start_line)
        
        for n, patent in enumerate(patent_lst):
            if patent.strip():
            
                new_filename = "{}-{}".format(filename, n-1)
            
                with open(new_filename, 'w') as patent_file:
                    patent_file.write(patent_start_line + patent)


def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print ("You have not split the file {} in the correct boundary!".format(fname))
            f.close()
        except:
            print ("Could not find file {}. Check if the filename is correct!".format(fname))

test()