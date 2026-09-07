/* =========================================================
   INNOVATECH SOLUTIONS S.A.C.
   FRONTEND JAVASCRIPT
   MACHINE LEARNING + RED NEURONAL + DATASETS
   MONEDA: SOLES PERUANOS (PEN)
========================================================= */


/* =========================================================
   CONFIGURACIÓN API
========================================================= */

const API_BASE_URL =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1" ||
    window.location.protocol === "file:"
        ? "http://localhost:8000"
        : "";


/* =========================================================
   VARIABLES DE TABLA
========================================================= */

let currentPage = 1;

const rowsPerPage = 10;

let currentDataset = "datos.csv";

let totalRecords = 0;


/* =========================================================
   INICIO
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* -----------------------------------------------------
       FECHA
    ----------------------------------------------------- */

    const dateElement =
        document.getElementById("current-date");

    if (dateElement) {

        const today = new Date();

        dateElement.innerText =
            today.toLocaleDateString(
                "es-PE",
                {
                    day: "2-digit",
                    month: "long",
                    year: "numeric"
                }
            );
    }


    /* -----------------------------------------------------
       DASHBOARD
    ----------------------------------------------------- */

    showSection(
        "dashboard",
        document.querySelector(".nav-item.active")
    );


    /* -----------------------------------------------------
       BACKEND
    ----------------------------------------------------- */

    checkBackend();


    /* -----------------------------------------------------
       DATASET
    ----------------------------------------------------- */

    const datasetSelect =
        document.getElementById(
            "dataset-select"
        );

    if (datasetSelect) {

        if (
            datasetSelect.value === "datos.csv" ||
            datasetSelect.value === ""
        ) {

            datasetSelect.value =
                "datos.csv";
        }

        currentDataset =
            datasetSelect.value ||
            "datos.csv";

        datasetSelect.addEventListener(
            "change",
            () => {

                currentDataset =
                    datasetSelect.value;

                currentPage = 1;

                loadData();
            }
        );
    }


    /* -----------------------------------------------------
       BUSCADOR
    ----------------------------------------------------- */

    const searchInput =
        document.getElementById(
            "data-search"
        );

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            debounce(
                () => {

                    currentPage = 1;

                    loadData();

                },
                400
            )
        );
    }


    /* -----------------------------------------------------
       FORMULARIO ML
    ----------------------------------------------------- */

    const mlForm =
        document.getElementById(
            "ml-form"
        );

    if (mlForm) {

        mlForm.addEventListener(
            "submit",
            predictML
        );
    }


    /* -----------------------------------------------------
       FORMULARIO NN
    ----------------------------------------------------- */

    const nnForm =
        document.getElementById(
            "nn-form"
        );

    if (nnForm) {

        nnForm.addEventListener(
            "submit",
            predictNN
        );
    }


    /* -----------------------------------------------------
       PAGINACIÓN
    ----------------------------------------------------- */

    const prevButton =
        document.getElementById(
            "prev-page"
        );

    if (prevButton) {

        prevButton.addEventListener(
            "click",
            () => changePage(-1)
        );
    }


    const nextButton =
        document.getElementById(
            "next-page"
        );

    if (nextButton) {

        nextButton.addEventListener(
            "click",
            () => changePage(1)
        );
    }


    /* -----------------------------------------------------
       CARGAR DATOS
    ----------------------------------------------------- */

    loadData();

});


/* =========================================================
   NAVEGACIÓN
========================================================= */

function showSection(
    sectionId,
    button = null
) {

    document
        .querySelectorAll(".page-section")
        .forEach(section => {

            section.classList.remove(
                "active-section"
            );
        });


    document
        .querySelectorAll(".nav-item")
        .forEach(item => {

            item.classList.remove(
                "active"
            );
        });


    const section =
        document.getElementById(
            sectionId
        );

    if (section) {

        section.classList.add(
            "active-section"
        );
    }


    if (button) {

        button.classList.add(
            "active"
        );

    } else {

        const matchingButton =
            document.querySelector(
                `.nav-item[onclick*="${sectionId}"]`
            );

        if (matchingButton) {

            matchingButton.classList.add(
                "active"
            );
        }
    }


    const titles = {

        dashboard:
            "Centro de Inteligencia",

        "ml-section":
            "Machine Learning",

        "nn-section":
            "Red Neuronal",

        "datos-section":
            "Base de Datos"
    };


    const title =
        document.getElementById(
            "page-title"
        );

    if (title) {

        title.innerText =
            titles[sectionId] ||
            "Centro de Inteligencia";
    }


    document
        .querySelector(".sidebar")
        ?.classList.remove(
            "mobile-open"
        );
}


