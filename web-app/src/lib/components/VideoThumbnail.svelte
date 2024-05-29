<script>
    import Border from "./Border.svelte";
    import Grid from "./Grid.svelte";
    import TrashSymbol from "$lib/assets/delete-icon.svg";
    import { formatToMins } from "$lib/core/formatting";
    const BACKEND_URL = "http://127.0.0.1:8000";

    export let thumbNailUrl = "";
    export let title = "";
    export let id = 0;
    export let status = 1;
    let lengthMinutes = 0.0;
    let duration = 0.0
    export let clickBinding;
    export let deleteHandler;

    // We can get just a videos metadata with the video tag
    let metadataSource = BACKEND_URL + "/uploads/"  + id;

    $: lengthMinutes = formatToMins(duration);

</script>

<button on:click={clickBinding} style="flex: 0 1 300px ; align-self: flex-start; overflow-x: wrap; overflow-y: hidden;" class="thumbnail-button">
    <video style="display: none;" src="{metadataSource}" preload="metadata" bind:duration crossorigin="anonymous">
        <track kind="captions"/>
    </video>
    <Grid rows="1fr auto">
        <div style="width: 100%; height: 100%">
            <p>{lengthMinutes}</p>
            <button on:click|stopPropagation={deleteHandler} class="delete-button">
                <img src={TrashSymbol} alt="Delete Video" class="delete-icon">
            </button>
            <img src={thumbNailUrl} alt="thumbnail" class="thumbnail">
        </div>

        <h3>
            {#if status === 0}
            Processing
            {/if}
            {title}
           
        </h3>
    </Grid>
</button>

<style>
    .thumbnail-button {
        transition: background-color 2s;
        background-color: #393939;
        border-color: transparent;
        border-radius: 15px;
        margin: 10px 5px 0px 5px;
    }

    div {
        position: relative;
        background-color: var(--based-color);
    }

    .thumbnail {
        margin: 15px 15px 0px 15px;
        width: calc(100% - 32px);
        height: calc(100% - 15px);
        border-radius: 15px;
    }

    .delete-icon{
        
    }

    .delete-button {
        position: absolute;
        right: 3rem;
        top: .9rem;
        display: none;
        background-color: transparent;
        border-style: none;
        z-index: 100;
        border-radius: 8px;
        transition: background-color 0.3s;
    }

    .delete-button:hover{
        background-color: #60606083;
        transition: background-color 0.3s;
    }

    p {
        position: absolute;
        right: 3rem;
        bottom: 10px;
        background-color: #262626;
        color: #f4f4f4;
        padding: 4px 8px 4px 8px;
        border-radius: 4px;
    }

    h3 {
        margin: 8px 15px 0px 15px;
        color: #f4f4f4;
        overflow-wrap: break-word;
        min-width: 0;
        text-align: start;
    }

    .thumbnail-button div, .thumbnail-button h3 {
        background-color: transparent;
    }

    .thumbnail-button:hover{
        background-color: #606060;
        transition: background-color 0.8s;
    }

    .thumbnail-button:hover .delete-button{
        display: block;
    }
</style>