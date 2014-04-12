#include <assert.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include "dict.h"
#include "list.h"
     
struct _dict_t{
        list_t lista;
};
     
dict_t dict_empty(void){
        
        dict_t dict = calloc(1, sizeof(struct _dict_t));
        
        dict->lista = list_empty();
        assert(dict != NULL); 
        assert(dict_length(dict) == 0);
        return(dict);

}
     
dict_t dict_destroy(dict_t dict){
        
        free(dict->lista);
        (dict->lista) = NULL;
        free(dict);
        dict = NULL;
        return(dict);
}
     
unsigned int dict_length(dict_t dict){
        assert(dict != NULL);
        return(list_length(dict->lista));
        list_destroy(dict->lista);
        free(dict);
}
     
bool dict_is_equal(dict_t dict, dict_t other){
        assert(dict != NULL && other != NULL);
        return(list_is_equal(dict->lista,other->lista));
        list_destroy(dict->lista);
        list_destroy(other->lista);
        free(dict);
        free(other);
}
     
bool dict_exists(dict_t dict, word_t word){
        
        assert(dict->lista != NULL);
        assert(word != NULL);
        
        bool r = true;
        index_t indice = index_from_string(word);
        
        r=(list_search(dict->lista,indice) != NULL);
               
        return r;
		
		index_destroy(indice);
		free(word);
		list_destroy(dict->lista);
		free(dict);

}
     
def_t dict_search(dict_t dict, word_t word) {
    index_t indice = index_from_string(word);
    assert(dict != NULL && word != NULL);
    assert(dict_exists(dict,word));
    assert(list_search(dict->lista,index_from_string(word)) == NULL);
    return(data_to_string(list_search(dict->lista,indice)));
    index_destroy(index_from_string(word));
       
}
     
dict_t dict_add(dict_t dict, word_t word, def_t def){
        assert(dict != NULL && word != NULL && def != NULL);
        assert(dict_exists(dict,word) == false);
        /*assert poscondicion*/
        dict->lista = (list_append(dict->lista, index_from_string(word),
        data_from_string(def)));
        return(dict);
}  
     
dict_t dict_remove(dict_t dict, word_t word){
        
        index_t variab = NULL;
        
        assert(dict != NULL && word != NULL);
        assert(dict_exists(dict,word));
        /*assert poscondicion*/
        
        variab = index_from_string(word);
        
        dict->lista = list_remove((dict->lista),variab);
        
        return(dict);
        
        
		list_destroy(dict->lista);
		free(dict);
		dict = NULL;
		index_destroy(variab);
		
			
}
     
dict_t dict_copy(dict_t dict){
        dict_t dict2 = NULL;
        dict2 = calloc(1, sizeof(struct _dict_t));
        dict2->lista = list_copy(dict->lista);
        assert(dict_is_equal(dict,dict2));
        return(dict2);
}
     
void dict_dump(dict_t dict, FILE *fd){
        assert(dict != NULL);
        assert(fd != NULL);
        list_dump(dict->lista, fd);
}
