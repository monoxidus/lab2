#include <assert.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include "dict.h"
#include "list.h"

struct _dict_t {
    list_t lista;
};

dict_t dict_empty(void) {
    dict_t dict = calloc(1, sizeof(struct _dict_t));
    dict->lista = list_empty();
    assert(dict != NULL);
    assert(dict_length(dict) == 0);
    return (dict);
}

dict_t dict_destroy(dict_t dict) {
    list_destroy(dict->lista);
    free(dict);
    dict = NULL;
    return (dict);
}

unsigned int dict_length(dict_t dict) {
    assert(dict != NULL);
    return (list_length(dict->lista));
}

bool dict_is_equal(dict_t dict, dict_t other) {
    assert(dict != NULL && other != NULL);
    return (list_is_equal(dict->lista, other->lista));
}

bool dict_exists(dict_t dict, word_t word) {
    assert(dict->lista != NULL);
    assert(word != NULL);
    bool r = true;
    index_t indice = index_from_string(word);
    r = (list_search(dict->lista, indice) != NULL);
    index_destroy(indice);
    return r;
}

def_t dict_search(dict_t dict, word_t word) {
    assert(dict != NULL && word != NULL);
    /*assert(dict_exists(dict,word)); */
    index_t indice = index_from_string(word);
    def_t r = NULL;
    data_t s = NULL;
    if (dict_exists(dict, word) == false) {
        printf("word does not exist\n");
    } else {
        s = list_search(dict->lista, indice);
        r = data_to_string(s);
    }
    index_destroy(indice);
    return (r);
}

dict_t dict_add(dict_t dict, word_t word, def_t def) {
    assert(dict != NULL);
    assert(word != NULL);
    assert(def != NULL);
    assert(dict_exists(dict, word) != true);
    index_t l = index_from_string(word);
    data_t a = data_from_string(def);
    /*assert poscondicion */
    dict->lista = (list_append(dict->lista, l, a));
    return (dict);
}

dict_t dict_remove(dict_t dict, word_t word) {
    index_t variab = NULL;
    assert(dict != NULL && word != NULL);
    assert(dict_exists(dict, word));
    /*assert poscondicion */
    variab = index_from_string(word);
    list_remove((dict->lista), variab);
    index_destroy(variab);
    return (dict);

}

dict_t dict_copy(dict_t dict) {
    dict_t dict2 = NULL;
    dict2 = calloc(1, sizeof(struct _dict_t));
    dict2->lista = list_copy(dict->lista);
    assert(dict_is_equal(dict, dict2));
    return (dict2);
}

void dict_dump(dict_t dict, FILE * fd) {
    assert(dict != NULL);
    assert(fd != NULL);
    list_dump(dict->lista, fd);
}
