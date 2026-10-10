"""Contenido didáctico del simulador del dogma central.

El nivel se inspira en los materiales de la asignatura y se amplía únicamente
cuando la aclaración mejora la comprensión del proceso. La interfaz muestra una
versión resumida por defecto y deja el detalle en paneles desplegables.
"""

MODEL_NAME = "Modelo eucariota didáctico de expresión génica"

DOGMA_SPECIAL_CASES = [
    {
        "flow": "ARN → ADN",
        "name": "Transcripción inversa",
        "description": (
            "La transcriptasa inversa permite sintetizar ADN a partir de ARN, "
            "como ocurre en retrovirus y en técnicas como la RT-PCR."
        ),
    },
    {
        "flow": "ARN → ARN",
        "name": "Replicación de ARN",
        "description": (
            "Algunos virus de ARN copian su genoma usando ARN como molde sin "
            "pasar por una fase de ADN."
        ),
    },
    {
        "flow": "proteína → proteína",
        "name": "Herencia conformacional",
        "description": (
            "Los priones pueden inducir el plegamiento anómalo de otras proteínas. "
            "No es una transferencia clásica de información genética."
        ),
    },
]

REPLICATION_STEPS = [
    {
        "number": 1,
        "title": "Apertura de la doble hélice",
        "actor": "Helicasa",
        "description": (
            "La helicasa separa las dos hebras parentales al romper las interacciones "
            "entre bases complementarias y genera la horquilla de replicación."
        ),
        "result": "Cada hebra parental queda expuesta y puede funcionar como molde.",
    },
    {
        "number": 2,
        "title": "Colocación de cebadores",
        "actor": "Primasa",
        "description": (
            "La ADN polimerasa necesita un extremo 3′-OH desde el que empezar. La "
            "primasa sintetiza pequeños cebadores de ARN que proporcionan ese punto de inicio."
        ),
        "result": "La síntesis de las nuevas hebras puede comenzar.",
    },
    {
        "number": 3,
        "title": "Síntesis de la hebra líder",
        "actor": "ADN polimerasa",
        "description": (
            "La ADN polimerasa lee el molde 3′ → 5′ y sintetiza la hebra nueva 5′ → 3′. "
            "En la hebra líder puede avanzar de manera continua en la dirección de la horquilla."
        ),
        "result": "Se forma una hebra nueva continua y complementaria al molde.",
    },
    {
        "number": 4,
        "title": "Síntesis de la hebra rezagada",
        "actor": "Primasa + ADN polimerasa",
        "description": (
            "Por el antiparalelismo del ADN, la otra hebra se sintetiza en tramos cortos, "
            "los fragmentos de Okazaki. Cada fragmento también se fabrica 5′ → 3′."
        ),
        "result": "Se generan fragmentos discontinuos de ADN nuevo.",
    },
    {
        "number": 5,
        "title": "Unión y corrección",
        "actor": "ADN ligasa + mecanismos de corrección",
        "description": (
            "La ADN ligasa une los fragmentos de Okazaki y la replicación incorpora "
            "mecanismos de corrección que reducen los errores de copia."
        ),
        "result": "La hebra rezagada queda continua y aumenta la fidelidad de la copia.",
    },
    {
        "number": 6,
        "title": "Resultado semiconservativo",
        "actor": "Sistema de replicación",
        "description": (
            "Al finalizar se obtienen dos moléculas de ADN. Cada una contiene una hebra "
            "parental y una hebra sintetizada durante la replicación."
        ),
        "result": "La información genética queda duplicada antes de la división celular.",
    },
]

REPLICATION_MACHINERY = [
    {
        "name": "Helicasa",
        "type": "Enzima",
        "function": "Abre la doble hélice y forma la horquilla de replicación.",
        "modeled": True,
    },
    {
        "name": "Primasa",
        "type": "Enzima",
        "function": "Sintetiza los cebadores de ARN necesarios para iniciar la copia.",
        "modeled": True,
    },
    {
        "name": "ADN polimerasa",
        "type": "Enzima",
        "function": (
            "Añade desoxirribonucleótidos complementarios, sintetiza siempre 5′ → 3′ "
            "y participa en la corrección de errores."
        ),
        "modeled": True,
    },
    {
        "name": "ADN ligasa",
        "type": "Enzima",
        "function": "Sella las discontinuidades entre fragmentos de Okazaki.",
        "modeled": True,
    },
]

REPLICATION_MODELS = [
    {
        "name": "Conservativo",
        "description": (
            "La molécula parental permanecería completa y se sintetizaría otra molécula "
            "formada únicamente por ADN nuevo."
        ),
    },
    {
        "name": "Semiconservativo",
        "description": (
            "Cada molécula hija conserva una hebra parental y contiene una hebra nueva. "
            "Es el modelo aceptado."
        ),
    },
    {
        "name": "Dispersivo",
        "description": (
            "Cada hebra hija contendría fragmentos de ADN parental y nuevo intercalados."
        ),
    },
]

