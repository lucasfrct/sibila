# flake8: noqa: E501

class ArrayControl:

    def __init__(self):
        self.last_sequential = -1

    def fetch_contiguous_items(self, array):
        init = self.last_sequential + 1

        for i in range(init, len(array)):
            if array[i] is None:
                break
            self.last_sequential = i

        items = array[init:self.last_sequential + 1]

        return items

    def reset(self):
        self.last_sequential = -1
        
    def slice_after_match(self, term: str , array):
        for i, item in enumerate(array):
            if term in item:
                return array[i:]
        return array
    
    def slice_between_match(self, initial_term: str, final_term: str, array):
        start_idx = None
        end_idx = None
        
        if initial_term == '' and final_term == '':
            return array
        
        # Encontrar o índice do termo inicial
        for i, item in enumerate(array):
            if initial_term in item:
                start_idx = i
                break

        # Se o termo inicial não for encontrado, retorna o array completo
        if start_idx is None:
            start_idx = 0

        # Encontrar o índice do termo final, começando após o termo inicial
        for j in range(start_idx, len(array) - 1):
            if final_term in array[j]:
                end_idx = j
                break
            
           # Se o termo inicial não for encontrado, retorna o array completo
        if end_idx is None:
            end_idx = len(array) - 1

        # Retorna o recorte entre os índices de início e fim
        return array[start_idx:(end_idx + 1)]