/* =========================================================
   SIDEBAR MOBILE
========================================================= */

function toggleSidebar() {

    document
        .querySelector(".sidebar")
        ?.classList.toggle(
            "mobile-open"
        );
}


/* =========================================================
   VERIFICAR BACKEND
========================================================= */

async function checkBackend() {

    const statusElement =
        document.getElementById(
            "system-status"
        );

    const statusText =
        document.getElementById(
            "status-text"
        );


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/api/estado`
            );


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const result =
            await response.json();


        console.log(
            "Estado del backend:",
            result
        );


        if (statusElement) {

            statusElement.classList.add(
                "online"
            );

            statusElement.classList.remove(
                "offline"
            );
        }


        if (statusText) {

            statusText.innerText =
                "SISTEMA OPERATIVO";
        }


    } catch (error) {

        console.error(
            "Error backend:",
            error
        );


        if (statusElement) {

            statusElement.classList.add(
                "offline"
            );

            statusElement.classList.remove(
                "online"
            );
        }


        if (statusText) {

            statusText.innerText =
                "BACKEND DESCONECTADO";
        }
    }
}


/* =========================================================
   MACHINE LEARNING
   RANDOM FOREST
========================================================= */

async function predictML(event) {

    event.preventDefault();


    const button =
        document.getElementById(
            "btn-predict-ml"
        );


    const resultBox =
        document.getElementById(
            "result-ml"
        );


    if (!button) {

        console.error(
            "No existe btn-predict-ml"
        );

        return;
    }


    /* -----------------------------------------------------
       ELEMENTOS
    ----------------------------------------------------- */

    const presupuestoElement =
        document.getElementById(
            "ml-presupuesto"
        );

    const deadlineElement =
        document.getElementById(
            "ml-deadline"
        );

    const bugsElement =
        document.getElementById(
            "ml-bugs"
        );

    const devsElement =
        document.getElementById(
            "ml-devs"
        );

    const servicioElement =
        document.getElementById(
            "ml-servicio"
        );

    const infraElement =
        document.getElementById(
            "ml-infra"
        );

    const renovacionElement =
        document.getElementById(
            "ml-renovacion"
        );


    if (
        !presupuestoElement ||
        !deadlineElement ||
        !bugsElement ||
        !devsElement ||
        !servicioElement ||
        !infraElement ||
        !renovacionElement
    ) {

        alert(
            "Faltan campos del formulario de Machine Learning."
        );

        return;
    }


    /* -----------------------------------------------------
       DATOS
    ----------------------------------------------------- */

    const data = {

        presupuesto_estimado:
            parseFloat(
                presupuestoElement.value
            ),

        deadline_dias:
            parseInt(
                deadlineElement.value,
                10
            ),

        cantidad_bugs:
            parseInt(
                bugsElement.value,
                10
            ),

        numero_desarrolladores:
            parseInt(
                devsElement.value,
                10
            ),

        tipo_servicio:
            servicioElement.value,

        infraestructura_nube_previa:
            infraElement.value,

        renovacion_contrato:
            renovacionElement.value
    };


    console.log(
        "Datos enviados Random Forest:",
        data
    );


    /* -----------------------------------------------------
       VALIDACIONES
    ----------------------------------------------------- */

    if (
        !Number.isFinite(
            data.presupuesto_estimado
        ) ||
        !Number.isFinite(
            data.deadline_dias
        ) ||
        !Number.isFinite(
            data.cantidad_bugs
        ) ||
        !Number.isFinite(
            data.numero_desarrolladores
        )
    ) {

        alert(
            "Completa correctamente todos los campos numéricos."
        );

        return;
    }


    if (
        data.presupuesto_estimado <= 0
    ) {

        alert(
            "El presupuesto debe ser mayor que 0."
        );

        return;
    }


    if (
        data.deadline_dias <= 0
    ) {

        alert(
            "El deadline debe ser mayor que 0 días."
        );

        return;
    }


    if (
        data.cantidad_bugs < 0
    ) {

        alert(
            "La cantidad de bugs no puede ser negativa."
        );

        return;
    }


    if (
        data.numero_desarrolladores <= 0
    ) {

        alert(
            "Debe existir al menos un desarrollador."
        );

        return;
    }


    /* -----------------------------------------------------
       LOADING
    ----------------------------------------------------- */

    button.disabled = true;

    button.innerHTML = `
        <i class="fa-solid fa-spinner fa-spin"></i>
        PROCESANDO PREDICCIÓN...
    `;


    try {

        /* -------------------------------------------------
           PETICIÓN
        ------------------------------------------------- */

        const response =
            await fetch(
                `${API_BASE_URL}/api/predecir-ml`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(data)
                }
            );


        if (!response.ok) {

            const errorText =
                await response.text();

            throw new Error(
                `Error HTTP ${response.status}: ${errorText}`
            );
        }


        const result =
            await response.json();


        console.log(
            "Respuesta Random Forest:",
            result
        );


        /* -------------------------------------------------
           ERROR BACKEND
        ------------------------------------------------- */

        if (!result.success) {

            throw new Error(
                result.error ||
                "El modelo no pudo realizar la predicción."
            );
        }


        /* -------------------------------------------------
           HORAS
        ------------------------------------------------- */

        const horas =
            Number(
                result.horas_hombre
            );


        if (!Number.isFinite(horas)) {

            throw new Error(
                "La API devolvió horas-hombre inválidas."
            );
        }


        const horasElement =
            document.getElementById(
                "res-ml-horas"
            );


        if (horasElement) {

            horasElement.innerText =
                `${horas.toLocaleString(
                    "es-PE",
                    {
                        minimumFractionDigits: 1,
                        maximumFractionDigits: 1
                    }
                )} hrs`;
        }


        /* -------------------------------------------------
           COSTO EN SOLES
        ------------------------------------------------- */

        const costo =
            Number(
                result.costo_pen
            );


        if (!Number.isFinite(costo)) {

            throw new Error(
                "La API no devolvió una cotización válida en soles."
            );
        }


        const costoElement =
            document.getElementById(
                "res-ml-costo"
            );


        if (costoElement) {

            costoElement.innerText =
                `S/ ${costo.toLocaleString(
                    "es-PE",
                    {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    }
                )} PEN`;
        }


        /* -------------------------------------------------
           TARIFA
        ------------------------------------------------- */

        const tarifaElement =
            document.getElementById(
                "res-ml-tarifa"
            );


        if (tarifaElement) {

            const tarifa =
                Number(
                    result.tarifa_hora
                );

            if (
                Number.isFinite(tarifa)
            ) {

                tarifaElement.innerText =
                    `S/ ${tarifa.toLocaleString(
                        "es-PE",
                        {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        }
                    )}/hora`;
            }
        }


        /* -------------------------------------------------
           MODELO
        ------------------------------------------------- */

        const modelElement =
            document.getElementById(
                "res-ml-modelo"
            );


        if (modelElement) {

            modelElement.innerText =
                result.modelo ||
                "Random Forest Regressor";
        }


        /* -------------------------------------------------
           MOSTRAR RESULTADO
        ------------------------------------------------- */

        if (resultBox) {

            resultBox.classList.remove(
                "hidden"
            );

            resultBox.classList.add(
                "show"
            );


            resultBox.scrollIntoView({

                behavior:
                    "smooth",

                block:
                    "center"
            });
        }


    } catch (error) {

        console.error(
            "Error Random Forest:",
            error
        );


        mostrarError(
            "result-ml",
            error.message
        );


    } finally {

        button.disabled = false;

        button.innerHTML = `
            <i class="fa-solid fa-wand-magic-sparkles"></i>
            EJECUTAR PREDICCIÓN
        `;
    }
}


/* =========================================================
   RED NEURONAL
   MLP REGRESSOR
========================================================= */

async function predictNN(event) {

    event.preventDefault();


    const button =
        document.getElementById(
            "btn-predict-nn"
        );


    const resultBox =
        document.getElementById(
            "result-nn"
        );


    if (!button) {

        console.error(
            "No existe btn-predict-nn"
        );

        return;
    }


    /* -----------------------------------------------------
       ELEMENTOS
    ----------------------------------------------------- */

    const presupuestoElement =
        document.getElementById(
            "nn-presupuesto"
        );

    const deadlineElement =
        document.getElementById(
            "nn-deadline"
        );

    const bugsElement =
        document.getElementById(
            "nn-bugs"
        );

    const devsElement =
        document.getElementById(
            "nn-devs"
        );

    const servicioElement =
        document.getElementById(
            "nn-servicio"
        );

    const infraElement =
        document.getElementById(
            "nn-infra"
        );

    const renovacionElement =
        document.getElementById(
            "nn-renovacion"
        );


    if (
        !presupuestoElement ||
        !deadlineElement ||
        !bugsElement ||
        !devsElement ||
        !servicioElement ||
        !infraElement ||
        !renovacionElement
    ) {

        alert(
            "Faltan campos del formulario de Red Neuronal."
        );

        return;
    }


    /* -----------------------------------------------------
       DATOS
    ----------------------------------------------------- */

    const data = {

        presupuesto_estimado:
            parseFloat(
                presupuestoElement.value
            ),

        deadline_dias:
            parseInt(
                deadlineElement.value,
                10
            ),

        cantidad_bugs:
            parseInt(
                bugsElement.value,
                10
            ),

        numero_desarrolladores:
            parseInt(
                devsElement.value,
                10
            ),

        tipo_servicio:
            servicioElement.value,

        infraestructura_nube_previa:
            infraElement.value,

        renovacion_contrato:
            renovacionElement.value
    };


    console.log(
        "Datos enviados Red Neuronal:",
        data
    );


    /* -----------------------------------------------------
       VALIDACIONES
    ----------------------------------------------------- */

    if (
        !Number.isFinite(
            data.presupuesto_estimado
        ) ||
        !Number.isFinite(
            data.deadline_dias
        ) ||
        !Number.isFinite(
            data.cantidad_bugs
        ) ||
        !Number.isFinite(
            data.numero_desarrolladores
        )
    ) {

        alert(
            "Completa correctamente todos los campos numéricos."
        );

        return;
    }


    if (
        data.presupuesto_estimado <= 0
    ) {

        alert(
            "El presupuesto debe ser mayor que 0."
        );

        return;
    }


    if (
        data.deadline_dias <= 0
    ) {

        alert(
            "El deadline debe ser mayor que 0 días."
        );

        return;
    }


    if (
        data.cantidad_bugs < 0
    ) {

        alert(
            "La cantidad de bugs no puede ser negativa."
        );

        return;
    }


    if (
        data.numero_desarrolladores <= 0
    ) {

        alert(
            "Debe existir al menos un desarrollador."
        );

        return;
    }


    /* -----------------------------------------------------
       LOADING
    ----------------------------------------------------- */

    button.disabled = true;

    button.innerHTML = `
        <i class="fa-solid fa-spinner fa-spin"></i>
        PROCESANDO RED NEURONAL...
    `;


    try {

        /* -------------------------------------------------
           PETICIÓN
        ------------------------------------------------- */

        const response =
            await fetch(
                `${API_BASE_URL}/api/predecir-nn`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(data)
                }
            );


        if (!response.ok) {

            const errorText =
                await response.text();

            throw new Error(
                `Error HTTP ${response.status}: ${errorText}`
            );
        }


        const result =
            await response.json();


        console.log(
            "Respuesta Red Neuronal:",
            result
        );


        /* -------------------------------------------------
           ERROR BACKEND
        ------------------------------------------------- */

        if (!result.success) {

            throw new Error(
                result.error ||
                "La red neuronal no pudo realizar la predicción."
            );
        }


        /* -------------------------------------------------
           HORAS
        ------------------------------------------------- */

        const horas =
            Number(
                result.horas_hombre
            );


        if (!Number.isFinite(horas)) {

            throw new Error(
                "La red neuronal devolvió horas-hombre inválidas."
            );
        }


        const horasElement =
            document.getElementById(
                "res-nn-horas"
            );


        if (horasElement) {

            horasElement.innerText =
                `${horas.toLocaleString(
                    "es-PE",
                    {
                        minimumFractionDigits: 1,
                        maximumFractionDigits: 1
                    }
                )} hrs`;
        }


        /* -------------------------------------------------
           COSTO EN SOLES
        ------------------------------------------------- */

        const costo =
            Number(
                result.costo_pen
            );


        if (!Number.isFinite(costo)) {

            throw new Error(
                "La API no devolvió una cotización válida en soles."
            );
        }


        const costoElement =
            document.getElementById(
                "res-nn-costo"
            );


        if (costoElement) {

            costoElement.innerText =
                `S/ ${costo.toLocaleString(
                    "es-PE",
                    {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    }
                )} PEN`;
        }


        /* -------------------------------------------------
           TARIFA
        ------------------------------------------------- */

        const tarifaElement =
            document.getElementById(
                "res-nn-tarifa"
            );


        if (tarifaElement) {

            const tarifa =
                Number(
                    result.tarifa_hora
                );

            if (
                Number.isFinite(tarifa)
            ) {

                tarifaElement.innerText =
                    `S/ ${tarifa.toLocaleString(
                        "es-PE",
                        {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        }
                    )}/hora`;
            }
        }


        /* -------------------------------------------------
           MODELO
        ------------------------------------------------- */

        const modelElement =
            document.getElementById(
                "res-nn-modelo"
            );


        if (modelElement) {

            modelElement.innerText =
                result.modelo ||
                "MLP Regressor - Red Neuronal";
        }


        /* -------------------------------------------------
           MOSTRAR RESULTADO
        ------------------------------------------------- */

        if (resultBox) {

            resultBox.classList.remove(
                "hidden"
            );

            resultBox.classList.add(
                "show"
            );


            resultBox.scrollIntoView({

                behavior:
                    "smooth",

                block:
                    "center"
            });
        }


    } catch (error) {

        console.error(
            "Error Red Neuronal:",
            error
        );


        mostrarError(
            "result-nn",
            error.message
        );


    } finally {

        button.disabled = false;

        button.innerHTML = `
            <i class="fa-solid fa-brain"></i>
            EJECUTAR PREDICCIÓN
        `;
    }
}


/* =========================================================
   MOSTRAR ERROR
========================================================= */

function mostrarError(
    resultId,
    mensaje
) {

    const resultBox =
        document.getElementById(
            resultId
        );


    if (!resultBox) {

        alert(
            "No se pudo realizar la predicción.\n\n" +
            mensaje
        );

        return;
    }


    resultBox.classList.remove(
        "hidden"
    );

    resultBox.classList.add(
        "show"
    );


    const errorElement =
        resultBox.querySelector(
            ".prediction-error"
        );


    if (errorElement) {

        errorElement.innerText =
            mensaje;

    } else {

        alert(
            "No se pudo realizar la predicción.\n\n" +
            mensaje
        );
    }
}


/* =========================================================
   CARGAR DATOS DEL CSV
========================================================= */

async function loadData() {

    const tableBody =
        document.getElementById(
            "data-table-body"
        );


    if (!tableBody) {

        return;
    }


    const searchInput =
        document.getElementById(
            "data-search"
        );


    const search =
        searchInput
            ? searchInput.value.trim()
            : "";


    /* -----------------------------------------------------
       LOADING
    ----------------------------------------------------- */

    tableBody.innerHTML = `
        <tr>
            <td colspan="10" class="table-loading">
                <i class="fa-solid fa-spinner fa-spin"></i>
                Cargando registros...
            </td>
        </tr>
    `;


    try {

        const params =
            new URLSearchParams({

                archivo:
                    currentDataset,

                page:
                    currentPage,

                limit:
                    rowsPerPage,

                search:
                    search
            });


        console.log(
            "Consultando dataset:",
            currentDataset
        );


        const response =
            await fetch(
                `${API_BASE_URL}/api/datos?${params.toString()}`
            );


        if (!response.ok) {

            const errorText =
                await response.text();

            throw new Error(
                `Error HTTP ${response.status}: ${errorText}`
            );
        }


        const result =
            await response.json();


        console.log(
            "Datos recibidos:",
            result
        );


        if (!result.success) {

            throw new Error(
                result.error ||
                "No se pudieron cargar los datos."
            );
        }


        /* -------------------------------------------------
           TOTAL
        ------------------------------------------------- */

        totalRecords =
            Number(
                result.total || 0
            );


        /* -------------------------------------------------
           RENDER
        ------------------------------------------------- */

        renderTable(
            result.datos
        );


        /* -------------------------------------------------
           PAGINACIÓN
        ------------------------------------------------- */

        updatePagination(
            result.total,
            result.page,
            result.limit
        );


        /* -------------------------------------------------
           TOTAL DASHBOARD
        ------------------------------------------------- */

        const totalElement =
            document.getElementById(
                "data-total"
            );


        if (totalElement) {

            totalElement.innerText =
                Number(
                    result.total
                ).toLocaleString(
                    "es-PE"
                );
        }


        /* -------------------------------------------------
           BADGE
        ------------------------------------------------- */

        const badge =
            document.getElementById(
                "records-badge"
            );


        if (badge) {

            badge.innerText =
                `${Number(
                    result.total
                ).toLocaleString(
                    "es-PE"
                )} registros`;
        }


        /* -------------------------------------------------
           TÍTULO
        ------------------------------------------------- */

        const tableTitle =
            document.getElementById(
                "table-title"
            );


        if (tableTitle) {

            tableTitle.innerText =
                currentDataset;
        }


        /* -------------------------------------------------
           CABECERAS
        ------------------------------------------------- */

        renderTableHeaders(
            result.columnas
        );


    } catch (error) {

        console.error(
            "Error cargando datos:",
            error
        );


        tableBody.innerHTML = `
            <tr>
                <td colspan="10" class="table-error">

                    <i class="fa-solid fa-triangle-exclamation"></i>

                    <strong>
                        No se pudieron cargar los datos
                    </strong>

                    <br><br>

                    ${escapeHTML(
                        error.message
                    )}

                    <br><br>

                    <small>
                        Verifica que FastAPI esté ejecutándose
                        en http://localhost:8000
                    </small>

                </td>
            </tr>
        `;
    }
}


/* =========================================================
   RENDERIZAR CABECERAS
========================================================= */

function renderTableHeaders(columns) {

    const tableHead =
        document.getElementById(
            "data-table-head"
        );


    if (
        !tableHead ||
        !columns ||
        columns.length === 0
    ) {

        return;
    }


    tableHead.innerHTML =
        columns
            .map(column => {

                return `
                    <th>
                        ${escapeHTML(
                            formatColumnName(
                                column
                            )
                        )}
                    </th>
                `;

            })
            .join("");
}


/* =========================================================
   RENDERIZAR TABLA
========================================================= */

function renderTable(data) {

    const tableBody =
        document.getElementById(
            "data-table-body"
        );


    if (!tableBody) {

        return;
    }


    if (
        !data ||
        data.length === 0
    ) {

        tableBody.innerHTML = `
            <tr>

                <td colspan="10" class="empty-table">

                    <i class="fa-solid fa-folder-open"></i>

                    <br>

                    No se encontraron registros.

                </td>

            </tr>
        `;

        return;
    }


    tableBody.innerHTML =
        data
            .map(row => {

                return `

                    <tr>

                        <td>
                            ${escapeHTML(
                                row.id_proyecto
                            )}
                        </td>

                        <td>
                            S/
                            ${formatNumber(
                                row.presupuesto_estimado,
                                2
                            )}
                        </td>

                        <td>
                            ${escapeHTML(
                                row.deadline_dias
                            )}
                            días
                        </td>

                        <td>
                            ${escapeHTML(
                                row.cantidad_bugs
                            )}
                        </td>

                        <td>
                            ${escapeHTML(
                                row.numero_desarrolladores
                            )}
                        </td>

                        <td>
                            ${escapeHTML(
                                row.tipo_servicio
                            )}
                        </td>

                        <td>
                            ${escapeHTML(
                                row.infraestructura_nube_previa
                            )}
                        </td>

                        <td>
                            ${escapeHTML(
                                row.renovacion_contrato
                            )}
                        </td>

                        <td>

                            <strong>

                                ${formatNumber(
                                    row.horas_hombre_invertidas,
                                    1
                                )}

                            </strong>

                        </td>

                        <td>
                            ${escapeHTML(
                                row.fecha_entrega
                            )}
                        </td>

                    </tr>
                `;

            })
            .join("");
}


/* =========================================================
   FORMATEAR NOMBRE DE COLUMNA
========================================================= */

function formatColumnName(column) {

    const names = {

        id_proyecto:
            "ID Proyecto",

        presupuesto_estimado:
            "Presupuesto",

        deadline_dias:
            "Deadline",

        cantidad_bugs:
            "Bugs",

        numero_desarrolladores:
            "Desarrolladores",

        tipo_servicio:
            "Tipo de Servicio",

        infraestructura_nube_previa:
            "Infraestructura Cloud",

        renovacion_contrato:
            "Renovación",

        horas_hombre_invertidas:
            "Horas Hombre",

        fecha_entrega:
            "Fecha Entrega"
    };


    return (
        names[column] ||
        column.replaceAll(
            "_",
            " "
        )
    );
}


/* =========================================================
   PAGINACIÓN
========================================================= */

function updatePagination(
    total,
    page,
    limit
) {

    const totalPages =
        Math.max(
            1,
            Math.ceil(
                total / limit
            )
        );


    const pageInfo =
        document.getElementById(
            "page-info"
        );


    if (pageInfo) {

        pageInfo.innerText =
            `Página ${page} de ${totalPages}`;
    }


    const prevButton =
        document.getElementById(
            "prev-page"
        );


    const nextButton =
        document.getElementById(
            "next-page"
        );


    if (prevButton) {

        prevButton.disabled =
            page <= 1;
    }


    if (nextButton) {

        nextButton.disabled =
            page >= totalPages;
    }
}


/* =========================================================
   CAMBIAR PÁGINA
========================================================= */

function changePage(direction) {

    const totalPages =
        Math.max(
            1,
            Math.ceil(
                totalRecords /
                rowsPerPage
            )
        );


    const newPage =
        currentPage +
        direction;


    if (
        newPage >= 1 &&
        newPage <= totalPages
    ) {

        currentPage =
            newPage;

        loadData();
    }
}


/* =========================================================
   CAMBIAR DATASET
========================================================= */

function changeDataset(dataset) {

    if (
        dataset !== "datos.csv" &&
        dataset !== "20k.csv"
    ) {

        console.error(
            "Dataset no permitido:",
            dataset
        );

        return;
    }


    currentDataset =
        dataset;


    currentPage =
        1;


    const select =
        document.getElementById(
            "dataset-select"
        );


    if (select) {

        select.value =
            dataset;
    }


    loadData();
}


/* =========================================================
   DEBOUNCE
========================================================= */

function debounce(
    callback,
    delay
) {

    let timeout;


    return function (...args) {

        clearTimeout(
            timeout
        );


        timeout =
            setTimeout(
                () => callback.apply(this, args),
                delay
            );
    };
}


/* =========================================================
   FORMATEAR NÚMEROS
========================================================= */

function formatNumber(
    value,
    decimals = 2
) {

    const number =
        Number(value);


    if (
        !Number.isFinite(number)
    ) {

        return "0";
    }


    return number.toLocaleString(
        "es-PE",
        {

            minimumFractionDigits:
                decimals,

            maximumFractionDigits:
                decimals
        }
    );
}


/* =========================================================
   SEGURIDAD HTML
========================================================= */

function escapeHTML(value) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";
    }


    return String(value)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );
}


/* =========================================================
   RESET ML
========================================================= */

function resetML() {

    const form =
        document.getElementById(
            "ml-form"
        );


    if (form) {

        form.reset();
    }


    const result =
        document.getElementById(
            "result-ml"
        );


    if (result) {

        result.classList.add(
            "hidden"
        );

        result.classList.remove(
            "show"
        );
    }
}


/* =========================================================
   RESET NN
========================================================= */

function resetNN() {

    const form =
        document.getElementById(
            "nn-form"
        );


    if (form) {

        form.reset();
    }


    const result =
        document.getElementById(
            "result-nn"
        );


    if (result) {

        result.classList.add(
            "hidden"
        );

        result.classList.remove(
            "show"
        );
    }
}


/* =========================================================
   RECARGAR DATOS
========================================================= */

function refreshData() {

    loadData();
}


/* =========================================================
   EXPORTAR FUNCIONES
   PARA ONCLICK DEL HTML
========================================================= */

window.showSection =
    showSection;

window.toggleSidebar =
    toggleSidebar;

window.predictML =
    predictML;

window.predictNN =
    predictNN;

window.changePage =
    changePage;

window.changeDataset =
    changeDataset;

window.refreshData =
    refreshData;

window.resetML =
    resetML;

window.resetNN =
    resetNN;

window.loadData =
    loadData;