from fugashi import Tagger
import pykakasi
from sudachipy import tokenizer
from sudachipy import dictionary

class Word:
    def __init__(self, word, pos, dictionary_form, hira, kana, roma):
        """ Word object with attributes Part of speech, Dictionary form, Hiragana
            Katakana and Romaji"""
        self.word = word
        self.next = None
        self.prev = None
        self.pos = pos
        self.dictionary_form = dictionary_form
        self.hira = hira
        self.kana = kana
        self.roma = roma

    def get_word(self):
        return self.word
    
    def get_next(self):
        return self.next
    
    def get_dictionary_form(self):
        return self.dictionary_form

    def get_pos(self):
        return(self.pos)
        
    def get_hira(self):
        return(self.hira)
        
    def get_kana(self):
        return(self.kana)
        
    def get_romaji(self):
        return(self.roma)
    
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def get_head(self):
        return(self.head)
    
    def get_tail(self):
        return(self.tail)
    
    def append(self, new_word):
        if self.head is None:
            self.head = new_word
            self.tail = new_word
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_word
        new_word.prev = current
        self.tail = new_word
    
    def insert(self, data, position):
        new_node = Node(data)
        if position == 0:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            return
        current = self.head
        index = 0
        while current.next and index < position - 1:
            current = current.next
            index += 1
        if not current.next:
            self.tail = new_node
        new_node.prev = current
        new_node.next = current.next
        current.next = new_node
        new_node.next.prev = new_node
    
    def delete(self, value):
        if self.head is None:
            return
        if self.head.data == value:
            if self.head == self.tail:
                self.tail = None
            self.head = self.head.next
            self.head.prev = None
            return
        current = self.head
        while current.next:
            if current.next.data == value:
                if current.next == self.tail:
                    self.tail = current
                current.next = current.next.next
                current.next.prev = current
                return
            current = current.next
  
def populate_doubly_linked_list(words_list):
    doubly_linked_list = DoublyLinkedList()
    
    for word in words_list:
        doubly_linked_list.append(word)
    
    return doubly_linked_list

def create_words_list(user_input):
    tagger = Tagger('-Owakati')
    kks = pykakasi.kakasi()
    punc = ['・','、','。','「','」','『','』','【','】','〔','〕','〈','〉','《','》', '？','’','！','\n']
    for i in punc:
        user_input = user_input.replace(i, "")
    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.C
    tokens = [m.surface() for m in tokenizer_obj.tokenize(user_input, mode)]
    nodes_list = []
    for token in tokens:
        tagger.parse(token) #parsing with fugashi
        parsed_word = tagger(token)[0]
        POS = (parsed_word.pos.split(",")[0]) #extracting part of speech
        dict_form = parsed_word.feature.lemma #extracting dictionary form
        converted_word = kks.convert(token) #converting into a kks object to extract other attributes
        item = converted_word[0]
        orig, dict_form, hiragana, katakana, romaji = (token, dict_form, item['hira'], item['kana'], item['kunrei'])
        word = Word(orig, POS, dict_form, hiragana, katakana, romaji) #creating the word object
        nodes_list.append(word)
    return nodes_list

def print_as_sentence(doubly_linked_list):
    current = doubly_linked_list.get_head()
    sentence=""
    while current is not None:
        sentence+=(current.get_word())
        current = current.get_next()
    print(sentence)

# def main():    
#     words = create_words_list("子供の頃は自転車に乗れませんでしたが、今は乗れます。")
#     dll = populate_doubly_linked_list(words)
#     print_as_sentence(dll)
    
# main()