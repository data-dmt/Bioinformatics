# Simulador Dogma Central

Aplicación educativa e interactiva para explorar tres procesos fundamentales del flujo de la información genética:

- **replicación del ADN**;
- **transcripción de ADN a ARN**;
- **traducción del ARNm a una cadena polipeptídica**.

El proyecto combina un núcleo de cálculo desarrollado en **Python con Biopython** con una interfaz web en **HTML, CSS, JavaScript y SVG**. La intención es que las secuencias calculadas y las representaciones visuales se complementen: el usuario puede introducir una secuencia, obtener los resultados exactos y recorrer cada mecanismo paso a paso mediante un explorador interactivo.

## Funcionalidades principales

La aplicación permite:

- introducir una hebra codificante de ADN en dirección **5′ → 3′**;
- validar y normalizar la secuencia;
- obtener la hebra complementaria;
- representar una replicación semiconservativa simplificada;
- diferenciar hebra líder y hebra rezagada;
- generar y visualizar fragmentos de Okazaki;
- transcribir la secuencia de ADN a ARN;
- traducir el ARNm utilizando el código genético estándar;
- consultar codones, anticodones y aminoácidos;
- reproducir cada proceso automáticamente o avanzar paso a paso;
- mostrar u ocultar etiquetas, enzimas, puentes de hidrógeno y explicaciones;
- consultar contenido teórico complementario sin saturar la vista principal;
- validar el comportamiento mediante pruebas automáticas.

## Procesos representados

### Replicación

La replicación se representa mediante una horquilla que avanza de izquierda a derecha. A partir de esta convención se muestran:

- apertura de la doble hélice por la **helicasa**;
- formación de cebadores mediante la **primasa**;
- síntesis de ADN en dirección **5′ → 3′** por la **ADN polimerasa**;
- síntesis continua de la **hebra líder**;
- síntesis discontinua de la **hebra rezagada**;
- formación de **fragmentos de Okazaki**;
- unión final de los fragmentos mediante **ADN ligasa**;
- formación de dos moléculas hijas semiconservativas.

La interfaz incluye también una explicación de los modelos conservativo, semiconservativo y dispersivo, junto con la relevancia del experimento de **Meselson y Stahl**.

El tamaño utilizado para los fragmentos de Okazaki puede modificarse desde la interfaz. Este parámetro controla la segmentación empleada por el simulador y facilita observar cómo se reconstruye la hebra rezagada.

### Transcripción

La secuencia introducida se interpreta como una **hebra codificante de ADN 5′ → 3′**. El programa obtiene la hebra molde complementaria y genera el ARN correspondiente.

Se representan:

- hebra codificante y hebra molde;
- lectura del molde en dirección **3′ → 5′**;
- síntesis de ARN en dirección **5′ → 3′**;
- complementariedad entre ADN y ARN;
- sustitución de timina por uracilo;
- función de la **ARN polimerasa**;
- iniciación, elongación y terminación;
- concepto de promotor;
- pre-ARNm y procesamiento eucariota: **cap 5′, splicing y cola poli-A**;
- diferencia entre intrones y exones;
- funciones generales de ARNm, ARNt y ARNr.

La secuencia de entrada no contiene anotaciones genómicas. Por este motivo, el programa no intenta inventar posiciones reales de promotores, intrones, exones o señales de terminación. Estos elementos se explican como contexto biológico, mientras que la secuencia de ARN mostrada procede directamente del cálculo realizado sobre la entrada.

### Traducción

La traducción utiliza el ARNm producido por el simulador y el código genético estándar.

El programa:

- localiza el primer **AUG** utilizado como inicio del modelo;
- establece el marco de lectura desde esa posición;
- divide el ARNm en codones de tres nucleótidos;
- calcula el anticodón complementario de cada ARNt;
- obtiene el aminoácido correspondiente mediante Biopython;
- construye progresivamente la cadena polipeptídica;
- reconoce **UAA, UAG y UGA** como codones STOP cuando aparecen dentro del marco de lectura;
- diferencia entre una traducción terminada, una secuencia sin AUG y una traducción que alcanza el final sin STOP.

El explorador permite seleccionar cada codón para consultar su posición, anticodón, aminoácido asociado y cadena acumulada hasta ese punto.

## Explorador interactivo

Tras ejecutar la secuencia, los resultados aparecen en un explorador dividido en tres pestañas: **Replicación**, **Transcripción** y **Traducción**.

Los controles disponibles son:

- **Reproducir / Pausar**: recorre automáticamente la etapa activa.
- **Paso**: avanza manualmente un estado de la animación.
- **Reiniciar**: vuelve al estado inicial de la etapa.
- **Velocidad**: modifica el ritmo de reproducción.
- **Etiquetas**: muestra u oculta las anotaciones del esquema.
- **Enzimas**: muestra u oculta los participantes principales.
- **Puentes**: controla la representación de los apareamientos de bases cuando corresponde.
- **Explicación**: muestra u oculta el panel narrativo sincronizado con la animación.

Las animaciones son complementarias a los resultados textuales. Las secuencias, posiciones y productos moleculares se calculan en Python y se muestran también de forma explícita para poder comparar la representación gráfica con el resultado bioinformático.

## Métricas de la secuencia

El resumen inicial muestra varias propiedades calculadas a partir de la secuencia:

- número total de bases;
- **contenido GC**;
- número estimado de puentes de hidrógeno en la doble hélice;
- número de fragmentos de Okazaki generado con el tamaño seleccionado;
- número de aminoácidos obtenidos durante la traducción.

