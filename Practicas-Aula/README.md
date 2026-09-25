::: center
**Del ADN a la proteína**\
Práctica de Bioinformática\
**Autor:** Diego Muñoz Torres **Fecha:** 2026-09-25
:::

------------------------------------------------------------------------

# Ejercicio 1. Replicación del ADN

La molécula inicial es:

::: center
`5’--ATG CCG TTA GCT--3’`\
`3’--TAC GGC AAT CGA--5’`
:::

La replicación del ADN es **semiconservativa**: cada una de las hebras
originales actúa como molde para sintetizar una nueva hebra
complementaria. Por tanto, tras una ronda de replicación se obtienen dos
moléculas de ADN con la misma secuencia que la molécula inicial, cada
una formada por una hebra parental y una hebra recién sintetizada.

Las nuevas hebras serán:

::: center
`3’--TAC GGC AAT CGA--5’`\
`5’--ATG CCG TTA GCT--3’`
:::

Las principales enzimas implicadas son:

- **Helicasa**: separa las dos hebras rompiendo los puentes de hidrógeno
  entre las bases.

- **Primasa**: sintetiza cebadores de ARN que permiten iniciar la
  síntesis de ADN.

- **ADN polimerasa**: incorpora nucleótidos complementarios y sintetiza
  la nueva hebra en dirección 5'$\rightarrow$`<!-- -->`{=html}3'.

- **Ligasa**: une los fragmentos de ADN, especialmente los fragmentos de
  Okazaki de la hebra retardada.

Si la ADN polimerasa introdujera una base incorrecta y el error no fuese
reparado, podría quedar fijado como una **mutación**. Su efecto
dependería de la región afectada y podría ser neutro o modificar
posteriormente la secuencia y función de una proteína.

**Extensión con Biopython.** Mediante `Bio.Seq` se obtuvo
automáticamente la hebra complementaria utilizando `complement()` y se
comprobó que coincidía con el resultado manual. También se utilizó
`reverse_complement()` para representar la hebra complementaria en la
orientación convencional 5'$\rightarrow$`<!-- -->`{=html}3'.

# Ejercicio 2. Transcripción del ADN a ARN

Para la secuencia:

::: center
`5’--ATG CCT GAA TGC--3’`\
`3’--TAC GGA CTT ACG--5’`
:::

se considera como **cadena molde** la hebra inferior, que es leída por
la ARN polimerasa en dirección 3'$\rightarrow$`<!-- -->`{=html}5'. El
ARN se sintetiza de forma antiparalela en dirección
5'$\rightarrow$`<!-- -->`{=html}3':

::: center
`ADN molde: 3’--TAC GGA CTT ACG--5’`\
`ARNm: 5’--AUG CCU GAA UGC--3’`
:::

La hebra superior es la **cadena codificante**, ya que presenta la misma
secuencia que el ARNm salvo por la sustitución de timina (T) por uracilo
(U).

La **región promotora** es una región reguladora situada aguas arriba
del inicio de la transcripción donde se unen la ARN polimerasa y otros
factores. La secuencia proporcionada no permite identificar un promotor
concreto. La **región codificante** corresponde a la secuencia que
contiene la información que puede traducirse a proteína; en este caso
comienza por `ATG`, aunque la secuencia propuesta no contiene un codón
de parada y, por tanto, no representa una CDS completa.

**Extensión con Biopython.** Se utilizó la CDS del gen humano *HBB*
almacenada en `HBB_CDS.fasta`. Biopython permitió obtener la región
codificante del ARNm mediante `transcribe()`. Al invertir la orientación
de la secuencia se comprobó que la transcripción depende de conocer
correctamente qué hebra actúa como molde. Al tratar la orientación
mediante `reverse_complement()`, se recupera el mismo transcrito.

# Ejercicio 3. Traducción del ARNm a proteína

El transcrito es:

::: center
`5’--AUG UAU GCU UAA--3’`
:::

Los codones se interpretan como:

::: center
`AUG `$\rightarrow$` Met UAU `$\rightarrow$` Tyr GCU `$\rightarrow$` Ala UAA `$\rightarrow$` STOP`
:::

Por tanto, la proteína obtenida es:

::: center
**Met--Tyr--Ala**
:::

`AUG` es el codón de inicio y `UAA` es un codón de terminación.

Si el codón de inicio mutara de `AUG` a `GUG`, en células eucariotas
podría dificultarse o impedirse el inicio de la traducción en esa
posición, pudiendo utilizarse otro `AUG` situado posteriormente. En
bacterias, `GUG` puede funcionar en determinados genes como codón de
inicio, incorporándose habitualmente N-formilmetionina como aminoácido
iniciador.

Si desapareciera el codón de parada, el ribosoma continuaría traduciendo
el ARNm hasta encontrar otro codón STOP, produciendo normalmente una
proteína más larga cuya estructura o función podría verse alterada.

**Extensión con Biopython.** La traducción con `Bio.Seq.translate()`
produjo `MYA*`, equivalente a Met--Tyr--Ala seguido del codón de
terminación, coincidiendo con la traducción manual.

# Ejercicio 4. Splicing alternativo

Considerando un gen formado por cinco exones:

::: center
`Exón 1 -- Exón 2 -- Exón 3 -- Exón 4 -- Exón 5`
:::

dos posibles variantes de splicing alternativo serían:

- **Isoforma 1**: Exón 1 -- Exón 2 -- Exón 4 -- Exón 5.

