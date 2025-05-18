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
     

def encode_string(string, huffman_codes):
    encoded_string=""
    for c in string:
        encoded_string+=huffman_codes[c]
    return encoded_string
    

def decode_string(encoded_string, huffman_codes):
    decoded_string=""
    reversed_codes = {v: k for k, v in huffman_codes.items()}
    prefix=""
    for c in encoded_string:
        prefix+=c
        if prefix  in reversed_codes:
            decoded_string+=reversed_codes[prefix]
            prefix=""
        
    
    return decoded_string

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
        
    endcoded_string=encode_string(user_input,huffman_codes)
    print("kok ",endcoded_string)
    print("decoded ", decode_string(endcoded_string,huffman_codes))

if __name__ =="__main__":
    main()