REPLICATION_EVIDENCE = (
    "Meselson y Stahl demostraron en 1958 que la replicación es semiconservativa "
    "mediante marcaje isotópico con nitrógeno y centrifugación en gradiente de densidad."
)

TRANSCRIPTION_STEPS = [
    {
        "number": 1,
        "title": "Reconocimiento e iniciación",
        "actor": "Promotor + ARN polimerasa",
        "description": (
            "La ARN polimerasa reconoce una región promotora situada antes de la secuencia "
            "que se transcribe, se posiciona y abre localmente la doble hélice."
        ),
        "result": "Se forma una burbuja de transcripción y queda accesible la hebra molde.",
    },
    {
        "number": 2,
        "title": "Elongación",
        "actor": "ARN polimerasa",
        "description": (
            "La enzima avanza sobre la hebra molde en dirección 3′ → 5′ mientras incorpora "
            "ribonucleótidos complementarios al extremo 3′ del ARN naciente. El ARN crece 5′ → 3′."
        ),
        "result": "Se forma un transcrito de ARN complementario a la hebra molde.",
    },
    {
        "number": 3,
        "title": "Complementariedad ADN–ARN",
        "actor": "Apareamiento de bases",
        "description": (
            "A del molde se aparea con U en ARN, T con A, C con G y G con C. Por ello, "
            "la secuencia del ARN coincide con la hebra codificante salvo por U en lugar de T."
        ),
        "result": "La información de la región transcrita queda copiada en ARN.",
    },
    {
        "number": 4,
        "title": "Terminación",
        "actor": "ARN polimerasa + señal de terminación",
        "description": (
            "La síntesis finaliza cuando el complejo de transcripción recibe una señal de terminación. "
            "El simulador usa el final de la secuencia porque la entrada no incluye anotaciones regulatorias."
        ),
        "result": "Se libera un transcrito primario de ARN.",
    },
    {
        "number": 5,
        "title": "Procesamiento del pre-ARNm",
        "actor": "Cap 5′ · cola poli-A · splicing",
        "description": (
            "En eucariotas, el pre-ARNm se modifica antes de la traducción: se añade un cap 5′, "
            "una cola poli-A en 3′ y se eliminan intrones mediante splicing, uniendo los exones."
        ),
        "result": "Se obtiene un ARNm maduro, más estable y preparado para su utilización.",
    },
]

TRANSCRIPTION_MACHINERY = [
    {
        "name": "ARN polimerasa",
        "type": "Enzima",
        "function": "Lee la hebra molde 3′ → 5′ y sintetiza ARN 5′ → 3′.",
        "modeled": True,
    },
    {
        "name": "Promotor",
        "type": "Región reguladora del ADN",
        "function": "Señala el entorno donde se inicia la transcripción de un gen.",
        "modeled": False,
    },
    {
        "name": "Ribonucleótidos",
        "type": "A, U, C y G",
        "function": "Son las unidades que se incorporan para formar la cadena de ARN.",
        "modeled": True,
    },
    {
        "name": "Procesamiento del ARNm",
        "type": "Maduración eucariota",
        "function": "Incluye cap 5′, cola poli-A y splicing del transcrito primario.",
        "modeled": False,
    },
]

RNA_TYPES = [
    {
        "name": "ARNm",
        "full_name": "ARN mensajero",
        "description": (
            "Transporta la información del gen en forma de codones hasta el ribosoma, "
            "donde servirá de molde para la síntesis proteica."
        ),
    },
    {
        "name": "ARNt",
        "full_name": "ARN de transferencia",
        "description": (
            "Actúa como adaptador: contiene un anticodón complementario a un codón del ARNm "
            "y transporta el aminoácido correspondiente."
        ),
    },
    {
        "name": "ARNr",
        "full_name": "ARN ribosómico",
        "description": (
            "Forma parte esencial del ribosoma y participa tanto en el posicionamiento de ARNm/ARNt "
            "como en la formación de los enlaces peptídicos."
        ),
    },
]

RNA_PROCESSING = [
    {
        "name": "Cap 5′",
        "description": "Protege el extremo 5′ y facilita el reconocimiento del ARNm durante su utilización.",
    },
    {
        "name": "Cola poli-A",
        "description": "Se añade al extremo 3′ y contribuye a la estabilidad y vida media del ARNm.",
    },
    {
        "name": "Splicing",
        "description": "Elimina intrones del pre-ARNm y une los exones que permanecerán en el ARNm maduro.",
    },
    {
        "name": "Splicing alternativo",
        "description": (
            "Permite combinar exones de distintas formas y generar varios ARNm —y potencialmente "
            "proteínas diferentes— a partir de un mismo gen."
        ),
    },
]

