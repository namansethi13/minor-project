//axios get request to results/format2/?semester=3&course=bca

const axios = require('axios');
const fs = require('fs');

async function format2(semester, course) { // this is to get all the subjects of the semester and course
    try {
        const response = await axios.get(`http://https://resultlymsi.pythonanywhere.com/results/format2/?semester=${semester}&course=${course}`, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        //print response
        return response.data;
    }
    catch (error) {
        console.error('Error:', error.message);
    }
}
format2(3, 'BCA')
    .then(subjectTeacherMapping => {
        subjectTeacherMapping['020106'] = 'Pooja Singh';
        format2Post(subjectTeacherMapping);

    })
    .catch(error => {
        console.error('Error:', error.message);
    }); // now modify the teacher name and post it to same url
// console.log(subjectTeacherMapping);
// subjectTeacherMapping['020106'] = 'Pooja Singh';

//post request to results/format2/


async function format2Post(subjectTeacherMapping) {
    data = {
        "course":"BCA",
        "shift": '1',
        "semester": '3',
        "passing": '2023',
        "section": 'A',
        "faculty_name":"pooja singh",
        // additionals format 2 
        // endpoint hit then get faculty details of all the subjects
        
        // additional format 6
        "batch": "2020-2023",
        "subjectTeacherMapping": subjectTeacherMapping,




    }
    try {
        const response = await axios.post('http://https://resultlymsi.pythonanywhere.com/results/format2/', data, {
            headers: {
                'Content-Type': 'application/json',
            },
            responseType: 'stream', // Set the responseType to 'stream' for handling binary data
        });
       const contentDispositionHeader = response.headers['content-disposition'];
        const filename = contentDispositionHeader ? contentDispositionHeader.split('filename=')[1] : 'download';

        // Create a write stream to save the file
        const writeStream = fs.createWriteStream(filename);

        // Pipe the response stream to the write stream
        response.data.pipe(writeStream);

        // Wait for the write stream to finish writing the file
        await new Promise(resolve => {
            writeStream.on('finish', resolve);
        });

        console.log(`File "${filename}" downloaded successfully.`);
        
    }
    catch (error) {
        console.error('Error:', error.message);
    }
}

