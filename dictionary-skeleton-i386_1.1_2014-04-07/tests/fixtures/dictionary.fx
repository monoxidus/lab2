# esperamos el menu
> .*

# pedimos el tamaño
< z
# espero encontrar un cero
> [0]
: No es el tamaño esperado!

# agregamos: independiente
< a
> .*
< independiente
> .*
< el rojo
> .*

# agregamos: boca
< a
> .*
< boca
> .*
< el xeneize
> .*

# agregamos: san lorenzo
< a
> .*
< san lorenzo
> .*
< el ciclón
> .*

# agregamos: velez
< a
> .*
< velez
> .*
< el fortín
> .*

# agregamos: racing
< a
> .*
< racing
> .*
< la academia
> .*

# agregamos: river
< a
> .*
< river
> .*
< el millonario
> .*

# agregamos: lanus
< a
> .*
< lanus
> .*
< el granate
> .*

# pedimos el tamaño
< z
# espero encontrar 7
> [7]
: No es el tamaño esperado!

# buscamos algo que no existe: milan
< s
> .*
< milan
> .*

# buscamos river
< s
> .*
< river
> el millonario

# borramos independiente
< d
> .*
< independiente
> .*

# pedimos el tamaño
< z
# espero encontrar 6
> [6]
: No es el tamaño esperado!

# buscamos independiente
< s
> .*
< independiente
! el rojo
: Encontramos la palabra borrada!

# agregamos: rafaela
< a
> .*
< rafaela
> .*
< la crema
> .*

# pedimos el tamaño
< z
# espero encontrar 7
> [7]
: No es el tamaño esperado!

# borramos racing
< d
> .*
< racing
> .*

# pedimos el tamaño
< z
# espero encontrar 6
> [6]
: No es el tamaño esperado!

# hacemos una copia
< c
# debería mostrarse el diccionario
> .*

# vaciamos el diccionario
< e
> .*

# agregamos al diccionario recien vaciado: rafaela
< a
> .*
< rafaela
> .*
< la crema
> .*

# pedimos el tamaño
< z
# espero encontrar 1
> [1]

# pedimos mostrarlo
< h
# espero encontrar
# {
# rafaela: la crema
# }
> {\s*rafaela: la crema\s*}

# salir chequeando leaks
< q
> All heap blocks were freed -- no leaks are possible
