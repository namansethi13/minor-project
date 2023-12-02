//code by chatgpt creates A tag with href and download attribute for the file


// function format1(data) {
//     console.log(data);
//     fetch('http://127.0.0.1:8000/results/format1/', {
//         method: "POST",
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data),
//     })
//     .then(response => {
//         // Check if the response is successful (status code 200)
//         if (response.ok) {
//             // Extract filename from Content-Disposition header
//             const filename = response.headers.get('Content-Disposition').split('filename=')[1];
            
//             // Convert response to a blob
//             return response.blob().then(blob => {
//                 // Create a link to the blob
//                 const url = window.URL.createObjectURL(blob);
//                 const a = document.createElement('a');
//                 a.href = url;
//                 a.download = filename || 'download'; // Set default filename if not provided
//                 document.body.appendChild(a);
//                 a.click();
//                 document.body.removeChild(a);
//             });
//         } else {
//             // Handle errors
//             console.error('Error:', response.statusText);
//         }
//     })
//     .catch(error => {
//         console.error('Fetch error:', error);
//     });
// }



//node js testing
const axios = require('axios');
const fs = require('fs');

async function format1(data) {
    try {
        const response = await axios.post('http://127.0.0.1:8000/results/format1/', data, {
            headers: {
                'Content-Type': 'application/json',
            },
            responseType: 'stream', // Set the responseType to 'stream' for handling binary data
        });

        // Extract filename from Content-Disposition header
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
    } catch (error) {
        console.error('Error:', error.message);
    }
}


data={
    "course":["BCA","BCA"],
    "shift":'1',
    "semester":['2','3'],
    "passing":['2024','2023'],
    "sections":['B','A'],
    //additonals
    "subjectcodes":['020102','020104'],
    "faculty_name":"Pooja Singh",

}
format1(data)