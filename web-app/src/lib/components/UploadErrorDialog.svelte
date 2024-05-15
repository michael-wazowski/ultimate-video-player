<script>
    let dialogObject;
    export function ShowDialog(){
        dialogObject.showModal();
    }
    </script>
    
    <dialog bind:this={dialogObject}>
        <p> There was an error while trying to upload the video file!</p>
        <button on:click={() => dialogObject.close()} class="cancel">Ok</button>
    </dialog>
    
    <style>
        dialog{
            background-color: #262626;;
            border-radius: 15px;
            font-family: Barlow;
            color: #f4f4f4;
            border-color: #0f62fe;
        }
    
        button{
            font-family: Barlow;
            background-color: #393939;
            border-style: none;
            font-size: 12pt;
            color: #f4f4f4;
            height: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
            border-radius: .2rem;
            transition: background-color 0.4s;
        }
        
        .cancel:hover{
            background-color: #606060;
        }
    </style>