

##################################
## Initializing Testing Program ##
##################################
import unittest
import re

#################################
## Beginning of Code Functions ##
#################################

#Error message is returned rather than printed.
def inputCheck(string,check=True):
    text = None
    while True:
        text = string
        if len(text) == 0:
            return ("Error, no input given\n")
        if not text.isalpha() and check:
            return ("Error, cannot include numbers or punctuation.\n")
        break
    return text

def getListFromFile(filename):
  try:
    file = open(filename)
  except:
    print("Error, dictionary file does not exist.")
    exit(0)
  lines = file.readlines()
  for line in range(len(lines)):  
    lines[line] = lines[line].strip()
    if lines[line] == "":
      lines.pop(line)
  file.close()
  if len(lines) == 0: 
    print("Error, file is empty.")
    exit(0)
  return lines

def same(item, target):
  return len([itemLetter for (itemLetter, targetLetter) in zip(item, target) if itemLetter == targetLetter])

def build(pattern, words, seen, potentialNextWords):
  return [word for word in words if re.search(pattern, word) and word not in seen.keys() and word not in potentialNextWords]

#Needed to alter the return values and introduce a new parameter called recursiveRun which is true when the function is in a recursion, and false when it is the first time being called. This allows the function to return the path if it is a one step solution.
def find(word, words, seen, target, path, recursiveRun= False):
  potentialNextWords = []
  fixedIndexes=[i for i in range(len(word)) if word[i] == target[i]] 
  for i in [index for index in range(len(word)) if index not in fixedIndexes]: 
    potentialNextWords += build(word[:i] + "." + word[i + 1:], words, seen, potentialNextWords)
  if len(potentialNextWords) == 0: 
    return False
  potentialNextWords = sorted([(same(word, target), word) for word in potentialNextWords], reverse=True) 
  for (match, item) in potentialNextWords:
    if match >= len(target) - 1:
      if match == len(target) - 1:
        path.append(item)
      if not recursiveRun:
        return path
      else:
        return True
    seen[item] = True
  for (match, item) in potentialNextWords: 
    path.append(item)
    if find(item, words, seen, target, path, True):
      return path
    path.pop()

###############################
## Beginning of Testing Code ##
###############################

class TestFileNameInputAndHandling(unittest.TestCase):
    def test_invalidFile(self):
        self.assertRaises((SystemExit, FileNotFoundError),getListFromFile,'bad')

    def test_emptyFile(self):
        self.assertRaises(SystemExit,getListFromFile,'blank.txt')

class TestCheckWordInput(unittest.TestCase):
    def test_punctuation(self):
        self.assertEqual(inputCheck('word.'), "Error, cannot include numbers or punctuation.\n")

    def test_numbers(self):
        self.assertEqual(inputCheck('word4'), "Error, cannot include numbers or punctuation.\n")

    def test_spaces(self):
        self.assertEqual(inputCheck('word word'), "Error, cannot include numbers or punctuation.\n")

    def test_correctInput(self):
        self.assertEqual(inputCheck('word'), 'word')

class TestWordComparator(unittest.TestCase):
    def test_twoStrings1(self):
        self.assertEqual(same('list','seek'), 0)

    def test_twoStrings2(self):
        self.assertEqual(same('lead','gold'), 1)

    def test_twoStrings3(self):
        self.assertEqual(same('letter','letter'), 6)

class TestMatchingWordsListBuilder(unittest.TestCase):
    def test_patterningWorks(self):
        self.assertEqual(build('test', ['test','assert','best'],{},[]),['test'])

    def test_wildcardWorks(self):
        self.assertEqual(build('.est', ['test','assert','best'],{},[]),['test','best'])

    def test_seenBlacklistWorks(self):
        self.assertEqual(build('.est', ['test','assert','best'],{'test': True},[]),['best'])

    def test_listBlacklistWorks(self):
        self.assertEqual(build('.est', ['test','assert','best'],{},['test']),['best'])

class TestFindingPaths(unittest.TestCase):
    def setUp(self):
        #Only words with 4 letters will be tested (to save memory space and minimize resource usage). Hence the self.gameWords variable will contain a list of 4 letter words from the dictionary.
        self.gameWords=[]
        try:
            fhandle = open("dictionary.txt")
            for line in fhandle:
                if len(line) == 5:
                    line = line.strip()
                    self.gameWords.append(line)
            fhandle.close()
        except:
            print("Error, dictionary.txt is required for this testing program to run fully. Ensure that it is located in the same directory as test.py")

    def test_correctPathFound1(self):
        self.assertEqual((find('lead', self.gameWords, {'lead':True},'gold', ['lead'])), ['lead', 'load', 'goad'])

    def test_correctPathFound2(self):
        self.assertEqual((find('hide', self.gameWords, {'hide':True},'seek', ['hide'])), ['hide', 'side', 'site', 'sits', 'sies', 'sees'])

    def test_correctPathFoundOneStep(self):
        self.assertEqual((find('hide', self.gameWords, {'hide':True},'ride', ['hide'])), ['hide'])

    def test_correctPathFoundNoPath(self):
        self.assertEqual((find('asfd', self.gameWords, {'asfd':True},'xxxx', ['asfd'])), False)

    def test_correctPathFoundStartEqualsMatch(self):
        self.assertEqual(find('lead', self.gameWords, {'lead':True},'lead', ['lead']), False)

if __name__ == '__main__':
    unittest.main()
