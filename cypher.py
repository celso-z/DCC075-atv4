from abc import ABC, abstractmethod


class Cypher(ABC):
    def __init__(self, key: str):
        self.key = key 

    @abstractmethod
    def cypher(self, block:str) -> str:
        pass

    @abstractmethod
    def decypher(self, block:str) -> str:
        pass

    def adjust_key_size(self, block:str) -> str:
        size = len(block)
        adjusted_key = (self.key * (size // len(self.key) + 1))[:size]

        return adjusted_key

class VigenereCypher(Cypher):
    def cypher(self, block:str) -> str:
        ret = ""
        adjusted_key = self.adjust_key_size(block)

        for c, k in zip(block,adjusted_key):
            ret = ret + (chr((((ord(c) % 97) + (ord(k) % 97)) % 26) + 65))

        return ret

    def decypher(self, block:str) -> str:
        ret = ""
        adjusted_key = self.adjust_key_size(block)

        for c, k in zip(block,adjusted_key):
            ret = ret + (chr((((ord(c) - 65) - (ord(k) - 97)) % 26) + 97))

        return ret
    
class BlockCypher(ABC):
    def __init__(self, cypher:Cypher, block_size:int):
        self.cypher = cypher
        self.block_size = block_size
        self.pad_size = 0

    def separate_blocks(self, block: str, update_pad: bool = False) -> list[str]:
        #Separa mensagens em blocos de tamanho block_size
        pad_size = (self.block_size -(len(block) % self.block_size) if len(block) % self.block_size else 0)
        if update_pad:
            self.pad_size = pad_size
        block = block.ljust(len(block) + pad_size, 'x')
        ret = []

        i = 0
        while(i < len(block)):
            ret.append(block[i:i+self.block_size])
            i = i + self.block_size
        return ret

    @abstractmethod
    def cypherData(self, data: str):
        pass


class EBC(BlockCypher):
    def cypherData(self, data: str) -> str:
        data_blocks = self.separate_blocks(data, True)
        cyphered_blocks = []

        for block in data_blocks:
            cyphered_blocks.append(self.cypher.cypher(block))

        cypher_text:str = "".join(cyphered_blocks)

        return cypher_text

    def decypherData(self, data: str) -> str:
        data_blocks = self.separate_blocks(data)
        cyphered_blocks = []

        for block in data_blocks:
            cyphered_blocks.append(self.cypher.decypher(block))
        cypher_text:str = "".join(cyphered_blocks)

        return cypher_text[:-self.pad_size]

class CFB(BlockCypher):
    def __init__(self, init_vector:str, cypher:Cypher, block_size:int):
        self.init_vector = init_vector
        super().__init__(cypher, block_size)


    def cypherData(self, data: str) -> str:
        data_blocks = self.separate_blocks(data, True)
        previous_block = self.init_vector * (self.block_size//len(self.init_vector) + 1)
        cyphered_blocks = []

        for block in data_blocks:
            new_block = ""
            cypher = self.cypher.cypher(previous_block)
            for c, t in zip(cypher, block):
                new_block = new_block + (chr(ord(c) ^ ord(t)))
            cyphered_blocks.append(new_block)
            previous_block = new_block


        cypher_text:str = "".join(cyphered_blocks)
        return cypher_text

    def decypherData(self, data: str) -> str:
        data_blocks = self.separate_blocks(data)
        previous_block = self.init_vector * (self.block_size//len(self.init_vector) + 1)
        cyphered_blocks = []

        for block in data_blocks:
            new_block = ""
            cypher = self.cypher.cypher(previous_block)
            for c, t in zip(cypher, block):
                new_block = new_block + (chr(ord(c) ^ ord(t)))
            cyphered_blocks.append(new_block)
            previous_block = block


        cypher_text:str = "".join(cyphered_blocks)
        return cypher_text[:-self.pad_size]

def main():
    cypher = VigenereCypher("76003")
    blocking = CFB("aaa", cypher, 5)
    text = blocking.cypherData("finalmenterm")
    dec = blocking.decypherData(text)
    

if __name__ == "__main__":
    main()

