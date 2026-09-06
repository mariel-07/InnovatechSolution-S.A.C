/* =========================================================
INNOVATECH SOLUTIONS S.A.C.
FRONTEND JAVASCRIPT
========================================================= */

/* =========================================================
CONFIGURACIÓN DEL BACKEND
========================================================= */

const API_BASE_URL = "http://localhost:8000";

/* =========================================================
CAMBIO DE PESTAÑAS
========================================================= */

function switchTab(tabId, button) {


// Ocultar todas las pestañas
document
    .querySelectorAll(".tab-content")
    .forEach(tab => {
        tab.classList.add("hidden");
    });


// Quitar estado activo de todos los botones
document
    .querySelectorAll(".tab-btn")
    .forEach(btn => {
        btn.classList.remove("active");
    });


// Mostrar pestaña seleccionada
const selectedTab = document.getElementById(tabId);

if (selectedTab) {
    selectedTab.classList.remove("hidden");
}


// Activar botón seleccionado
if (button) {
    button.classList.add("active");
}


}

/* =========================================================
PREDICCIÓN MACHINE LEARNING
========================================================= */

async function predictML(event) {


event.preventDefault();


const button = document.getElementById("btn-predict-ml");

const resultBox = document.getElementById("result-ml");


// Obtener datos del formulario
const data = {

    presupuesto_usd:
        parseFloat(
            document.getElementById("ml-presupuesto").value
        ),

    deadline_dias:
        parseInt(
            document.getElementById("ml-deadline").value
        ),

    tipo_servicio:
        document.getElementById("ml-servicio").value,

    infraestructura_cloud:
        parseInt(
            document.getElementById("ml-infra").value
        )
};


// Estado de carga
button.classList.add("loading");

button.innerHTML = `
    <i class="fa-solid fa-spinner fa-spin"></i>
    PROCESANDO PREDICCIÓN...
`;


try {

    const response = await fetch(
        `${API_BASE_URL}/api/predecir-ml`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        }
    );


    // Verificar respuesta HTTP
    if (!response.ok) {

        throw new Error(
            `Error HTTP: ${response.status}`
        );

    }


    const result = await response.json();


    console.log(
        "Resultado Machine Learning:",
        result
    );


    /* =================================================
       MOSTRAR RESULTADO
    ================================================== */

    document.getElementById(
        "res-ml-horas"
    ).innerText =
        `${result.horas_hombre} hrs`;


    document.getElementById(
        "res-ml-costo"
    ).innerText =
        `$${Number(result.costo_usd).toLocaleString(
            "en-US",
            {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }
        )} USD`;


    resultBox.classList.remove("hidden");


    // Desplazar hacia el resultado
    resultBox.scrollIntoView({
        behavior: "smooth",
        block: "nearest"
    });

}

catch (error) {

    console.error(
        "Error Machine Learning:",
        error
    );


    alert(
        "No se pudo conectar con el servidor Python.\n\n" +
        "Verifica que app.py esté ejecutándose en:\n" +
        "http://localhost:8000"
    );

}

finally {

    // Restaurar botón
    button.classList.remove("loading");

    button.innerHTML = `
        <i class="fa-solid fa-wand-magic-sparkles"></i>
        REALIZAR PREDICCIÓN
    `;

}


}

/* =========================================================
PREDICCIÓN RED NEURONAL
========================================================= */

async function predictNN(event) {


event.preventDefault();


const button =
    document.getElementById("btn-predict-nn");


const resultBox =
    document.getElementById("result-nn");


// Obtener datos del formulario
const data = {

    presupuesto_estimado:
        parseFloat(
            document.getElementById("nn-presupuesto").value
        ),

    deadline_dias:
        parseInt(
            document.getElementById("nn-deadline").value
        ),

    cantidad_bugs:
        parseInt(
            document.getElementById("nn-bugs").value
        ),

    numero_desarrolladores:
        parseInt(
            document.getElementById("nn-devs").value
        ),

    infraestructura_nube_previa:
        document.getElementById("nn-infra").value,

    renovacion_contrato:
        document.getElementById("nn-renovacion").value,

    tipo_servicio:
        "Sistema SaaS"
};


// Estado de carga
button.classList.add("loading");

button.innerHTML = `
    <i class="fa-solid fa-spinner fa-spin"></i>
    PROCESANDO RED NEURONAL...
`;


try {

    const response = await fetch(
        `${API_BASE_URL}/api/predecir-nn`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        }
    );


    // Verificar respuesta
    if (!response.ok) {

        throw new Error(
            `Error HTTP: ${response.status}`
        );

    }


    const result = await response.json();


    console.log(
        "Resultado Red Neuronal:",
        result
    );


    /* =================================================
       MOSTRAR RESULTADO
    ================================================== */

    document.getElementById(
        "res-nn-horas"
    ).innerText =
        `${result.horas_hombre} hrs`;


    document.getElementById(
        "res-nn-costo"
    ).innerText =
        `S/ ${Number(result.costo_pen).toLocaleString(
            "es-PE",
            {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }
        )} PEN`;


    resultBox.classList.remove("hidden");


    // Desplazar hacia el resultado
    resultBox.scrollIntoView({
        behavior: "smooth",
        block: "nearest"
    });

}

catch (error) {

    console.error(
        "Error Red Neuronal:",
        error
    );


    alert(
        "No se pudo conectar con el servidor Python.\n\n" +
        "Verifica que app.py esté ejecutándose en:\n" +
        "http://localhost:8000"
    );

}

finally {

    // Restaurar botón
    button.classList.remove("loading");

    button.innerHTML = `
        <i class="fa-solid fa-brain"></i>
        REALIZAR PREDICCIÓN
    `;

}


}

/* =========================================================
INICIO
========================================================= */

document.addEventListener(
"DOMContentLoaded",
() => {


    // Iniciar mostrando Machine Learning
    switchTab(
        "tab-ml",
        document.getElementById("btn-ml")
    );

}


);
