function format1(data) {
    data={
        "course":"BCA",
        "shift":'1',
        "sem":['2','3'],
        "passing":['2024','2023'],
        "subjectcodes":['020102','020202'],
        "sections":['B','A'],

    }
    fetch('http://127.0.0.1:8000/results/format1/',  {
        method: "POST",
        body: data, // Use FormData as the request body
    })
    .then(response => response.json()).then(data => {
        console.log(data)
    })
}

