# automaton-ops

Genere un autómata basado en operaciones de autómatas: unión, intersección, concatenación y cerradura de kleene.

**Nota: para ver esta documentación en inglés vaya a la [version en Inglés](README.md)**

## Instalación

Este proyecto corre usando Python3, y fue desarrollado usando la version 3.8.5, en caso de que no tenga Python3 instalado, usted puede seguir las instrucciones de instalación de python de la página oficial de python: https://www.python.org/downloads/.

### Descargar el código fuente

Descarge el código fuente en el siguiente enlace: https://github.com/gbriones1/automaton-ops/archive/main.zip

Este archivo es un archivo comprimido `.zip` por lo que necesitará descomprimir el contenido de este archivo dando clic derecho en él para abrir el menú y luego seleccionando la opción para extraer el contenido.

O si lo prefiere, usted puede clonar este repositorio ejecutando el siguiente comando en una terminal:

```bash
git clone https://github.com/gbriones1/automaton-ops.git
```

Si usted ya tiene el código fuente, entonces continúe al siguiente paso.

### Abrir una terminal

Para verificar que tiene Python3 instalado, necesita abrir una terminal y ejecutar el siguiente comando:

```bash
python3 --version
```

Una terminal puede ser abierta de diferentes maneras dependiendo en su sistema operativo:

#### MacOS

En su Mac, haga alguna de las siguientes:

 * Clic en el ícono de Lauchpad en el Dock, escriba Terminal en el campo de búsqueda y luego haga clic en Terminal.
 * En el Finder, abra el directorio /Applications/Utilities, después de doble clic en Terminal.

#### Windows

 1. Haga clic en el ícono de Windows en la esquina inferior izquierda de su escritorio, o presione la tecla Win en su teclado.
 2. Escriba cmd o Command Prompt. Después de abrir el menú de inicio, escriba esto en su teclado para buscar las opciones del menú. La aplicación “Command Prompt” aparecerá como el primer resultado.
 3. Haga clic en la aplicación Command Prompt del menú. Esto abrirá la terminal en una nueva ventana.

#### Linux

 * Presione Ctrl+Alt+T en Ubuntu, o presione Alt+F2, luego escriba gnome-terminal, y presione enter.

### Navegar a la ubicación del código fuente

Con la terminal abierta use el comando `cd` seguido de una estructura de directorios separados por diagonales (`/`) para navegar a la ubicación del código fuente

```bash
cd <ruta>/<al>/<código>/<fuente>
```

**Nota: Si usted está usando Windows, separe los directorios usando diagonales invertidas: `\`**

## Uso del programa

Los autómatas que usamos son compatibles con la herramienta online: http://ivanzuzak.info/noam/webapps/fsm_simulator/. Esta es una herramienta que se utiliza para dibujar y simular autómatas finitos utilizando expresiones regulares y definiciones de autómatas.

### Defina autómatas

Una definición válida de máquina de estados finita (FSM) contiene una lista de estados, símbolos y transiciones, el estado inicial y los estados de aceptación. Los estados y símbolos son cadenas de caracteres alfanuméricos y no pueden ser los mismos. Las transiciones tienen el formato: `estadoA:símbolo>estadoB,estadoC`. El carácter `$` es usado para representar el símbolo vacío (epsilon) pero no debe ser listado en el alfabeto.

Hemos proveído una lista de definiciones de autómatas en la carpeta `samples` de este proyecto. Pero si así lo desea, usted puede ir a la página http://ivanzuzak.info/noam/webapps/fsm_simulator/ despues en la sección `① Create automaton` navegue a la pestaña `Input automaton` y después de clic en alguno de los botones `Generate random DFA`, `Generate random NFA`, o `Generate random eNFA` para generar una definición aleatoria que será desplegado en el área de texto bajo los botones.

Los autómatas deben ser archivos de texto para que el programa los pueda leer.

### Ejecute el programa

Para ejecutar el programa en su terminal, escriba `./main.py` seguido por los argumentos: `--automaton1 <ruta>/<al>/<autómata>`, `--automaton2 <ruta>/<al>/<autómata>` y `--operation <nombre_de_operacion>`

Los nombres de operaciones disponibles son:

 * `union`
 * `intersect`
 * `concat`
 * `kleene_star`

**Nota: `kleene_star` es una operación de un solo autómata, para tal caso, el argumento `--automaton2` no es requerido.**

Usted también puede ver la ayuda del programa ejecutando:

```bash
./main.py --help
```

#### Ejemplo

Si usted quisiera realizar una unión entre los autómatas definidos en los archivos: `samples/DFA_1.txt` y `samples/DFA_2.txt`, ejecute el siguiente comando:

```bash
./main.py --automaton1 samples/DFA_1.txt --automaton2 samples/DFA_2.txt --operation union
```

Esto generará la siguiente salida:

```
#states
AP
AR
BQ
CP
CQ
CR
#initial
AP
#accepting
AP
AR
BQ
CR
#alphabet
0
1
#transitions
AP:0>BQ
CP:0>CQ
CQ:1>CR
CR:0>CQ
CP:1>CP
CQ:0>CQ
AR:0>BQ
AR:1>AP
BQ:1>AR
AP:1>AP
CR:1>CP
BQ:0>CQ
```

### Dibuje el grafo de un autómata

La salida de la ejecución será la definición de un autómata que resulte de la operación, este texto puede ser copiado y pegado en el área de texto en http://ivanzuzak.info/noam/webapps/fsm_simulator/ en la sección `① Create automaton` bajo la pestaña `Input automaton`, después cree el grafo haciendo clic en el boton `Create automaton`.

El grafo generado aparecerá en la sección `③ Transition graph` de la misma página.

#### Simule el autómata

Una vez dibujado el grafo del autómata, usted puede simular la ejecución del mismo utilizando una palabra que utilice los símbolos del alfabeto.

En la sección `② Simulate automaton`  se pueden generar palabras aleatorias o alguna de su preferencia, después se da clic en el botón `Start` para empezar la simulación.

Para navegar por la simulación utilice los botones que también se encuentran en esta sección. Mientras navega por la simulación, los colores de los estados en el gráfico del autómata cambiarán, se estará indicando con color gris aquellos estados con los que se encuentra en el camino. Si al terminar de procesar la palabra, alguno de los estados de aceptación se encuentra de color gris, entonces la palabra es aceptada.
