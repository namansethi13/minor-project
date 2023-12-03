//axios get request to results/format2/?semester=3&course=bca

const axios = require('axios');
const fs = require('fs');

async function format7(semester, course) { // this is to get all the subjects of the semester and course
    try {
        const response = await axios.get(`http://127.0.0.1:8000/results/format7/?semester=${semester}&course=${course}`, {
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
format7(3, 'BCA')
    .then(subjectTeacherMapping => {
       // modify the teacher name in order of the Subjects
       // enter Section in the object (currently empty like this Section : "")
       // add course , shift ,semester, and passing year
       //final output example
//        subject teacher mapping = {
    
//         "Subjects": ["020102", "020104", "020106", "020108", "020110", "020136", "020172", "020174", "020176"],
//         "Faculty Names": ["Dr. ABC", "Dr. DEF", "Dr. GHI", "Dr. JKL", "Dr. MNO", "Dr. PQR", "Dr. STU", "Dr. VWX", "Dr. YZ"],
//         "Practicals": ["020172", "020174", "020176"],
//         "Section":'A',
//         "semester": '2',
//         "shift": 1,
//         "passing": 2024,
//         "course": "BCA"  
    
// }
        console.log(subjectTeacherMapping);
        subjectTeacherMapping['Section'] = 'A';
        subjectTeacherMapping['semester'] = '2';
        subjectTeacherMapping['shift'] = 1;
        subjectTeacherMapping['passing'] = 2024;
        subjectTeacherMapping['course'] = 'BCA';
        format2Post(subjectTeacherMapping);

    })
    .catch(error => {
        console.error('Error:', error.message);
    }); // now modify the teacher name and post it to same url
// console.log(subjectTeacherMapping);
// subjectTeacherMapping['020106'] = 'Pooja Singh';

//post request to results/format2/


async function format2Post(subjectTeacherMapping) {
    try {
        const response = await axios.post('http://127.0.0.1:8000/results/format7/', subjectTeacherMapping, {
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

