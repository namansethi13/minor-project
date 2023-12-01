function format1(data) {
   console.log(data)
    fetch('http://127.0.0.1:8000/results/format1/',  {
        method: "POST",
        body: JSON.stringify(data),
    })
    .then(response => response.json()).then(data => {
        console.log(data)
    })
}




data={
    "course":"BCA",
    "shift":'1',
    "semester":['2','3'],
    "passing":['2024','2023'],
    "sections":['B','A'],
    //additonals
    "subjectcodes":['020102','020104'],

}
format1(data)