// Functions defining http requests to the api for use in the client

// Request the list of videos and their information in the database
export async function getVideos(BACKEND_URL)  {
    try{
        let response = await fetch(BACKEND_URL+'/list', {
            method: 'GET',
            headers: {
                'content-type': 'application/json',
                'Access-Control-Allow-Origin' : '*',
            }
        });
        if(response.ok){
            return response.json();
        }
        else{
            return null;
        }
    }
    catch{
        return null;
    }
}

export async function deleteVideo(BACKEND_URL, id) {
    try{
        let response = await fetch(`${BACKEND_URL}/delete/${id}`, {
            method: 'DELETE',
            headers: {
                'content-type': 'application/json',
                'Access-Control-Allow-Origin' : '*',
            }
        });
        if(response.ok){
            return true;
        }
        else{
            return false;
        }
    }
    catch{
        return false;
    }
}

// Gets the filename of a video in the database, filenames contain the id and the original name of the video for now
// export async function getVideoFileUrl(id = 0){
//     try{
//         let response = await fetch(`http://127.0.0.1:8000/uploads/url/${id}`, {
//             method: 'GET',
//             headers: {
//                 'content-type': 'application/json',
//                 'Access-Control-Allow-Origin' : '*',
//             }
//         });
//         if(response.ok){
//             return response.text();
//         }
//         else{
//             return null;
//         }
//     }
//     catch{
//         return null;
//     }
// }