INTRON_EXON_CONTEXT = {
    "introns": (
        "Secuencias presentes en el transcrito primario que se eliminan durante el splicing. "
        "Pueden contener regiones reguladoras y participar en splicing alternativo."
    ),
    "exons": (
        "Secuencias que permanecen en el ARN maduro después del splicing. Pueden incluir "
        "regiones codificantes y regiones no traducidas (UTR)."
    ),
}

TRANSLATION_STEPS = [
    {
        "number": 1,
        "title": "Iniciación",
        "actor": "Ribosoma + ARNm + ARNt",
        "description": (
            "El ribosoma se ensambla sobre el ARNm y establece un marco de lectura. Para mantener "
            "el modelo reproducible, el simulador utiliza el primer AUG como codón de inicio."
        ),
        "result": "Comienza la síntesis de la cadena polipeptídica con metionina.",
    },
    {
        "number": 2,
        "title": "Reconocimiento codón–anticodón",
        "actor": "ARNt",
        "description": (
            "El ribosoma lee el ARNm en grupos de tres bases. El anticodón del ARNt se aparea de "
            "forma complementaria y antiparalela con el codón y aporta su aminoácido."
        ),
        "result": "Cada codón se relaciona con un aminoácido según el código genético.",
    },
    {
        "number": 3,
        "title": "Elongación",
        "actor": "Ribosoma + ARNt",
        "description": (
            "El ribosoma enlaza los aminoácidos mediante enlaces peptídicos y avanza al siguiente "
            "codón, repitiendo el ciclo de reconocimiento e incorporación."
        ),
        "result": "La cadena polipeptídica crece siguiendo el orden codificado por el ARNm.",
    },
    {
        "number": 4,
        "title": "Terminación",
        "actor": "Ribosoma + factores de terminación",
        "description": (
            "Cuando se alcanza UAA, UAG o UGA no existe un ARNt que aporte un aminoácido. "
            "La señal STOP provoca la finalización de la síntesis y la liberación del polipéptido."
        ),
        "result": "La cadena polipeptídica queda liberada.",
    },
    {
        "number": 5,
        "title": "Plegamiento y función",
        "actor": "Cadena polipeptídica",
        "description": (
            "La secuencia lineal de aminoácidos debe adquirir una estructura tridimensional adecuada "
            "para realizar su función biológica. El simulador se detiene en la secuencia primaria."
        ),
        "result": "El polipéptido puede convertirse en una proteína funcional.",
    },
]

TRANSLATION_MACHINERY = [
    {
        "name": "ARNm",
        "type": "Molécula de información",
        "function": "Aporta la secuencia de codones que determina el orden de los aminoácidos.",
        "modeled": True,
    },
    {
        "name": "Ribosoma",
        "type": "Complejo de ARNr y proteínas",
        "function": "Lee el ARNm, coordina los ARNt y cataliza la síntesis del polipéptido.",
        "modeled": True,
    },
    {
        "name": "ARNt",
        "type": "ARN adaptador",
        "function": "Reconoce codones mediante su anticodón y transporta un aminoácido.",
        "modeled": True,
    },
    {
        "name": "ARNr",
        "type": "ARN ribosómico",
        "function": "Forma parte del ribosoma y participa en la catálisis del enlace peptídico.",
        "modeled": False,
    },
    {
        "name": "Factores de traducción",
        "type": "Proteínas auxiliares",
        "function": "Coordinan las fases de iniciación, elongación y terminación.",
        "modeled": False,
    },
]

MODEL_ASSUMPTIONS = [
    "La entrada se interpreta como la hebra codificante de ADN escrita 5′ → 3′.",
    (
        "La replicación muestra una única horquilla que avanza de izquierda a derecha para distinguir "
        "con claridad hebra líder y rezagada."
    ),
    (
        "El tamaño de los fragmentos de Okazaki se elige con fines de visualización y puede modificarse."
    ),
    (
        "La secuencia de entrada no incluye anotaciones de promotores, intrones, exones o terminadores; "
        "estos procesos se explican, pero no se inventan posiciones concretas."
    ),
    (
        "El ARNm usado en la traducción conserva la secuencia transcrita porque no es posible inferir "
        "un patrón de splicing fiable a partir de una secuencia aislada sin anotación."
    ),
    (
        "La traducción utiliza el primer AUG como inicio y el código genético estándar; se detiene en "
        "UAA, UAG o UGA cuando aparecen en el mismo marco de lectura."
    ),
]
