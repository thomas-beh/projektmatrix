function drawGanttDependencies() {
    const chart = document.querySelector(".gantt-chart");
    const svg = document.querySelector(".gantt-dependency-layer");

    if (!chart || !svg) {
        console.warn("Gantt chart or SVG layer not found.");
        return;
    }

    /*
     * Alte Verbindungen entfernen.
     */
    svg.querySelectorAll(".gantt-dependency-line")
        .forEach((element) => element.remove());


    const chartRect = chart.getBoundingClientRect();

    svg.setAttribute("width", chart.scrollWidth);
    svg.setAttribute("height", chart.scrollHeight);
    svg.setAttribute(
        "viewBox",
        `0 0 ${chart.scrollWidth} ${chart.scrollHeight}`
    );


    /*
     * Alle geplanten Work Steps suchen.
     */
    const workStepBars = Array.from(
        chart.querySelectorAll(
            ".gantt-bar-work-step.gantt-bar-planned"
        )
    );

    console.log(
        "Planned Work Step bars:",
        workStepBars.length
    );


    /*
     * Nach Development Stage gruppieren.
     */
    const groups = new Map();

    workStepBars.forEach((bar) => {
        const stageId = bar.dataset.dependencyFrom;

        console.log(
            "Work Step:",
            bar.id,
            "Parent:",
            stageId
        );

        if (!stageId) {
            return;
        }

        if (!groups.has(stageId)) {
            groups.set(stageId, []);
        }

        groups.get(stageId).push(bar);
    });


    console.log(
        "Development Stage groups:",
        groups
    );


    groups.forEach((children, stageId) => {

        /*
         * Passenden Hauptbalken suchen.
         */
        const stageBarId = `planned-${stageId}`;

        const stageBar =
            document.getElementById(stageBarId);

        console.log(
            "Looking for Stage:",
            stageBarId,
            stageBar
        );

        if (!stageBar) {
            console.warn(
                `Stage bar ${stageBarId} not found.`
            );
            return;
        }


        const stageRect =
            stageBar.getBoundingClientRect();


        /*
         * Verbindung beginnt ungefähr in der
         * Mitte des Development-Stage-Balkens.
         */
        const stageX =
            stageRect.left
            - chartRect.left
            + stageRect.width / 2;

        const stageY =
            stageRect.top
            - chartRect.top
            + stageRect.height / 2;


        /*
         * Positionen der Work Steps.
         */
        const childPositions = children.map((bar) => {
            const rect = bar.getBoundingClientRect();

            return {
                element: bar,

                x:
                    rect.left
                    - chartRect.left,

                y:
                    rect.top
                    - chartRect.top
                    + rect.height / 2,
            };
        });


        /*
         * Stamm bewusst etwas rechts vom
         * Startpunkt der Stage setzen.
         */
        let trunkX = stageX + 12;


        /*
         * Falls ein Work Step weiter links beginnt,
         * muss der Stamm trotzdem links von ihm liegen.
         */
        const leftMostChildX = Math.min(
            ...childPositions.map(
                child => child.x
            )
        );

        if (trunkX >= leftMostChildX - 8) {
            trunkX = leftMostChildX - 12;
        }


        const lastChildY = Math.max(
            ...childPositions.map(
                child => child.y
            )
        );


        /*
         * Stage -> Stamm
         *
         * Development Stage █████
         *                     |
         *                     |
         */
        drawLine(
            svg,
            stageX,
            stageY,
            trunkX,
            stageY,
            false
        );

        drawLine(
            svg,
            trunkX,
            stageY,
            trunkX,
            lastChildY,
            false
        );


        /*
         * Stamm -> Work Steps
         */
        childPositions.forEach((child) => {

            drawLine(
                svg,
                trunkX,
                child.y,
                child.x - 6,
                child.y,
                true
            );

        });
    });
}


function drawLine(
    svg,
    x1,
    y1,
    x2,
    y2,
    arrow
) {
    const line = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "line"
    );

    line.setAttribute(
        "class",
        "gantt-dependency-line"
    );

    line.setAttribute("x1", x1);
    line.setAttribute("y1", y1);
    line.setAttribute("x2", x2);
    line.setAttribute("y2", y2);

    if (arrow) {
        line.setAttribute(
            "marker-end",
            "url(#gantt-arrowhead)"
        );
    }

    svg.appendChild(line);
}


function initializeGanttDependencies() {
    /*
     * Ein requestAnimationFrame sorgt dafür,
     * dass Browser/Grid zunächst vollständig
     * layoutet wurden.
     */
    requestAnimationFrame(() => {
        drawGanttDependencies();
    });
}


document.addEventListener(
    "DOMContentLoaded",
    initializeGanttDependencies
);


window.addEventListener(
    "load",
    initializeGanttDependencies
);


window.addEventListener(
    "resize",
    drawGanttDependencies
);