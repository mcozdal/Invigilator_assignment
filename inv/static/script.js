console.log('asdasd')


const button = document.getElementById('1234')
console.log(button.value)
var cluster1 = 'İstek Türü'

var kriterler = ['Hata', 'Yeni', 'Degisiklik', 'Destek', 'Fast']
var kriterlerLen = kriterler.length
var comps = new Array()

for (i = 0; i < kriterlerLen - 1; i++) {
    for (j = i + 1; j < kriterlerLen; j++) {
        comps.push([kriterler[i], kriterler[j]])
    }

}

compsLen = comps.length




function createTable(tableNo, cluster, comps) {
    const table = document.createElement('table')
    table.id = `table${tableNo}`
    document.body.appendChild(table)

    // header
    function createHeader(tableNo, cluster) {
        const row = document.createElement('tr')
        row.id = `header${tableNo}`

        table.append(row)

        // comparison
        const com = document.createElement('td')
        com.innerHTML = 'Comparsions'
        row.append(com)

        // Cluster Name
        const clusterName = document.createElement('td')
        clusterName.innerHTML = cluster
        row.append(clusterName)

        //left numbers
        for (i = 9; i >= 2; i--) {
            const number = document.createElement('td')
            number.innerHTML = i
            number.className = `n-left number left-${i}`
            row.append(number)
        }

        // Equal
        const seperator = document.createElement('td')
        seperator.innerHTML = '1'
        seperator.className = 'seperator number'
        row.append(seperator)

        //right numbers
        for (i = 2; i <= 9; i++) {
            // console.log(i)
            const number = document.createElement('td')
            number.innerHTML = i
            number.className = `n-right number right-${i}`
            row.append(number)
        }

        // Cluster Name

        const clusterName2 = document.createElement('td')
        clusterName2.innerHTML = cluster
        row.append(clusterName2)
    }

    createHeader(1, cluster)



    function createOptions(compNo) {
        row = document.createElement('tr');
        table.append(row)

        // comparison No
        const com = document.createElement('td')
        com.innerHTML = compNo + 1
        row.append(com)

        // Cluster Name
        const clusterName = document.createElement('td')
        clusterName.innerHTML = comps[compNo][0]
        row.append(clusterName)

        for (j = 9; j >= 2; j--) {
            // const box = document.createElement('td')
            // box.className = `number left-${j}`

            const box = create('td',
                { className: `number left-${j}` })

            row.append(box)
            // const radio = document.createElement('input')
            // radio.type = 'radio'
            // radio.name = `radio${compNo}`
            // radio.value = -j
            const radio = create('input',
                {
                    type: 'radio',
                    name: `radio${compNo}`,
                    value: -j
                })

            box.append(radio)
        }

        const box = create('td', {
            className: 'seperator number'
        })
        row.append(box)

        const seperator = create('input', {
            type: 'radio',
            name: `radio${compNo}`,
            value: 1
        })
        box.append(seperator)

        for (j = 2; j <= 9; j++) {

            const box = create('td', {
                className: `number right-${j}`
            })
            row.append(box)

            const radio = create('input',
                {
                    type: 'radio',
                    name: `radio${compNo}`,
                    value: j
                })
            box.append(radio)

        }


        const clusterName2 = document.createElement('td')
        clusterName2.innerHTML = comps[compNo][1]
        row.append(clusterName2)

    }
    for (i = 0; i < comps.length; i++) {
        createOptions(i)
    }
}

createTable(1, cluster1, comps)

function bb() {
    for (i = 0; i < 10; i++) {
        document.getElementsByName(`radio${i}`)[i].checked = 1
    }
}


function createData() {
    console.log('calisti')

    let data = new Array()
    var full = new Array()

    for (k = 0; k < compsLen; k++) {

        var abc = document.querySelector(`input[name="radio${k}"]:checked`).value
        full.push(abc)
        console.log(abc)
    }
    var index = 0

    for (i = 0; i < 5; i++) {
        let row = new Array()

        for (j = 0; j < 5; j++) {
            row.push(0)
        }
        data.push(row)
    }

    for (i = 0; i < 5; i++) {

        for (j = i + 1; j < 5; j++) {
            if (full[index] < 0) {
                data[j][i] = full[index] * - 1
                data[i][j] = `1 / ${full[index] * - 1}`
            } else {
                data[i][j] = full[index]
                data[j][i] = `1 / ${full[index]}`

            }
            index++
        }
    }

    console.log(data)
    // for (i = 0; i < comps.length; i++) {

    //     abc = document.querySelector(`input[name="radio${i}"]:checked`).value

    // //     console.log(abc)
    // }
    return data
}

function create(elem, props) {
    const obj = document.createElement(elem)

    for (let x in props) {
        obj[x] = props[x]
    }

    return obj
}

inp = create('input', {
    type: 'button', value: 'submit', onclick: 'postData()'
})
document.body.append(inp)

// async function postData() {
//     let data = createData()
//     const response = await fetch("/echo", {
//         method: "POST",
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify(data)
//     });
//     const actualResponse = await response.json();
// }


function postData() {

    let dat = createData()

    // Creating a XHR object
    let xhr = new XMLHttpRequest();
    let url = "http://127.0.0.1:8000/courses/anp/";

    // open a connection
    xhr.open("POST", url, true);

    // Set the request header i.e. which type of content you are sending
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    // Create a state change callback
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Print received data from server
            console.log(this.responseText);
        }
    };

    // Converting JSON data to string
    let data = JSON.stringify({ data: dat })
    console.log(data)
    // Sending data with the request
    xhr.send(data);
}

