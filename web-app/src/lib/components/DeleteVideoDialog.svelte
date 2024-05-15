<script>
let dialogObject;
let id;
let videoName = "";
export function ShowDialog(deletedId, filename){
    dialogObject.showModal();
    id = deletedId;
    videoName = filename;
}

export let confirmedDelte;
</script>

<dialog bind:this={dialogObject}>
    <p> Are you sure you want to permanently delete the video "{videoName}"? You will NOT be able to recover it later.</p>
    <button on:click={() => {dialogObject.close(); confirmedDelte(id);}} class="yes" style="margin-right: 1rem;">Yes</button>
    <button on:click={() => dialogObject.close()} class="cancel">Cancel</button>
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

    .yes:hover{
        background-color: #da1e28;
    }

    .cancel:hover{
        background-color: #606060;
    }
</style>