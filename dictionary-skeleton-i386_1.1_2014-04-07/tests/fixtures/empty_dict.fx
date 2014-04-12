# esperamos el menu
> .*

# mostramos el dict vacio
< h
# espero encontrar {} (con cualquier cantidad de espacios o lineas en blanco)
> {\s*}

# pedimos el tamaño en un dict vacio
< z
# espero encontrar un cero
> [0]
: No es el tamaño esperado!

# buscamos en un dict vacio
< s
> .*
< foo
> no.*exist

# borramos en un dict vacio
< d
> .*
< foo
> no.*exist

# hacemos una copia
< c
# debería mostrarse otro diccionario vacio
> {\s*}

# salir chequeando leaks
< q
> All heap blocks were freed -- no leaks are possible
