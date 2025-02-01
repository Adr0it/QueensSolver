var matrix = document.getElementsByClassName("grid-wrapper")[0];
var numRows = document.getElementById("numRows");
var numCols = document.getElementById("numCols");
var colorWheel = document.getElementById("color-wheel");
var solveButton = document.getElementById("solve-button");

// add matrix size options
numRows.innerHTML = Array.from({ length: 19 }, (_, i) => `<option value="${i + 1}">${i + 1}</option>`).join('');
numCols.innerHTML = Array.from({ length: 19 }, (_, i) => `<option value="${i + 1}">${i + 1}</option>`).join('');

// change cell color on click
function updateCellColor(cell) {
    console.log(colorWheel.value);
    cell.style.backgroundColor = colorWheel.value;
}

// update matrix on dimensions change
function updateMatrix() {
    if (matrix.children.length > 0)
        matrix.innerHTML = "";

    let rows = parseInt(numRows.value);
    let cols = parseInt(numCols.value);
    console.log(`(${rows}, ${cols})`);

    for (let i = 1; i <= rows; i++) {
        for (let j = 1; j <= cols; j++) {
            let cell = document.createElement("div");  
            cell.className = "cell";  
            cell.id = `(${i}, ${j})`;
            cell.addEventListener("click", () => updateCellColor(cell));
            matrix.appendChild(cell);
        }
    }
    matrix.style.gridTemplateRows = `repeat(${rows}, 40px)`;
    matrix.style.gridTemplateColumns = `repeat(${cols}, 40px)`;
}
numRows.addEventListener("change", updateMatrix);
numCols.addEventListener("change", updateMatrix);
updateMatrix();

// sends data to optimizer, handles response
async function sendData(m) {
    try {
        const response = await fetch('http://127.0.0.1:5000/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(m)
        });

        const result = await response.json();
        console.log(result);

        if (result.solved.length == 0) {
            alert("Problem infeasible");
            return;
        }

        result.solved.forEach((cord) => {
            var cell = document.getElementById(`(${cord[0]}, ${cord[1]})`);
            cell.style.backgroundImage = "url('static/crown.png')";
            cell.style.backgroundPosition = "center";
            cell.style.backgroundSize = "35px";
        });
        
    } catch (error) {
        console.error('Error:', error);
    }
}

// prepare matrix data and send off to backend optimizer
function solveQueens() {
    let m = [];
    let colorMap = new Map();
    let colorIdx = 0;

    // initialize m
    for (var r = 0; r < parseInt(numRows.value); r++) {
        m[r] = [];
        for (var c = 0; c < parseInt(numCols.value); c++) {
            m[r][c] = 0;
        }
    }

    // fill m
    Array.from(matrix.children).forEach(child => {
        if (child.style.backgroundColor === "") {
            alert("At least one cell is not colored!");
            return;
        }
        let i = child.id.substring(1, child.id.indexOf(","));
        let j = child.id.substring(child.id.indexOf(",")+1, child.id.indexOf(")"));
        let color = child.style.backgroundColor;

        let idx; 
        if (colorMap.get(color)) {
            idx = colorMap.get(color);
        } else {
            colorIdx++;
            colorMap.set(color, colorIdx);
            idx = colorIdx;
        }
        m[i-1][j-1] = idx;
    });

    console.log(m);
    sendData(m);
}
solveButton.addEventListener("click", solveQueens);