El contenido GC se calcula como:

```text
(G + C) / longitud total × 100
```

Para la estimación de puentes de hidrógeno se consideran **2** para cada pareja A–T y **3** para cada pareja G–C.

## Organización del proyecto

```text
.
├── biology_content.py
├── simulator.py
├── web_app.py
├── requirements.txt
├── tests/
│   └── test_simulator.py
└── web/
    ├── index.html
    ├── style.css
    ├── diagrams.js
    └── app.js
```

### `biology_content.py`

Contiene el contenido explicativo que acompaña a los cálculos: pasos de cada proceso, enzimas y participantes principales, modelos de replicación, tipos de ARN y explicaciones complementarias. Separar estos datos de la lógica evita mezclar los algoritmos con los textos de la interfaz.

### `simulator.py`

Contiene el núcleo bioinformático. Sus responsabilidades principales son:

- validación y normalización del ADN;
- obtención de secuencias complementarias;
- replicación y fragmentos de Okazaki;
- transcripción ADN → ARN;
- traducción ARN → cadena polipeptídica;
- cálculo de contenido GC y puentes de hidrógeno;
- preparación de los resultados consumidos por la interfaz web.

### `web_app.py`

Implementa un servidor HTTP local utilizando la biblioteca estándar de Python. Sirve la interfaz y expone el endpoint:

```text
POST /api/simulate
```

La petición incluye la secuencia de ADN y el tamaño elegido para los fragmentos de Okazaki. La respuesta contiene los resultados de la simulación en formato JSON.

### `web/app.js`

Controla la interfaz:

- envío y validación básica de la secuencia;
- comunicación con la API;
- pestañas del explorador;
- reproducción y avance paso a paso;
- actualización de resultados y explicaciones;
- navegación codón a codón.

### `web/diagrams.js`

Contiene la construcción de los diagramas SVG y la lógica visual asociada a las animaciones de replicación, transcripción y traducción.

### `web/style.css`

Define la identidad visual, distribución, tamaños, estados interactivos, componentes y comportamiento responsive de la aplicación.

## Entrada

La entrada debe estar formada únicamente por las bases:

```text
A T C G
```

Se admiten minúsculas y espacios porque la secuencia se normaliza antes de procesarse.

La secuencia incluida por defecto es:

```text
ATGCCATGGAATGCTTAA
```

Su transcripción produce:

```text
AUGCCAUGGAAUGCUUAA
```

Y la traducción desde el primer AUG produce:

```text
Met-Pro-Trp-Asn-Ala
```

seguida por el codón STOP `UAA`.

La interfaz admite hasta **600 bases** para mantener manejable la visualización interactiva.

## Convenciones y límites del modelo

El simulador utiliza unas convenciones concretas para producir resultados reproducibles:

1. La entrada representa la **hebra codificante de ADN 5′ → 3′**.
2. La horquilla utilizada para distinguir líder y rezagada avanza de izquierda a derecha.
3. El tamaño de los fragmentos de Okazaki se controla mediante un parámetro didáctico configurable.
4. Promotores, intrones, exones y otras anotaciones genómicas no pueden inferirse de una secuencia aislada sin información adicional, por lo que no se inventan posiciones concretas.
5. La traducción comienza en el primer `AUG` encontrado y mantiene ese marco hasta un STOP o hasta el final de la secuencia.

## Requisitos

- Python 3
- Biopython `>=1.85,<2.0`
- navegador web moderno

No se utilizan frameworks web ni bibliotecas JavaScript externas.

## Instalación

Crear un entorno virtual:

```bash
python3 -m venv .venv
```

Activarlo en macOS o Linux:

```bash
source .venv/bin/activate
```

En Windows:

```text
.venv\Scripts\activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución web

Desde la raíz del proyecto:

```bash
python web_app.py
```

Por defecto se utiliza:

```text
http://127.0.0.1:8000
```

Para utilizar otro puerto:

```bash
python web_app.py --port 8001
```

Para iniciar el servidor sin abrir el navegador automáticamente:

```bash
python web_app.py --no-browser
```

## Pruebas automáticas

El proyecto incluye pruebas para comprobar, entre otros aspectos:

- validación de secuencias;
- complementariedad de ADN;
- reconstrucción de la hebra rezagada a partir de fragmentos de Okazaki;
- transcripción;
- traducción con y sin AUG;
- traducción con y sin STOP;
- comportamiento del marco de lectura;
- contenido GC;
- estimación de puentes de hidrógeno.

Para ejecutarlas:

```bash
python -m unittest discover -s tests -v
```

## Referencias

El contenido biológico toma como base los siguientes materiales de consulta:

- https://mltechdrawer.github.io/BIO/Bloque1_Bioinformatica/01_dogma/
- https://mltechdrawer.github.io/BIO/Bloque1_Bioinformatica/01_replicacion/
- https://mltechdrawer.github.io/BIO/Bloque1_Bioinformatica/01_transcripcion/
- https://mltechdrawer.github.io/BIO/Bloque1_Bioinformatica/01_traduccion/

Para el diseño del explorador se tomó como referencia general el enfoque interactivo de:

- https://simulations4all.com/simulations/dna-replication-and-protein-synthesis-explorer

La implementación, los cálculos y la estructura del proyecto son propios y se mantienen centrados en replicación, transcripción y traducción.
