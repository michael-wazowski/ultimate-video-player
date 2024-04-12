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