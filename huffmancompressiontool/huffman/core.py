import heapq


class Node:
    def __init__(self,character=None, freq=None):
        self.character=character
        self.freq=freq
        self.left=None
        self.right=None
        
    def __lt__(self,other):
        return self.freq<other.freq
    
    
    
def build_huffman_tree(freq_dict):
    pq=[Node(char,f) for char, f in freq_dict.items()]
    heapq.heapify(pq)
    
    while len(pq)>1:
        left_child=heapq.heappop(pq)
        right_child=heapq.heappop(pq)
        merged_node=Node(freq=left_child.freq+right_child.freq)
        merged_node.left=left_child
        merged_node.right=right_child
        
        heapq.heappush(pq,merged_node)
    return pq[0]
        
    

def generate_huffman_codes(node, code="", huffman_codes={}):
        
    if node is not None:
        if node.character is not None:
            huffman_codes[node.character]=code
        
        generate_huffman_codes(node.left,code+"0",huffman_codes)
        generate_huffman_codes(node.right,code+"1",huffman_codes)
        
    return huffman_codes
     

def encode_string():
    pass

def decode_sting():
    pass


def count_frequency(string):
    freq_dict={}
    for c in string:
        if c in freq_dict:
            freq_dict[c]+=1
        else:
            freq_dict[c]=1
    
    

    print(freq_dict)
    
    return freq_dict
    
    
    
def main():
    
    print("plz enter")
    user_input=input()
    freq_dict=count_frequency(user_input)
    root=build_huffman_tree(freq_dict)
    
    huffman_codes=generate_huffman_codes(root)
    for char, code in huffman_codes.items():
        print(f"Character: {char}, Code: {code}")

if __name__ =="__main__":
    main()