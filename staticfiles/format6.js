const axios = require('axios');
const fs = require('fs');

async function format6(data) {
    try {
        const response = await axios.post('httpultlymsi.pythonanywhere.com/results/format6/', data, {
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
//demimter-done
//shhersh
//name-file
//buffer

data = {
    "2_BCA": {
        "faculty_name":"Cheshta",
        "needed_subjects":['020102','020104'],
        "sections":['A','B'],
        
        'shift':1,
        'admitted':'2021',
        'passing':'2024'
        
        }, 

    "3_BCA": {
        "faculty_name":"Cheshta",
        
        "needed_subjects":['020104'],

        "sections":['A'],
        
        'shift':1,
        'admitted':'2020',
        'passing':'2023'
       
        },
}
format6(data)