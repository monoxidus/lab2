#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include "dict.h"
#include "list.h"
#include "helpers.h"
#include "dict_helpers.h"

#define SHOW_SIZE_DICT 'z'
#define FIND_DEF 's'
#define ADD_WORD 'a'
#define DEL_WORD 'd'
#define EMPTY_DICT 'e'
#define SHOW_DICT 'h'
#define DOUBLE_DICT 'c'
#define LOAD_DICT 'l'
#define SAVE_DICT 'u'
#define EXIT 'q'

char print_menu(void) {
    char result = '\0', discard = '\0';
    int scanf_result = 0;
    printf("Elija. Las opciones son:\n"
           "\tz - Mostrar el tamaño del diccionario en uso\n"
           "\ts - Buscar una definicion para una palabra dada\n"
           "\ta - Agregar una palabra con su correspondiente definicion al "
           "diccionario\n"
           "\td - Borrar una palabra con su correspondiente definicion del "
           "diccionario\n"
           "\te - Vaciar el diccionario actual\n"
           "\th - Mostar el diccionario actual por salida estandar\n"
           "\tc - Copiar el diccionario actual, mostrando el diccionario\n"
           "\tcopiado por salida estandar\n"
           "\tl - Cargar un nuevo diccionario desde un archivo dado por "
           "el usuario\n"
           "\tu - Guardar el diccionario actual en un elegido dado por el "
           "usuario\n\tq - Finalizar\n\tPor favor ingrese su elección: ");

    scanf_result = scanf("%c", &result);
    if (scanf_result != 1) {
        result = '\0';
    }

    /* Consume everything left in the stdin buffer */
    while (discard != '\n') {
        scanf_result = scanf("%c", &discard);
    }

    return (result);
}

bool is_valid_option(char option) {
    bool result = false;

    result = (option == EXIT ||
              option == SHOW_SIZE_DICT ||
              option == FIND_DEF ||
              option == ADD_WORD ||
              option == DEL_WORD ||
              option == EMPTY_DICT ||
              option == SHOW_DICT ||
              option == DOUBLE_DICT ||
              option == LOAD_DICT || option == SAVE_DICT);

    return (result);
}

int main(void) {
    char option = '\0';
    dict_t dict = NULL;
    word_t word = NULL;
    def_t def = NULL;
    dict_t dict2 = NULL;
    char *filename = NULL;
    unsigned int x = 0;

    dict = dict_empty();

    do {
        option = print_menu();
        switch (option) {
            case SHOW_SIZE_DICT:
                x = (dict_length(dict));
                printf("El largo del diccionario es %u\n", x);
                break;
            case FIND_DEF:
                printf("palabra a buscar: \n");
                word = readline_from_stdin();
                def = dict_search(dict, word);
                printf("%s\n", def);
                free(word);
                free(def);
                word = NULL;
                def = NULL;
                break;
            case ADD_WORD:
                printf("palabra a agregar: \n");
                word = readline_from_stdin();
                printf("definicion:\n");
                def = readline_from_stdin();
                dict_add(dict, word, def);
                free(word);
                word = NULL;
                free(def);
                def = NULL;
                break;
            case DEL_WORD:
                printf("palabra a borrar: \n");
                word = readline_from_stdin();
                dict_remove(dict, word);
                free(word);
                word = NULL;
                break;
            case EMPTY_DICT:
				dict = dict_destroy(dict);
                dict = dict_empty();
                break;
            case SHOW_DICT:
                dict_dump(dict, stdout);
                printf("\n");
                break;
            case DOUBLE_DICT:
                dict2 = dict_copy(dict);
                dict_dump(dict2, stdout);
                printf("\n");
                dict = dict_destroy(dict);
                dict = dict_empty();
                break;
            case LOAD_DICT:
                dict = dict_destroy(dict);
                printf("nombre del archivo: \n");
                filename = readline_from_stdin();
                dict = dict_from_file(filename);
                free(filename);
                filename = NULL;
                break;
            case SAVE_DICT:
                printf("nombre del archivo: \n");
                filename = readline_from_stdin();
                dict_to_file(dict, filename);
                free(filename);
                filename = NULL;
                break;
            case EXIT:
                printf("Exiting.\n");
                dict = dict_destroy(dict);
                return (EXIT_SUCCESS);
            default:
                printf("\n\"%c\" is invalid. Please choose a valid "
                       "option.\n\n", option);
        }
    } while (!is_valid_option(option) != EXIT);
    /* destroy dict */
    dict = dict_destroy(dict);

    return (EXIT_SUCCESS);
}
