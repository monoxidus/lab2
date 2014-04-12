	

    #include <stdbool.h>
    #include "index.h"
    #include "data.h"
     
    struct _pair_t {
        index_t index;
        data_t data;
    }
     
    pair_t pair_from_index_data(index_t index, data_t data) {
        assert(index != NULL && data != NULL);
        pair->index = calloc(1, sizeof(struct _index_t));
        pair->data = calloc(1, sizeof(struct _data_t));
        return (pair);
    }
     
    pair_t pair_destroy(pair_t pair) {
        pair->index = index_destroy(pair->index);
        pair->data = data_destroy(pair->data);
        free(pair);
        pair = NULL;
        return (pair);
    }
     
    index_t pair_fst(pair_t pair) {
        assert(pair != NULL);
        assert(pair->index != NULL);
        return (pair->index);
    }
     
    data_t pair_snd(pair_t pair) {
        assert(pair != NULL);
        assert(pair->data != NULL);
        return (pair->data);
    }
     
    bool pair_is_equal(pair_t pair, pair_t other) {
        assert(pair != NULL && other != NULL);
        return (index_is_equal(pair->index, other->index) && data_is_equal(pair->data, other->data));
    }
     
    pair_t pair_copy(pair_t pair) {
        pair_t result = NULL;
        assert(pair != NULL);
        result->index = index_copy(pair->index);
        result->data = data_copy(pair->data);
        assert(pair_is_equal(pair, result));
        return (result);
    }