- **Isoforma 2**: Exón 1 -- Exón 3 -- Exón 5.

La inclusión o exclusión de determinados exones modifica la secuencia
del ARNm maduro y puede cambiar la longitud, la secuencia de aminoácidos
o los dominios funcionales de las proteínas resultantes. Si se altera el
marco de lectura también pueden aparecer codones de terminación
prematuros.

Este mecanismo aumenta la diversidad proteica porque un mismo gen puede
generar diferentes ARNm maduros y, potencialmente, distintas isoformas
proteicas sin necesidad de incrementar el número de genes.

**Extensión con bases de datos.** Se estudiaron los transcritos del gen
humano *FGFR2* (`ENSG00000066468`) utilizando datos de Ensembl. Se
observaron múltiples transcritos con diferente composición y longitud de
exones. Estas variaciones pueden modificar regiones funcionales de la
proteína; en particular, el splicing alternativo de *FGFR2* puede
afectar al dominio extracelular implicado en la unión a ligandos. Como
consecuencia, distintas isoformas pueden presentar diferente
especificidad por factores de crecimiento y modificar la señalización
celular aun procediendo del mismo gen.

# Ejercicio 5. Introducción a las proteínas

La secuencia propuesta es:

::: center
`Met--Ile--Ser--Gly--Val--Lys--His`
:::

La metionina se encuentra en el **extremo N-terminal**, mientras que la
histidina corresponde al **extremo C-terminal**.

El orden de los aminoácidos constituye la **estructura primaria** de la
proteína y condiciona las interacciones químicas que permiten su
plegamiento. Las propiedades de las cadenas laterales ---hidrofobicidad,
carga, polaridad o tamaño--- influyen en la formación de estructuras
secundarias y en la estructura tridimensional final, que a su vez
determina en gran medida la función de la proteína.

Si una mutación no sinónima sustituyera un aminoácido hidrofóbico
situado en una región interna por otro hidrofílico, podría
desestabilizar el núcleo hidrofóbico, alterar el plegamiento y modificar
la estabilidad o función de la proteína. El efecto dependería de la
posición concreta y de la importancia estructural del residuo.

**Extensión bioinformática.** Se examinó en el Protein Data Bank la
estructura **1LYZ**, correspondiente a una lisozima. La representación
tridimensional permite observar la organización de la cadena en hélices
$\alpha$, regiones $\beta$ y zonas de conexión. Una mutación puntual en
un residuo importante para estas interacciones puede modificar la
estabilidad de una estructura secundaria o del núcleo proteico,
provocando un plegamiento diferente.

# Ejercicio 6. Actividad integradora: del ADN a la proteína

Se seleccionó como secuencia de trabajo la **CDS del gen humano *HBB***,
obtenida de NCBI a partir del registro **AF007546.1**. La secuencia
codificante tiene 444 nucleótidos.

**Replicación.** Cada hebra actúa como molde para formar una nueva hebra
complementaria. La hebra codificante genera una nueva hebra
complementaria y esta, a su vez, sirve como molde para generar una nueva
hebra cuya secuencia coincide con la codificante original. De esta
manera se obtienen dos moléculas hijas, cada una formada por una hebra
parental y una nueva.

**Transcripción.** La CDS de ADN se transcribió a ARN sustituyendo las
timinas por uracilos. El transcrito comienza con el codón `AUG` y
termina con `UAA`.

**Traducción.** La traducción del ARNm produjo una proteína de **147
aminoácidos**, correspondiente a la beta-globina. La secuencia comienza
por:

::: center
`MVHLTPEEKSAVTALWGKVN...`
:::

El ADN es el punto de **mayor impacto potencial si un error queda
fijado**, ya que una mutación permanente puede transmitirse a los
transcritos y proteínas producidos posteriormente. Los errores de
transcripción o traducción, por el contrario, suelen afectar únicamente
a moléculas concretas y no modifican permanentemente la información
genética.

**Pipeline con Biopython.** En el cuaderno Jupyter se implementó un
pipeline que integra los tres procesos. A partir de la CDS de *HBB*, el
programa:

1.  genera la hebra complementaria;

2.  obtiene el ARNm;

3.  comprueba el codón de inicio, el codón de parada y que la longitud
    de la CDS sea múltiplo de tres;

4.  traduce el ARNm a proteína;

5.  informa mediante mensajes del progreso y de los resultados de cada
    etapa.

El código completo y sus salidas se incluyen en el cuaderno Jupyter
entregado junto con este informe.

# Conclusiones

Los ejercicios permiten recorrer las principales etapas que relacionan
la información genética con la función proteica. La complementariedad de
bases explica la replicación y la transcripción, mientras que el código
genético permite transformar la información del ARNm en una secuencia de
aminoácidos. Procesos como el splicing alternativo y el plegamiento
proteico muestran que la relación entre gen y función no es
estrictamente lineal, sino que existen distintos niveles de regulación y
procesamiento capaces de aumentar la diversidad funcional.

Las herramientas bioinformáticas empleadas permiten reproducir y
analizar estos procesos de manera programática, conectar las secuencias
con información almacenada en bases de datos biológicas y verificar los
resultados obtenidos manualmente.

# Fuentes de datos {#fuentes-de-datos .unnumbered}

- **NCBI Nucleotide**: CDS del gen humano *HBB*, registro AF007546.1.

- **Ensembl**: gen humano *FGFR2*, identificador ENSG00000066468.

- **RCSB Protein Data Bank**: estructura de lisozima, PDB 1LYZ.
