// Functions defining http requests to the api for use in the client

export async function exampleServerFunc(a = 0 , b = 0) {
    try{
        let response = await fetch('/api', {
            method: 'POST',
            body: JSON.stringify({ a, b }),
            headers: {
                'content-type': 'application/json'
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

export async function getVideos()  {
    try{
        let response = await fetch('http://127.0.0.1:8000/list', {
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

export async function getVideoFileUrl(id = 0){
    try{
        let response = await fetch(`http://127.0.0.1:8000/uploads/url/${id}`, {
            method: 'GET',
            headers: {
                'content-type': 'application/json',
                'Access-Control-Allow-Origin' : '*',
            }
        });
        if(response.ok){
            return response.text();
        }
        else{
            return null;
        }
    }
    catch{
        return null;
    }
}